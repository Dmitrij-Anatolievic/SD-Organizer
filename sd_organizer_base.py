import os
import shutil
import datetime
import logging
import psutil
from PIL import Image
from abc import ABC, abstractmethod
import json
import sys
from collections import defaultdict 

IS_WINDOWS = sys.platform == "win32"
if IS_WINDOWS:
    try:
        import wmi
    except ImportError:
        wmi = None
        print("Warning: 'wmi' library not found. Falling back to psutil for drive detection.")

class SDOrganizerBase(ABC):
    def __init__(self, brand_name, pictures_path=None, logs_path=None, log_to_gui_callback=None, config=None, app_config=None):
        self.brand_name = brand_name
        self.log_to_gui_callback = log_to_gui_callback # <--- CORREZIONE: Variabile corretta
        self.config = config
        self.app_config = app_config if app_config is not None else {}
        self.pictures_path = pictures_path
        self.logs_path = logs_path
        self.logger = self._setup_logging()
        self.undo_log = []
        self.last_undo_log_path = None

    def _setup_logging(self):
        log_filename = f"log_sposta_{self.brand_name}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        try:
            os.makedirs(self.logs_path, exist_ok=True)
            log_file_path = os.path.join(self.logs_path, log_filename)
        except OSError as e:
            self.log_and_callback("warning", f"Could not create log directory at '{self.logs_path}'. Using script folder. Error: {e}")
            self.logs_path = os.path.dirname(os.path.abspath(__file__))
            log_file_path = os.path.join(self.logs_path, log_filename)

        logger = logging.getLogger(f"{self.brand_name}SDOrganizer_{id(self)}")
        logger.setLevel(logging.INFO)
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(file_handler)
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(console_handler)
        return logger
    
    def log_and_callback(self, level, message):
        if not hasattr(self, 'logger') or self.logger is None:
            if self.log_to_gui_callback:
                self.log_to_gui_callback(f"{level.upper()}: {message}")
            return
            
        log_map = {"info": self.logger.info, "warning": self.logger.warning, "error": self.logger.error}
        log_func = log_map.get(level.lower(), self.logger.info)
        log_func(message)

        if self.log_to_gui_callback:
            self.log_to_gui_callback(f"{level.upper()}: {message}")

    def find_sd_card_path(self):
        self.log_and_callback("info", f"Searching for SD card with '{self.brand_name}' folders...")
        if not self.config:
            self.log_and_callback("error", "Configuration for this brand is missing.")
            return []

        folder_names = self.config.get("SD_FOLDER_NAMES_CANDIDATES") or self.config.get("SD_CARD_FOLDERS")
        if not folder_names:
            self.log_and_callback("warning", "No 'SD_FOLDER_NAMES_CANDIDATES' or 'SD_CARD_FOLDERS' in config. Cannot find SD card.")
            return []
            
        self.log_and_callback("info", f"Will search for folders: {', '.join(folder_names)}")
        
        scan_drives = set()
        if IS_WINDOWS and wmi:
            self.log_and_callback("info", "Using WMI for drive detection...")
            try:
                for disk in wmi.WMI().Win32_LogicalDisk(DriveType=2):
                    scan_drives.add(disk.DeviceID + "\\")
            except Exception as e:
                self.log_and_callback("warning", f"WMI query failed: {e}. Falling back to psutil.")
        
        self.log_and_callback("info", "Using psutil to scan for drives.")
        try:
            all_drives = psutil.disk_partitions()
            for d in all_drives:
                try:
                    # Safely handle d.opts which can be string or list
                    opts_str = ""
                    if isinstance(d.opts, str):
                        opts_str = d.opts.lower()
                    elif isinstance(d.opts, list):
                        opts_str = ",".join(d.opts).lower()
                    else:
                        opts_str = str(d.opts).lower()
                    
                    # Check for removable drives
                    if "removable" in opts_str:
                        scan_drives.add(d.mountpoint)
                    
                    # Check for SD card file systems
                    if d.fstype and d.fstype.lower() in ["exfat", "vfat", "fat32", "fat"]:
                        scan_drives.add(d.mountpoint)
                except (AttributeError, TypeError):
                    continue
            
            if not scan_drives:
                self.log_and_callback("warning", "No specific removable drives found. Scanning ALL drives as a fallback.")
                scan_drives.update(d.mountpoint for d in all_drives)
        except Exception as e:
            self.log_and_callback("error", f"Critical error during psutil drive scan: {e}")
            return []

        self.log_and_callback("info", f"Scanning {len(scan_drives)} candidate drives: {sorted(list(scan_drives))}")
        found_devices = []
        for drive_path in sorted(list(scan_drives)):
            try:
                dcim_path = os.path.join(drive_path, "DCIM")
                if not os.path.isdir(dcim_path):
                    continue
                for folder_name in folder_names:
                    candidate_path = os.path.join(dcim_path, folder_name)
                    if os.path.isdir(candidate_path):
                        self.log_and_callback("info", f"SUCCESS! Found compatible folder: {candidate_path}")
                        found_devices.append({'drive_path': drive_path, 'brand_folder': folder_name, 'full_path': candidate_path})
            except (PermissionError, FileNotFoundError):
                continue
            except Exception as e:
                self.log_and_callback("error", f"Unexpected error while checking {drive_path}: {e}")
        
        if not found_devices:
            self.log_and_callback("warning", "Scan complete. No compatible SD cards found.")
        return found_devices

    def organize_sd_files(self, sd_full_path, topic, move_files=True, progress_callback=None):
        self.log_and_callback("info", f"Starting organization: {sd_full_path}")
        self.undo_log = []

        if not self.check_write_permissions(self.pictures_path): return False
        min_free_gb = self.app_config.get("MIN_FREE_SPACE_GB", 5)
        if not self.check_disk_space(sd_full_path, self.pictures_path, min_free_gb): return False
        
        # --- 1. PRE-PROCESSING: GATHERING FILES AND METADATA ---
        files_to_process, supported_extensions = [], [] 
        if "FILE_DESTINATIONS" in self.config:
            supported_extensions.extend(self.config["FILE_DESTINATIONS"].keys())
        else:
            supported_extensions.extend(self.config.get("RAW_EXTENSIONS", []))
            supported_extensions.extend(self.config.get("JPEG_EXTENSIONS", []))
            supported_extensions.extend(self.config.get("VIDEO_EXTENSIONS", []))

        if not supported_extensions:
            self.log_and_callback("error", "No file extensions found in configuration.")
            return False

        for root, _, files in os.walk(sd_full_path):
            for file in files:
                if any(file.lower().endswith(ext.lower()) for ext in supported_extensions):
                    files_to_process.append(os.path.join(root, file))

        if not files_to_process:
            self.log_and_callback("warning", "No compatible files found to process.")
            return True

        total_files = len(files_to_process)
        self.log_and_callback("info", f"Found {total_files} files to process. Pre-processing to determine groups...")
        
        # Mappa per i nomi dei mesi
        mese_dict = {1:"Gennaio", 2:"Febbraio", 3:"Marzo", 4:"Aprile", 5:"Maggio", 6:"Giugno", 7:"Luglio", 8:"Agosto", 9:"Settembre", 10:"Ottobre", 11:"Novembre", 12:"Dicembre"}
        
        dest_root = self.config.get("DESTINATION_ROOT") or self.pictures_path
        
        # Raggruppa i file per Data e Percorso di Destinazione finale
        grouped_files = defaultdict(list)
        
        for source_path in files_to_process:
            try:
                date = self.get_date_taken(source_path)
                _, ext = os.path.splitext(source_path)
                ext_lower = ext.lower()
                
                # Determina la sottocartella di destinazione (immagini/raw, video, ecc.)
                subfolder = ""
                if "FILE_DESTINATIONS" in self.config:
                    subfolder = self.config["FILE_DESTINATIONS"].get(ext_lower, "")
                else:
                    ext_upper = ext.upper()
                    if ext_upper in self.config.get("RAW_EXTENSIONS", []): subfolder = os.path.join("Images", "RAW")
                    elif ext_upper in self.config.get("JPEG_EXTENSIONS", []): subfolder = os.path.join("Images", "JPEG")
                    elif ext_upper in self.config.get("VIDEO_EXTENSIONS", []): subfolder = "Videos"

                # --- NUOVA LOGICA: Struttura AAAA/Nome Mese/GG ---
                # Esempio: 2025/Settembre/17
                folder_structure = os.path.join(
                    str(date.year),
                    mese_dict.get(date.month, "Sconosciuto"),
                    f"{date.day:02d}"  # Giorno a due cifre: 01, 02, ..., 31
                )
                
                final_folder_path = os.path.join(dest_root, folder_structure, subfolder)
                
                # Chiave di raggruppamento: cartella finale + data di scatto
                group_key = (final_folder_path, date)
                
                grouped_files[group_key].append({
                    'source_path': source_path,
                    'date': date,
                    'ext': ext,
                    'final_folder_path': final_folder_path
                })
            except Exception as e:
                self.log_and_callback("error", f"Failed to pre-process file {source_path}: {e}")
        
        self.log_and_callback("info", f"File raggruppati in {len(grouped_files)} set. Inizio rinomina e spostamento/copia.")
        
        # --- 2. RENAME AND MOVE/COPY con numerazione progressiva ---
        processed_count = 0
        topic_name = topic.replace(" ", "_")
        
        for group_key, files_in_group in grouped_files.items():
            
            date = files_in_group[0]['date']
            final_folder_path = files_in_group[0]['final_folder_path']
            total_in_group = len(files_in_group)
            
            # Crea la cartella di destinazione. 'exist_ok=True' previene errori se la cartella esiste.
            os.makedirs(final_folder_path, exist_ok=True)
            
            # Prefisso Base: AAAA_MM_GG_ARGOMENTO
            base_name_prefix = date.strftime("%Y_%m_%d") + "_" + topic_name

            for index_in_group, file_data in enumerate(files_in_group):
                processed_count += 1
                source_path = file_data['source_path']
                ext = file_data['ext']
                
                # --- LOGICA DI RINEOMINA ---
                if total_in_group > 1:
                    # Multi-file: AAAA_MM_GG_ARGOMENTO_XX.EXT
                    counter = index_in_group + 1
                    new_filename_base = f"{base_name_prefix}_{counter:02d}"
                else:
                    # Singolo file: AAAA_MM_GG_ARGOMENTO.EXT
                    new_filename_base = base_name_prefix

                new_filename = new_filename_base + ext
                destination_path = os.path.join(final_folder_path, new_filename)
                
                destination_path = self._get_unique_filename(destination_path)
                
                try:
                    (shutil.move if move_files else shutil.copy)(source_path, destination_path)
                    if move_files: self.undo_log.append({"original": source_path, "destination": destination_path})
                    
                    if progress_callback:
                        progress_callback(int(processed_count / total_files * 100), os.path.basename(source_path))
                except Exception as e:
                    self.log_and_callback("error", f"Failed to process file {source_path}: {e}")
        
        if move_files: self.save_undo_log()
        self.log_and_callback("info", "Organization process finished.")
        return True

    def check_write_permissions(self, path):
        try:
            os.makedirs(path, exist_ok=True)
            test_file = os.path.join(path, "test_write.tmp")
            with open(test_file, 'w') as f: f.write("test")
            os.remove(test_file)
            return True
        except (IOError, OSError) as e:
            self.log_and_callback("error", f"Insufficient permissions to write to '{path}': {e}")
            return False

    def check_disk_space(self, sd_path, pictures_path, min_free_gb):
        try:
            total_size = sum(os.path.getsize(os.path.join(root, name)) for root, _, files in os.walk(sd_path) for name in files)
            free_space_gb = psutil.disk_usage(pictures_path).free / (1024**3)
            if free_space_gb < (total_size / (1024**3)) + min_free_gb:
                self.log_and_callback("error", f"Insufficient disk space on '{pictures_path}'.")
                return False
            return True
        except Exception as e:
            self.log_and_callback("error", f"Could not check disk space for '{pictures_path}': {e}")
            return False

    def get_date_taken(self, file_path):
        try:
            with Image.open(file_path) as img:
                exif_data = img._getexif()
                if exif_data:
                    date_str = exif_data.get(36867) or exif_data.get(306)
                    if date_str:
                        date_str = date_str.split(' ')[0]
                        year, month, day = map(int, date_str.replace('-', ':').split(':')[:3])
                        return datetime.date(year, month, day)
        except Exception: pass
        timestamp = os.path.getmtime(file_path)
        return datetime.date.fromtimestamp(timestamp)

    def save_undo_log(self):
        if not self.undo_log: return
        log_dir = os.path.join(self.logs_path, "undo_logs")
        try:
            os.makedirs(log_dir, exist_ok=True)
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            undo_log_file = os.path.join(log_dir, f"undo_log_{self.brand_name}_{timestamp}.json")
            with open(undo_log_file, "w") as f: json.dump(self.undo_log, f, indent=4)
            self.log_and_callback("info", f"Undo log saved to: {undo_log_file}")
            self.last_undo_log_path = undo_log_file
        except Exception as e:
            self.log_and_callback("error", f"Error saving undo log: {e}")

    @staticmethod
    def _get_unique_filename(destination_path):
        if not os.path.exists(destination_path): return destination_path
        base, ext = os.path.splitext(destination_path)
        counter = 1
        new_path = f"{base}_{counter}{ext}"
        while os.path.exists(new_path):
            counter += 1
            new_path = f"{base}_{counter}{ext}"
        return new_path

    @staticmethod
    def undo_last_operation(log_file_path, log_to_gui_callback):
        log_to_gui_callback("INFO: Starting undo operation...")
        if not os.path.exists(log_file_path):
            log_to_gui_callback(f"ERROR: Log file not found: {log_file_path}")
            return False
        try:
            with open(log_file_path, "r") as f: undo_log = json.load(f)
        except Exception as e:
            log_to_gui_callback(f"ERROR: Error reading log file: {e}")
            return False
        
        success = True
        for entry in reversed(undo_log):
            try:
                if os.path.exists(entry["destination"]):
                    os.makedirs(os.path.dirname(entry["original"]), exist_ok=True)
                    shutil.move(entry["destination"], entry["original"])
            except Exception as e:
                log_to_gui_callback(f"ERROR during undo of '{entry['destination']}': {e}")
                success = False
        log_to_gui_callback("INFO: Undo operation completed.")
        return success