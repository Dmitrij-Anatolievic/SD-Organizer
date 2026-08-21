"""
SD Organizer Logic Module
Fixed and Enhanced Version - CRASH FIX APPLIED + DATABASE INTEGRATION
"""
import os
import shutil
import datetime
import logging
import psutil
from PIL import Image
from PIL.ExifTags import TAGS
from abc import ABC
import json
import sys
from collections import defaultdict
import locale
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional, List, Dict, Tuple, Callable

# V3 Enhancement: Database integration
try:
    from database_manager import PhotoDatabase
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False
    print("Warning: Database module not available. Running without database features.")

IS_WINDOWS = sys.platform == "win32"
if IS_WINDOWS:
    try:
        import wmi
    except ImportError:
        wmi = None
        print("Warning: 'wmi' library not found. Falling back to psutil for drive detection.")


class SDOrganizerBase(ABC):
    """
    Base class with improved error handling and cross-platform compatibility.
    """
    # Class-level lock for thread safety
    _logger_lock = threading.Lock()
    
    def __init__(self, brand_name, pictures_path=None, logs_path=None, log_to_gui_callback=None, config=None, app_config=None):
        self.brand_name = brand_name
        self.log_to_gui_callback = log_to_gui_callback
        self.config = config or {}
        self.app_config = app_config or {}
        self.pictures_path = pictures_path
        self.logs_path = logs_path
        self.logger = self._setup_logging()
        self.undo_log = []
        self.last_undo_log_path = None
        self._operation_lock = threading.Lock()
        
        # V3 Enhancement: Initialize database
        self.database = None
        if DATABASE_AVAILABLE:
            try:
                self.database = PhotoDatabase()
                self.log_and_callback("info", "Database initialized successfully")
            except Exception as e:
                self.log_and_callback("warning", f"Could not initialize database: {e}")
        
        # SD Card cache for persistent identification
        self.sd_card_cache_file = os.path.join(os.path.expanduser("~"), ".sd_organizer_cache.json")
        self.sd_card_cache = self._load_sd_card_cache()
        
        # Setup Italian locale with better fallback handling
        self._setup_locale()

    def _setup_locale(self):
        """Setup Italian locale with proper fallback"""
        locale_options = ['it_IT.UTF-8', 'it_IT', 'Italian_Italy', 'Italian']
        locale_set = False
        
        for loc in locale_options:
            try:
                locale.setlocale(locale.LC_TIME, loc)
                locale_set = True
                self.log_and_callback("info", f"Locale set to: {loc}")
                break
            except locale.Error:
                continue
        
        if not locale_set:
            self.log_and_callback("warning", "Italian locale not available. Month names will be in English.")

    def _load_sd_card_cache(self):
        """Load SD card cache from file"""
        try:
            if os.path.exists(self.sd_card_cache_file):
                with open(self.sd_card_cache_file, 'r', encoding='utf-8') as f:
                    cache = json.load(f)
                    self.log_and_callback("info", f"Loaded SD card cache with {len(cache)} entries")
                    return cache
        except Exception as e:
            self.log_and_callback("warning", f"Could not load SD card cache: {e}")
        return {}
    
    def _save_sd_card_cache(self, volume_serial, drive_info):
        """Save SD card info to cache for future identification"""
        try:
            if not volume_serial:
                return
            
            self.sd_card_cache[volume_serial] = {
                'last_seen': datetime.datetime.now().isoformat(),
                'volume_name': drive_info.get('volume_name', ''),
                'brand': self.brand_name,
                'last_path': drive_info.get('path', '')
            }
            
            with open(self.sd_card_cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.sd_card_cache, f, indent=2, ensure_ascii=False)
            
            self.log_and_callback("info", f"Saved SD card to cache (Serial: {volume_serial})")
        except Exception as e:
            self.log_and_callback("warning", f"Could not save SD card cache: {e}")
    
    def _find_cached_sd_card(self, detected_drives):
        """Try to find previously used SD card by volume serial"""
        try:
            for drive in detected_drives:
                volume_serial = drive.get('volume_serial')
                if volume_serial and volume_serial in self.sd_card_cache:
                    cached_info = self.sd_card_cache[volume_serial]
                    self.log_and_callback("info", 
                        f"Recognized SD card from cache! "
                        f"Last seen: {cached_info.get('last_seen', 'unknown')}, "
                        f"Previous path: {cached_info.get('last_path', 'unknown')}")
                    return drive
        except Exception as e:
            self.log_and_callback("debug", f"Error checking cache: {e}")
        return None

    def _setup_logging(self):
        """Setup logging with improved error handling"""
        log_filename = f"log_sposta_{self.brand_name}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        try:
            os.makedirs(self.logs_path, exist_ok=True)
            log_file_path = os.path.join(self.logs_path, log_filename)
        except (OSError, TypeError) as e:
            fallback_dir = os.path.expanduser("~")
            self.log_and_callback("warning", f"Could not create log directory at '{self.logs_path}'. Using home folder. Error: {e}")
            self.logs_path = fallback_dir
            log_file_path = os.path.join(self.logs_path, log_filename)

        with self._logger_lock:
            logger = logging.getLogger(f"{self.brand_name}SDOrganizer_{id(self)}")
            logger.setLevel(logging.INFO)
            
            # Remove existing handlers to avoid duplicates
            for handler in logger.handlers[:]:
                handler.close()
                logger.removeHandler(handler)

            # Define formatter BEFORE use to prevent UnboundLocalError
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            
            # File handler with UTF-8 encoding
            try:
                file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
                file_handler.setLevel(logging.INFO)
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
            except Exception as e:
                print(f"Warning: Could not create file handler: {e}")
            
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        return logger

    def log_and_callback(self, level, message):
        """Log message with improved error handling"""
        try:
            if level == "info":
                self.logger.info(message)
            elif level == "warning":
                self.logger.warning(message)
            elif level == "error":
                self.logger.error(message)
            
            if self.log_to_gui_callback:
                try:
                    self.log_to_gui_callback(message)
                except Exception as e:
                    print(f"Warning: Could not send log to GUI: {e}")
        except Exception as e:
            print(f"Logging error: {e}")

    def detect_removable_drives(self):
        """Detect removable drives with improved cross-platform support"""
        drives = []
        
        if IS_WINDOWS:
            if wmi:
                drives = self._detect_drives_wmi()
            else:
                drives = self._detect_drives_psutil()
        else:
            drives = self._detect_drives_unix()
        
        self.log_and_callback("info", f"Detected {len(drives)} removable drive(s): {', '.join([d['label'] for d in drives]) if drives else 'None'}")
        return drives

    def find_sd_card_path(self):
        """
        Find SD card path by scanning removable drives for brand-specific folders.
        Returns list of dictionaries with drive info.
        """
        self.log_and_callback("info", f"Searching for SD card with '{self.brand_name}' folders...")
        
        if not self.config:
            self.log_and_callback("error", "Configuration for this brand is missing.")
            return []

        folder_names = self.config.get("SD_FOLDER_NAMES_CANDIDATES") or self.config.get("SD_CARD_FOLDERS")
        if not folder_names:
            self.log_and_callback("warning", "No 'SD_FOLDER_NAMES_CANDIDATES' or 'SD_CARD_FOLDERS' in config. Cannot find SD card.")
            return []
            
        self.log_and_callback("info", f"Will search for folders: {', '.join(folder_names)}")
        
        # Get list of removable drives
        scan_drives = set()
        
        if IS_WINDOWS and wmi:
            self.log_and_callback("info", "Using WMI for drive detection...")
            try:
                c = wmi.WMI()
                for disk in c.Win32_LogicalDisk(DriveType=2):
                    try:
                        drive_path = disk.DeviceID + "\\"
                        if os.path.exists(drive_path):
                            scan_drives.add(drive_path)
                    except (OSError, AttributeError):
                        continue
            except Exception as e:
                self.log_and_callback("warning", f"WMI query failed: {e}. Falling back to psutil.")
        
        # Always use psutil as primary or fallback
        self.log_and_callback("info", "Using psutil to scan for drives.")
        try:
            all_drives = psutil.disk_partitions(all=False)
            for d in all_drives:
                try:
                    # Safely handle d.opts which can be string or list
                    opts_str = ''
                    if isinstance(d.opts, str):
                        opts_str = d.opts.lower()
                    elif isinstance(d.opts, list):
                        opts_str = ','.join(d.opts).lower()
                    else:
                        opts_str = str(d.opts).lower()
                    
                    # Check for removable drives
                    if 'removable' in opts_str:
                        if os.path.exists(d.mountpoint):
                            scan_drives.add(d.mountpoint)
                    
                    # Check for SD card file systems
                    if d.fstype and d.fstype.lower() in ['exfat', 'vfat', 'fat32', 'fat']:
                        if os.path.exists(d.mountpoint):
                            scan_drives.add(d.mountpoint)
                except (AttributeError, TypeError, OSError):
                    continue
            
            if not scan_drives:
                self.log_and_callback("warning", "No specific removable drives found. Scanning ALL drives as a fallback.")
                for d in all_drives:
                    if os.path.exists(d.mountpoint):
                        scan_drives.add(d.mountpoint)
        except Exception as e:
            self.log_and_callback("error", f"Critical error during psutil drive scan: {e}")
            return []

        self.log_and_callback("info", f"Scanning {len(scan_drives)} candidate drives: {sorted(list(scan_drives))}")
        found_devices = []
        
        for drive_path in sorted(list(scan_drives)):
            try:
                # Check if drive is accessible
                if not os.path.isdir(drive_path):
                    continue
                
                # Look for DCIM folder
                dcim_path = os.path.join(drive_path, "DCIM")
                if not os.path.isdir(dcim_path):
                    continue
                
                # Search for brand-specific folders
                for folder_name in folder_names:
                    candidate_path = os.path.join(dcim_path, folder_name)
                    if os.path.isdir(candidate_path):
                        self.log_and_callback("info", f"SUCCESS! Found compatible folder: {candidate_path}")
                        found_devices.append({
                            'drive_path': drive_path,
                            'brand_folder': folder_name,
                            'full_path': candidate_path
                        })
                        # Don't break - there might be multiple folders
            except (PermissionError, FileNotFoundError, OSError) as e:
                self.log_and_callback("debug", f"Cannot access {drive_path}: {e}")
                continue
            except Exception as e:
                self.log_and_callback("error", f"Unexpected error while checking {drive_path}: {e}")
        
        if not found_devices:
            self.log_and_callback("warning", "Scan complete. No compatible SD cards found.")
        else:
            self.log_and_callback("info", f"Found {len(found_devices)} compatible SD card(s).")
        
        return found_devices

    def _detect_drives_wmi(self):
        """Detect drives using WMI (Windows)"""
        drives = []
        try:
            c = wmi.WMI()
            for drive in c.Win32_LogicalDisk(DriveType=2):  # DriveType=2 means removable
                try:
                    # Verify drive is accessible
                    drive_path = drive.Caption + "\\"
                    if os.path.exists(drive_path) and os.path.isdir(drive_path):
                        volume_name = drive.VolumeName or 'Removable Drive'
                        # Get volume serial number for unique identification
                        volume_serial = getattr(drive, 'VolumeSerialNumber', None)
                        drives.append({
                            'label': f"{drive.Caption} - {volume_name}",
                            'path': drive_path,
                            'volume_serial': volume_serial,
                            'volume_name': volume_name
                        })
                        self.log_and_callback("info", f"Found removable drive: {drive.Caption} (Serial: {volume_serial})")
                except (OSError, AttributeError, PermissionError) as e:
                    self.log_and_callback("debug", f"Skipping drive {drive.Caption}: {e}")
                    continue
        except Exception as e:
            self.log_and_callback("warning", f"WMI drive detection failed: {e}. Falling back to psutil.")
            drives = self._detect_drives_psutil()
        return drives

    def _detect_drives_psutil(self):
        """Detect drives using psutil (cross-platform fallback)"""
        drives = []
        try:
            partitions = psutil.disk_partitions(all=False)
            for partition in partitions:
                try:
                    # Safely handle partition.opts which can be string or list
                    opts_str = ''
                    if isinstance(partition.opts, str):
                        opts_str = partition.opts.lower()
                    elif isinstance(partition.opts, list):
                        opts_str = ','.join(partition.opts).lower()
                    else:
                        opts_str = str(partition.opts).lower()
                    
                    if IS_WINDOWS:
                        # Check for removable drives or common SD card file systems
                        is_removable = 'removable' in opts_str
                        is_sd_filesystem = partition.fstype and partition.fstype.lower() in ['exfat', 'vfat', 'fat32', 'fat']
                        
                        if is_removable or is_sd_filesystem:
                            # Verify the drive is accessible
                            if os.path.exists(partition.mountpoint) and os.path.isdir(partition.mountpoint):
                                drives.append({
                                    'label': f"{partition.device} - {partition.mountpoint}",
                                    'path': partition.mountpoint
                                })
                    else:
                        # Unix/Linux/Mac: check for typical removable media mount points
                        if '/media/' in partition.mountpoint or '/mnt/' in partition.mountpoint:
                            if os.path.exists(partition.mountpoint) and os.path.isdir(partition.mountpoint):
                                drives.append({
                                    'label': f"{partition.device} - {os.path.basename(partition.mountpoint)}",
                                    'path': partition.mountpoint
                                })
                except (OSError, AttributeError, PermissionError) as e:
                    # Skip drives that we can't access
                    self.log_and_callback("debug", f"Skipping drive {partition.device}: {e}")
                    continue
        except Exception as e:
            self.log_and_callback("error", f"psutil drive detection failed: {e}")
        return drives

    def _detect_drives_unix(self):
        """Detect drives on Unix-like systems"""
        drives = []
        media_path = "/media/"
        mnt_path = "/mnt/"
        
        try:
            for base_path in [media_path, mnt_path]:
                if not os.path.exists(base_path):
                    continue
                    
                try:
                    for user_dir in os.listdir(base_path):
                        user_path = os.path.join(base_path, user_dir)
                        if not os.path.isdir(user_path):
                            continue
                            
                        try:
                            for mount_dir in os.listdir(user_path):
                                mount_path = os.path.join(user_path, mount_dir)
                                try:
                                    if os.path.ismount(mount_path) and os.path.isdir(mount_path):
                                        drives.append({
                                            'label': f"{mount_dir}",
                                            'path': mount_path
                                        })
                                except (OSError, PermissionError):
                                    continue
                        except (OSError, PermissionError):
                            continue
                except (OSError, PermissionError):
                    continue
        except Exception as e:
            self.log_and_callback("warning", f"Unix drive detection failed: {e}")
        
        return drives

    def find_sd_card_folders(self, sd_root_path):
        """Find SD card folders with improved error handling"""
        candidates = self.config.get("SD_FOLDER_NAMES_CANDIDATES", [])
        if not candidates:
            self.log_and_callback("warning", f"No SD folder candidates configured for {self.brand_name}")
            return []

        found_folders = []
        try:
            for candidate in candidates:
                full_path = os.path.join(sd_root_path, candidate)
                if os.path.exists(full_path) and os.path.isdir(full_path):
                    found_folders.append({
                        'name': candidate,
                        'path': full_path
                    })
        except Exception as e:
            self.log_and_callback("error", f"Error searching for SD folders: {e}")
        
        return found_folders

    def analyze_dates_in_sd(self, sd_full_path) -> Dict[str, Dict]:
        """
        Pre-scan SD card and group files by date
        V3 Enhancement: Multi-event support
        
        Returns:
            Dictionary with date as key and info dict as value:
            {
                '2025-10-10': {
                    'files': [list of file paths],
                    'count': number of files,
                    'date_obj': datetime object
                },
                ...
            }
        """
        self.log_and_callback("info", "Analyzing dates in SD card...")
        
        files_to_process = self._collect_files_to_process(sd_full_path)
        if not files_to_process:
            return {}
        
        # Extract dates for all files
        file_metadata = self._parallel_extract_metadata(files_to_process, progress_callback=None)
        
        # Group by date
        date_groups = defaultdict(lambda: {'files': [], 'count': 0, 'date_obj': None})
        
        for file_path, date in file_metadata.items():
            if not date:
                date = datetime.datetime.now()
            
            date_str = date.strftime("%Y-%m-%d")
            date_groups[date_str]['files'].append(file_path)
            date_groups[date_str]['count'] += 1
            if date_groups[date_str]['date_obj'] is None:
                date_groups[date_str]['date_obj'] = date
        
        # Sort by date
        sorted_groups = dict(sorted(date_groups.items()))
        
        self.log_and_callback("info", f"Found {len(sorted_groups)} different dates in SD card")
        for date_str, info in sorted_groups.items():
            self.log_and_callback("info", f"  - {date_str}: {info['count']} files")
        
        return sorted_groups
    
    def organize_sd_files(self, sd_full_path, topic, move_files=True, progress_callback=None):
        """Organize files with thread safety and improved error handling"""
        with self._operation_lock:
            return self._organize_sd_files_internal(sd_full_path, topic, move_files, progress_callback)
    
    def organize_sd_files_multi_event(self, sd_full_path, event_mapping: Dict[str, str], move_files=True, progress_callback=None):
        """
        Organize files with different event names for different dates
        V3 Enhancement: Multi-event support
        
        Args:
            sd_full_path: Path to SD card
            event_mapping: Dictionary mapping date string to event name
                          {'2025-10-10': 'Matrimonio_Maria', '2025-10-11': 'Battesimo_Luca', ...}
            move_files: Whether to move or copy
            progress_callback: Progress callback function
            
        Returns:
            True if successful
        """
        with self._operation_lock:
            return self._organize_sd_files_multi_event_internal(sd_full_path, event_mapping, move_files, progress_callback)
    
    def _organize_sd_files_multi_event_internal(self, sd_full_path, event_mapping, move_files, progress_callback):
        """Internal organization logic for multi-event import"""
        self.log_and_callback("info", f"Starting multi-event organization from: {sd_full_path}")
        self.undo_log = []

        # Validate paths
        if not os.path.exists(sd_full_path):
            self.log_and_callback("error", f"Source path does not exist: {sd_full_path}")
            return False

        if not self.check_write_permissions(self.pictures_path):
            return False
            
        min_free_gb = self.app_config.get("MIN_FREE_SPACE_GB", 5)
        if not self.check_disk_space(sd_full_path, self.pictures_path, min_free_gb):
            return False
        
        files_to_process = self._collect_files_to_process(sd_full_path)
        if not files_to_process:
            self.log_and_callback("warning", "No compatible files found to process.")
            return True

        total_files = len(files_to_process)
        self.log_and_callback("info", f"Found {total_files} files to process with {len(event_mapping)} different events.")
        
        # Extract metadata in parallel
        self.log_and_callback("info", "Pre-reading EXIF data in parallel...")
        file_metadata = self._parallel_extract_metadata(files_to_process, progress_callback)
        
        processed_count = 0

        for source_path in files_to_process:
            processed_count += 1
            try:
                # Get date for this file
                date = file_metadata.get(source_path)
                if not date:
                    self.log_and_callback("warning", f"No date for {os.path.basename(source_path)}. Using current date.")
                    date = datetime.datetime.now()
                
                # Find event name for this date
                date_str = date.strftime("%Y-%m-%d")
                event_name = event_mapping.get(date_str)
                
                if not event_name:
                    # Fallback to generic name if date not in mapping
                    event_name = "Uncategorized"
                    self.log_and_callback("warning", f"No event name for date {date_str}, using 'Uncategorized'")
                
                # Sanitize event name
                topic_sanitized = self._sanitize_topic_name(event_name)
                if not topic_sanitized:
                    topic_sanitized = "Event"
                
                topic_name = topic_sanitized.replace(" ", "_")
                
                # Process file with appropriate event name
                self._process_single_file_with_date(source_path, topic_name, date, move_files)
                
                if progress_callback:
                    progress_percentage = int(processed_count / total_files * 100)
                    progress_callback(progress_percentage, os.path.basename(source_path))
                    
            except Exception as e:
                self.log_and_callback("error", f"Failed to process file {os.path.basename(source_path)}: {e}")
                continue

        if move_files:
            self.save_undo_log()
            
        self.log_and_callback("info", "Multi-event organization process finished.")
        return True

    def _organize_sd_files_internal(self, sd_full_path, topic, move_files, progress_callback):
        """Internal organization logic with parallel EXIF reading"""
        # Validate topic name
        topic = self._sanitize_topic_name(topic)
        if not topic:
            self.log_and_callback("error", "Invalid topic name provided.")
            return False
            
        self.log_and_callback("info", f"Starting organization process for '{topic}' from: {sd_full_path}")
        self.undo_log = []

        # Validate paths
        if not os.path.exists(sd_full_path):
            self.log_and_callback("error", f"Source path does not exist: {sd_full_path}")
            return False

        if not self.check_write_permissions(self.pictures_path):
            return False
            
        min_free_gb = self.app_config.get("MIN_FREE_SPACE_GB", 5)
        if not self.check_disk_space(sd_full_path, self.pictures_path, min_free_gb):
            return False
        
        files_to_process = self._collect_files_to_process(sd_full_path)
        if not files_to_process:
            self.log_and_callback("warning", "No compatible files found to process.")
            return True

        total_files = len(files_to_process)
        self.log_and_callback("info", f"Found {total_files} files to process.")
        
        # === PARALLEL EXIF READING ===
        self.log_and_callback("info", "Pre-reading EXIF data in parallel...")
        file_metadata = self._parallel_extract_metadata(files_to_process, progress_callback)
        
        processed_count = 0
        topic_name = topic.replace(" ", "_")

        for source_path in files_to_process:
            processed_count += 1
            try:
                # Use pre-extracted metadata
                date = file_metadata.get(source_path)
                if not date:
                    self.log_and_callback("warning", f"No date for {os.path.basename(source_path)}. Using current date.")
                    date = datetime.datetime.now()
                
                self._process_single_file_with_date(source_path, topic_name, date, move_files)
                
                if progress_callback:
                    progress_percentage = int(processed_count / total_files * 100)
                    progress_callback(progress_percentage, os.path.basename(source_path))
            except Exception as e:
                self.log_and_callback("error", f"Failed to process file {os.path.basename(source_path)}: {e}")
                # Continue processing other files instead of crashing
                continue

        if move_files:
            self.save_undo_log()
            
        self.log_and_callback("info", "Organization process finished.")
        return True

    def _sanitize_topic_name(self, topic):
        """Sanitize topic name to be filesystem-safe"""
        if not topic or not topic.strip():
            return None
            
        # Remove dangerous characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            topic = topic.replace(char, '_')
            
        # Remove leading/trailing whitespace and underscores
        topic = topic.strip().strip('_')
        
        # Limit length
        max_length = 50
        if len(topic) > max_length:
            topic = topic[:max_length].rstrip('_')
            
        return topic if topic else None

    def _collect_files_to_process(self, source_dir):
        """Collect files with improved error handling"""
        files_to_process = []
        supported_extensions = self.config.get("FILE_DESTINATIONS", {}).keys()
        
        if not supported_extensions:
            self.log_and_callback("error", "No file extensions configured for this brand.")
            return []

        try:
            for root, _, files in os.walk(source_dir):
                for file in files:
                    if any(file.lower().endswith(ext) for ext in supported_extensions):
                        file_path = os.path.join(root, file)
                        # Skip hidden files
                        if not os.path.basename(file).startswith('.'):
                            files_to_process.append(file_path)
        except Exception as e:
            self.log_and_callback("error", f"Error collecting files from {source_dir}: {e}")
        
        return files_to_process

    def _parallel_extract_metadata(self, file_paths: List[str], progress_callback: Optional[Callable] = None) -> Dict[str, Optional[datetime.datetime]]:
        """
        Extract EXIF metadata from multiple files in parallel.
        
        Args:
            file_paths: List of file paths to process
            progress_callback: Optional callback for progress updates
            
        Returns:
            Dictionary mapping file paths to their extracted dates
        """
        file_metadata = {}
        max_workers = min(4, len(file_paths))  # Limit to 4 threads
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_file = {
                executor.submit(self.get_date_taken, file_path): file_path 
                for file_path in file_paths
            }
            
            completed = 0
            total = len(file_paths)
            
            # Collect results as they complete
            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    date = future.result()
                    file_metadata[file_path] = date
                except Exception as e:
                    self.log_and_callback("warning", f"Error extracting metadata from {os.path.basename(file_path)}: {e}")
                    file_metadata[file_path] = None
                
                completed += 1
                if progress_callback and completed % 10 == 0:
                    # Update progress every 10 files during metadata extraction
                    progress_percentage = int(completed / total * 30)  # Use 30% of progress bar for this phase
                    progress_callback(progress_percentage, f"Reading metadata: {completed}/{total}")
        
        return file_metadata

    def _process_single_file_with_date(self, source_path: str, topic: str, date: datetime.datetime, move_files: bool) -> None:
        """
        Process a single file with pre-extracted date.
        ⚠️ BUG FIX APPLIED: Fixed path construction with empty subfolder
        ✅ IMPROVEMENT: Smart folder reuse with clear logging
        
        Args:
            source_path: Path to source file
            topic: Topic/event name
            date: Pre-extracted date
            move_files: Whether to move or copy
        """
        try:
            # Determine destination folder
            ext = os.path.splitext(source_path)[1].lower()
            subfolder = self.config.get("FILE_DESTINATIONS", {}).get(ext, "")
            
            year_str = date.strftime("%Y")
            
            # Fallback for month name if locale fails
            try:
                month_name_str = date.strftime("%B").capitalize()
            except:
                # Fallback to English month names
                month_names = ['January', 'February', 'March', 'April', 'May', 'June',
                             'July', 'August', 'September', 'October', 'November', 'December']
                month_name_str = month_names[date.month - 1]
            
            day_str = date.strftime("%d")
            day_folder_name = f"{day_str}_{topic}"
            
            # ⚠️ SUPER SMART PATH LOGIC - Check what's already in the path
            # User might provide:
            #   - C:\...\Nikon → Add 2025\Ottobre\21_Prova
            #   - C:\...\Nikon\2025 → Add Ottobre\21_Prova (year already there!)
            #   - C:\...\Nikon\2025\Ottobre → Add 21_Prova (year+month already there!)
            
            base_path = os.path.normpath(self.pictures_path)
            path_parts = base_path.split(os.sep)
            
            # Check what's already in the path
            year_in_path = year_str in path_parts
            
            # For month, check with different formats
            month_in_path = False
            if year_in_path and len(path_parts) >= 2:
                # Check if last part is the month
                last_part = path_parts[-1] if path_parts else ""
                if last_part.lower() == month_name_str.lower():
                    month_in_path = True
            
            # Build the path intelligently
            if year_in_path:
                # Year is already in path
                if month_in_path:
                    # Both year AND month are in path
                    # Just add day folder
                    day_path = os.path.join(base_path, day_folder_name)
                    if not hasattr(self, '_warned_full_path'):
                        self.log_and_callback("info", f"ℹ️  Using existing year+month folders: {year_str}/{month_name_str}")
                        self._warned_full_path = True
                else:
                    # Only year is in path, add month + day
                    day_path = os.path.join(base_path, month_name_str, day_folder_name)
                    if not hasattr(self, '_warned_year_in_path'):
                        self.log_and_callback("info", f"ℹ️  Using existing year folder: {year_str}")
                        self._warned_year_in_path = True
            else:
                # Normal case: add year + month + day
                day_path = os.path.join(base_path, year_str, month_name_str, day_folder_name)
            
            # For logging purposes, determine year_path and month_path
            if year_in_path:
                year_path = base_path
                if month_in_path:
                    month_path = base_path
                else:
                    month_path = os.path.join(base_path, month_name_str)
            else:
                year_path = os.path.join(base_path, year_str)
                month_path = os.path.join(year_path, month_name_str)
            
            # Check what exists and log appropriately
            year_exists = os.path.exists(year_path)
            month_exists = os.path.exists(month_path)
            day_exists = os.path.exists(day_path)
            
            # ⚠️ BUG FIX: Handle empty subfolder correctly
            # Use os.path.join for cross-platform compatibility
            if subfolder and subfolder.strip():
                # Split subfolder by both / and \ for cross-platform compatibility
                subfolder_parts = subfolder.replace('\\', '/').split('/')
                subfolder_parts = [part for part in subfolder_parts if part]  # Remove empty parts
                
                destination_folder = os.path.join(
                    day_path,
                    *subfolder_parts  # Now safe to unpack
                )
            else:
                # No subfolder, use simple path
                destination_folder = day_path
            
            # Create destination directory intelligently
            folder_exists = os.path.exists(destination_folder)
            
            if not folder_exists:
                os.makedirs(destination_folder, exist_ok=True)
                # Log only NEW folder creation
                if not year_exists:
                    self.log_and_callback("info", f"📁 Created year folder: {year_str}")
                if not month_exists:
                    self.log_and_callback("info", f"📁 Created month folder: {month_name_str}")
                if not day_exists:
                    self.log_and_callback("info", f"📁 Created day folder: {day_folder_name}")
            else:
                # Folder already exists - REUSING IT (this is the fix the user wants!)
                # Only log once per session to avoid spam
                if not hasattr(self, '_logged_reuse_folders'):
                    self._logged_reuse_folders = set()
                
                folder_key = f"{year_str}/{month_name_str}/{day_folder_name}"
                if folder_key not in self._logged_reuse_folders:
                    self.log_and_callback("info", f"♻️  Reusing existing folder: {year_str}/{month_name_str}/{day_folder_name}")
                    self._logged_reuse_folders.add(folder_key)
            
            # Determine new filename with progressive number
            base_filename = f"{date.strftime('%Y_%m_%d')}_{topic}"
            
            counter = 1
            while True:
                new_filename = f"{base_filename}_{counter:02d}{ext}"
                destination_path = os.path.join(destination_folder, new_filename)
                if not os.path.exists(destination_path):
                    break
                counter += 1
                if counter > 9999:  # Safety limit
                    raise ValueError("Too many files with same name")
            
            # Perform operation with better error handling
            try:
                if move_files:
                    shutil.move(source_path, destination_path)
                    self.undo_log.append({"original": source_path, "destination": destination_path})
                else:
                    shutil.copy2(source_path, destination_path)  # copy2 preserves metadata
                
                self.log_and_callback("info", f"Processed: {os.path.basename(source_path)} -> {new_filename}")
                
                # V3 Enhancement: Save to database
                self._save_to_database(source_path, destination_path, date, topic)
                
            except (IOError, OSError, PermissionError) as e:
                raise Exception(f"File operation failed: {e}")
            
        except Exception as e:
            self.log_and_callback("error", f"Error processing {os.path.basename(source_path)}: {e}")
            # Don't re-raise to allow other files to be processed
            # raise

    def check_write_permissions(self, path: str) -> bool:
        """Check write permissions with improved error handling"""
        try:
            os.makedirs(path, exist_ok=True)
            test_file = os.path.join(path, ".test_write_permission.tmp")
            with open(test_file, 'w') as f:
                f.write("test")
            os.remove(test_file)
            return True
        except (IOError, OSError, PermissionError) as e:
            self.log_and_callback("error", f"Insufficient permissions to write to '{path}': {e}")
            return False

    def check_disk_space(self, sd_path, pictures_path, min_free_gb):
        """Check disk space with improved calculation"""
        try:
            total_size_to_move = 0
            for root, _, files in os.walk(sd_path):
                for name in files:
                    try:
                        file_path = os.path.join(root, name)
                        if os.path.isfile(file_path):
                            total_size_to_move += os.path.getsize(file_path)
                    except (OSError, FileNotFoundError):
                        continue
            
            disk_usage = psutil.disk_usage(pictures_path)
            free_space_destination_gb = disk_usage.free / (1024**3)
            required_space_gb = (total_size_to_move / (1024**3)) + min_free_gb
            
            self.log_and_callback("info", f"Space check: Required ~{required_space_gb:.2f} GB, Available {free_space_destination_gb:.2f} GB")
            
            if free_space_destination_gb < required_space_gb:
                self.log_and_callback("error", f"Insufficient disk space. Required: ~{required_space_gb:.2f} GB, Available: {free_space_destination_gb:.2f} GB.")
                return False
            return True
        except Exception as e:
            self.log_and_callback("error", f"Could not check disk space: {e}")
            return False

    def get_date_taken(self, file_path):
        """Extract date from EXIF or file modification time - FIXED VERSION"""
        try:
            # Try to get EXIF data using modern Pillow API
            with Image.open(file_path) as img:
                exif_data = img.getexif()
                if exif_data:
                    # Look for DateTimeOriginal (36867) or DateTime (306)
                    for tag_id in [36867, 306]:
                        if tag_id in exif_data:
                            date_str = exif_data[tag_id]
                            try:
                                return datetime.datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
                            except ValueError:
                                continue
        except Exception:
            pass
        
        # Fallback to file modification time
        try:
            mtime = os.path.getmtime(file_path)
            return datetime.datetime.fromtimestamp(mtime)
        except Exception as e:
            self.log_and_callback("warning", f"Could not get date for {os.path.basename(file_path)}: {e}")
            return datetime.datetime.now()

    def save_undo_log(self):
        """Save undo log with improved error handling"""
        if not self.undo_log:
            return
        
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            undo_filename = f"undo_log_{self.brand_name}_{timestamp}.json"
            undo_filepath = os.path.join(self.logs_path, undo_filename)
            
            with open(undo_filepath, 'w', encoding='utf-8') as f:
                json.dump(self.undo_log, f, indent=2, ensure_ascii=False)
            
            self.last_undo_log_path = undo_filepath
            self.log_and_callback("info", f"Undo log saved: {undo_filepath}")
        except Exception as e:
            self.log_and_callback("error", f"Failed to save undo log: {e}")

    def undo_last_operation(self, undo_log_path):
        """Undo last operation with improved error handling"""
        try:
            if not os.path.exists(undo_log_path):
                self.log_and_callback("error", f"Undo log file not found: {undo_log_path}")
                return False
            
            with open(undo_log_path, 'r', encoding='utf-8') as f:
                undo_data = json.load(f)
            
            if not undo_data:
                self.log_and_callback("info", "Undo log is empty.")
                return True
            
            total = len(undo_data)
            restored_count = 0
            failed_count = 0
            
            for entry in reversed(undo_data):
                original_path = entry.get('original')
                destination_path = entry.get('destination')
                
                if not original_path or not destination_path:
                    continue
                
                try:
                    if os.path.exists(destination_path):
                        # Ensure original directory exists
                        os.makedirs(os.path.dirname(original_path), exist_ok=True)
                        shutil.move(destination_path, original_path)
                        restored_count += 1
                        self.log_and_callback("info", f"Restored: {os.path.basename(original_path)}")
                    else:
                        self.log_and_callback("warning", f"File not found: {destination_path}")
                        failed_count += 1
                except Exception as e:
                    self.log_and_callback("error", f"Failed to restore {os.path.basename(original_path)}: {e}")
                    failed_count += 1
            
            self.log_and_callback("info", f"Undo completed. Restored: {restored_count}, Failed: {failed_count}, Total: {total}")
            return True
        except Exception as e:
            self.log_and_callback("error", f"Failed to perform undo: {e}")
            return False


