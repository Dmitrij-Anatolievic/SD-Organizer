"""
Auto-Import Service Module
Monitors for SD card insertion and triggers automatic import
"""
import os
import time
import threading
import psutil
from typing import Callable, Dict, List, Optional
import logging
import json


class AutoImportService:
    """
    Service that monitors for removable drives and triggers automatic import
    """
    
    def __init__(self, 
                 check_interval: int = 5,
                 auto_import_callback: Callable = None):
        """
        Initialize auto-import service
        
        Args:
            check_interval: Seconds between drive checks
            auto_import_callback: Function to call when new SD detected
        """
        self.check_interval = check_interval
        self.auto_import_callback = auto_import_callback
        self.logger = logging.getLogger("AutoImportService")
        
        self.is_running = False
        self.monitor_thread = None
        self.known_drives = set()
        self.rules = []  # Auto-import rules
        
        # Load settings
        self.settings_path = os.path.join(
            os.path.expanduser("~"),
            ".sd_organizer",
            "auto_import_settings.json"
        )
        self._load_settings()
    
    def _load_settings(self):
        """Load auto-import settings from file"""
        try:
            if os.path.exists(self.settings_path):
                with open(self.settings_path, 'r') as f:
                    data = json.load(f)
                    self.rules = data.get('rules', [])
                    self.logger.info(f"Loaded {len(self.rules)} auto-import rules")
        except Exception as e:
            self.logger.error(f"Error loading auto-import settings: {e}")
    
    def _save_settings(self):
        """Save auto-import settings to file"""
        try:
            os.makedirs(os.path.dirname(self.settings_path), exist_ok=True)
            with open(self.settings_path, 'w') as f:
                json.dump({'rules': self.rules}, f, indent=2)
            self.logger.info("Saved auto-import settings")
        except Exception as e:
            self.logger.error(f"Error saving auto-import settings: {e}")
    
    def add_rule(self, rule: Dict):
        """
        Add auto-import rule
        
        Rule format:
        {
            'name': 'Rule name',
            'brand': 'Nikon',
            'destination': 'C:/Photos',
            'event_template': 'Event_{date}',
            'move_files': True,
            'enabled': True,
            'process_options': {
                'auto_rotate': True,
                'convert_raw': False,
                'create_web': False
            }
        }
        """
        self.rules.append(rule)
        self._save_settings()
        self.logger.info(f"Added auto-import rule: {rule.get('name')}")
    
    def remove_rule(self, rule_name: str):
        """Remove auto-import rule by name"""
        self.rules = [r for r in self.rules if r.get('name') != rule_name]
        self._save_settings()
    
    def get_rules(self) -> List[Dict]:
        """Get all auto-import rules"""
        return self.rules
    
    def start(self):
        """Start monitoring for SD cards"""
        if self.is_running:
            self.logger.warning("Auto-import service already running")
            return
        
        self.is_running = True
        self.known_drives = self._get_current_drives()
        
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        
        self.logger.info(f"Auto-import service started (checking every {self.check_interval}s)")
    
    def stop(self):
        """Stop monitoring"""
        self.is_running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        self.logger.info("Auto-import service stopped")
    
    def _get_current_drives(self) -> set:
        """Get set of currently mounted removable drives"""
        drives = set()
        
        try:
            partitions = psutil.disk_partitions(all=False)
            for partition in partitions:
                # Check if it's a removable drive
                if self._is_removable_drive(partition):
                    drives.add(partition.mountpoint)
        except Exception as e:
            self.logger.error(f"Error detecting drives: {e}")
        
        return drives
    
    def _is_removable_drive(self, partition) -> bool:
        """Check if partition is a removable drive"""
        import sys
        
        if sys.platform == "win32":
            # Windows: check for removable flag
            return 'removable' in partition.opts.lower()
        else:
            # Linux/Mac: check for media/mnt paths
            return '/media/' in partition.mountpoint or '/mnt/' in partition.mountpoint
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.is_running:
            try:
                current_drives = self._get_current_drives()
                
                # Detect new drives
                new_drives = current_drives - self.known_drives
                
                if new_drives:
                    self.logger.info(f"Detected {len(new_drives)} new drive(s)")
                    
                    for drive_path in new_drives:
                        self._handle_new_drive(drive_path)
                
                # Detect removed drives
                removed_drives = self.known_drives - current_drives
                if removed_drives:
                    self.logger.info(f"Detected {len(removed_drives)} removed drive(s)")
                
                self.known_drives = current_drives
                
            except Exception as e:
                self.logger.error(f"Error in monitor loop: {e}")
            
            time.sleep(self.check_interval)
    
    def _handle_new_drive(self, drive_path: str):
        """Handle newly detected drive"""
        self.logger.info(f"New drive detected: {drive_path}")
        
        # Wait a moment for drive to fully mount
        time.sleep(2)
        
        # Check if drive looks like a camera SD card
        if not self._looks_like_camera_sd(drive_path):
            self.logger.debug(f"{drive_path} doesn't look like a camera SD card")
            return
        
        # Find matching rule
        matching_rule = self._find_matching_rule(drive_path)
        
        if matching_rule and matching_rule.get('enabled', True):
            self.logger.info(f"Found matching rule: {matching_rule.get('name')}")
            
            # Trigger auto-import callback
            if self.auto_import_callback:
                try:
                    self.auto_import_callback(drive_path, matching_rule)
                except Exception as e:
                    self.logger.error(f"Error in auto-import callback: {e}")
        else:
            self.logger.info(f"No enabled rule found for {drive_path}, prompting user")
            
            # Trigger callback with no rule (will prompt user)
            if self.auto_import_callback:
                try:
                    self.auto_import_callback(drive_path, None)
                except Exception as e:
                    self.logger.error(f"Error in callback: {e}")
    
    def _looks_like_camera_sd(self, drive_path: str) -> bool:
        """Check if drive looks like a camera SD card"""
        try:
            # Check for common camera folders
            camera_indicators = [
                'DCIM',
                '100NIKON', '101NIKON', '103NZ_FC',
                '100CANON', '101CANON',
                '100_FUJI',
                '100MSDCF',  # Sony
                'PRIVATE',
                'MP_ROOT'  # Canon video
            ]
            
            # List root directory
            try:
                items = os.listdir(drive_path)
            except (PermissionError, OSError):
                return False
            
            # Check for camera folder indicators
            for item in items:
                if item.upper() in camera_indicators:
                    return True
            
            # Check for DCIM folder with subfolders
            dcim_path = os.path.join(drive_path, 'DCIM')
            if os.path.exists(dcim_path):
                try:
                    dcim_contents = os.listdir(dcim_path)
                    if dcim_contents:
                        return True
                except:
                    pass
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error checking if {drive_path} is camera SD: {e}")
            return False
    
    def _find_matching_rule(self, drive_path: str) -> Optional[Dict]:
        """Find auto-import rule matching the detected drive"""
        # For now, return first enabled rule
        # In future, could check drive volume name, brand-specific folders, etc.
        for rule in self.rules:
            if rule.get('enabled', True):
                return rule
        return None