class PhotoOrganizer(SDOrganizerBase):
    """
    Main PhotoOrganizer class implementing the SD organization logic.
    Inherits from SDOrganizerBase with all fixes applied.
    """
    pass

    def _save_to_database(self, source_path: str, destination_path: str, date: datetime.datetime, event_name: str = None):
        """
        Save photo metadata to database
        V3 Enhancement: Database integration
        """
        if not self.database:
            return
        
        try:
            # Extract comprehensive EXIF data
            photo_data = {
                'filepath': destination_path,
                'filename': os.path.basename(destination_path),
                'file_extension': os.path.splitext(destination_path)[1].lower(),
                'file_size': os.path.getsize(destination_path) if os.path.exists(destination_path) else 0,
                'date_taken': date.isoformat() if date else None,
                'event_name': event_name
            }
            
            # Try to extract detailed EXIF
            try:
                with Image.open(destination_path) as img:
                    exif = img.getexif()
                    
                    if exif:
                        # Camera info
                        photo_data['camera_make'] = exif.get(271)  # Make
                        photo_data['camera_model'] = exif.get(272)  # Model
                        photo_data['lens_model'] = exif.get(42036)  # LensModel
                        
                        # Exposure settings
                        photo_data['iso'] = exif.get(34855)  # ISOSpeedRatings
                        
                        # Aperture
                        aperture = exif.get(33437)  # FNumber
                        if aperture:
                            try:
                                if isinstance(aperture, tuple):
                                    photo_data['aperture'] = f"f/{aperture[0]/aperture[1]:.1f}"
                                else:
                                    photo_data['aperture'] = f"f/{float(aperture):.1f}"
                            except:
                                pass
                        
                        # Shutter speed
                        shutter = exif.get(33434)  # ExposureTime
                        if shutter:
                            try:
                                if isinstance(shutter, tuple):
                                    if shutter[0] < shutter[1]:
                                        photo_data['shutter_speed'] = f"1/{int(shutter[1]/shutter[0])}"
                                    else:
                                        photo_data['shutter_speed'] = f"{shutter[0]/shutter[1]:.2f}s"
                                else:
                                    photo_data['shutter_speed'] = f"{float(shutter):.2f}s"
                            except:
                                pass
                        
                        # Focal length
                        focal = exif.get(37386)  # FocalLength
                        if focal:
                            try:
                                if isinstance(focal, tuple):
                                    photo_data['focal_length'] = f"{focal[0]/focal[1]:.0f}mm"
                                else:
                                    photo_data['focal_length'] = f"{float(focal):.0f}mm"
                            except:
                                pass
                        
                        # GPS data
                        gps_info = exif.get(34853)
                        if gps_info and isinstance(gps_info, dict):
                            try:
                                # Latitude
                                lat = gps_info.get(2)
                                lat_ref = gps_info.get(1)
                                if lat and lat_ref:
                                    lat_decimal = lat[0] + lat[1]/60 + lat[2]/3600
                                    if lat_ref == 'S':
                                        lat_decimal = -lat_decimal
                                    photo_data['gps_latitude'] = lat_decimal
                                
                                # Longitude
                                lon = gps_info.get(4)
                                lon_ref = gps_info.get(3)
                                if lon and lon_ref:
                                    lon_decimal = lon[0] + lon[1]/60 + lon[2]/3600
                                    if lon_ref == 'W':
                                        lon_decimal = -lon_decimal
                                    photo_data['gps_longitude'] = lon_decimal
                                
                                # Altitude
                                alt = gps_info.get(6)
                                if alt:
                                    photo_data['gps_altitude'] = float(alt)
                            except:
                                pass
                        
                        # Image dimensions
                        photo_data['width'] = img.width
                        photo_data['height'] = img.height
                        photo_data['orientation'] = exif.get(274)  # Orientation
                        
                        # Store complete EXIF as JSON
                        exif_dict = {TAGS.get(k, k): str(v) for k, v in exif.items() if k in TAGS}
                        photo_data['exif_json'] = exif_dict
                        
            except Exception as e:
                self.log_and_callback("debug", f"Could not extract detailed EXIF: {e}")
            
            # Save to database
            photo_id = self.database.add_photo(photo_data)
            if photo_id > 0:
                self.log_and_callback("debug", f"Saved to database: {photo_data['filename']} (ID: {photo_id})")
            
        except Exception as e:
            self.log_and_callback("warning", f"Error saving to database: {e}")