class AutoImportSettings:
    """
    Manage auto-import configuration
    """
    
    def __init__(self):
        self.settings_dir = os.path.join(os.path.expanduser("~"), ".sd_organizer")
        self.settings_file = os.path.join(self.settings_dir, "auto_import_prefs.json")
        self.settings = self._load()
    
    def _load(self) -> Dict:
        """Load settings from file"""
        default_settings = {
            'enabled': False,
            'show_notification': True,
            'auto_start_import': False,  # If False, show prompt first
            'check_interval': 5,
            'last_used_brand': None,
            'last_used_destination': None,
            'last_used_event': None
        }
        
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    loaded = json.load(f)
                    default_settings.update(loaded)
        except Exception as e:
            logging.error(f"Error loading auto-import settings: {e}")
        
        return default_settings
    
    def save(self):
        """Save settings to file"""
        try:
            os.makedirs(self.settings_dir, exist_ok=True)
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            logging.error(f"Error saving auto-import settings: {e}")
    
    def get(self, key: str, default=None):
        """Get setting value"""
        return self.settings.get(key, default)
    
    def set(self, key: str, value):
        """Set setting value"""
        self.settings[key] = value
        self.save()
    
    def is_enabled(self) -> bool:
        """Check if auto-import is enabled"""
        return self.settings.get('enabled', False)
    
    def enable(self):
        """Enable auto-import"""
        self.set('enabled', True)
    
    def disable(self):
        """Disable auto-import"""
        self.set('enabled', False)


class ImportNotification:
    """
    Notification system for auto-import events
    """
    
    @staticmethod
    def notify_sd_detected(drive_path: str, callback: Callable = None):
        """
        Show notification that SD card was detected
        
        Args:
            drive_path: Path to detected drive
            callback: Optional callback when user clicks notification
        """
        try:
            # Try to use system notifications if available
            import subprocess
            import sys
            
            title = "SD Card Detected"
            message = f"SD card detected at {drive_path}. Click to import photos."
            
            if sys.platform == "win32":
                # Windows notification (requires win10toast)
                try:
                    from win10toast import ToastNotifier
                    toaster = ToastNotifier()
                    toaster.show_toast(
                        title,
                        message,
                        duration=10,
                        threaded=True,
                        callback_on_click=callback
                    )
                except ImportError:
                    logging.warning("win10toast not installed, skipping notification")
            
            elif sys.platform == "darwin":
                # macOS notification
                subprocess.run([
                    'osascript', '-e',
                    f'display notification "{message}" with title "{title}"'
                ])
            
            elif sys.platform.startswith("linux"):
                # Linux notification (requires notify-send)
                try:
                    subprocess.run(['notify-send', title, message])
                except FileNotFoundError:
                    logging.warning("notify-send not installed, skipping notification")
            
        except Exception as e:
            logging.error(f"Error showing notification: {e}")
    
    @staticmethod
    def notify_import_complete(files_imported: int, destination: str):
        """Notify that import is complete"""
        try:
            import subprocess
            import sys
            
            title = "Import Complete"
            message = f"Successfully imported {files_imported} files to {destination}"
            
            if sys.platform == "win32":
                try:
                    from win10toast import ToastNotifier
                    toaster = ToastNotifier()
                    toaster.show_toast(title, message, duration=5, threaded=True)
                except ImportError:
                    pass
            
            elif sys.platform == "darwin":
                subprocess.run([
                    'osascript', '-e',
                    f'display notification "{message}" with title "{title}"'
                ])
            
            elif sys.platform.startswith("linux"):
                try:
                    subprocess.run(['notify-send', title, message])
                except FileNotFoundError:
                    pass
        
        except Exception as e:
            logging.error(f"Error showing notification: {e}")
