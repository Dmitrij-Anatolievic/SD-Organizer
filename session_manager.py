"""
Session Manager Module - Auto-save and restore session state
Allows resuming interrupted operations
"""
import os
import json
from datetime import datetime
from typing import Optional, Dict, Any


class SessionManager:
    """
    Manages session state with auto-save functionality.
    Allows resuming interrupted operations.
    """
    
    def __init__(self, session_file: str = None):
        """
        Initialize session manager.
        
        Args:
            session_file: Path to session file. Defaults to ~/.sd_organizer_session.json
        """
        if session_file is None:
            session_file = os.path.expanduser("~/.sd_organizer_session.json")
        
        self.session_file = session_file
        self.state = {}
        self._load_session()
    
    def _load_session(self):
        """Load session from disk"""
        if os.path.exists(self.session_file):
            try:
                with open(self.session_file, 'r', encoding='utf-8') as f:
                    self.state = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load session: {e}")
                self.state = {}
        else:
            self.state = {}
    
    def save_session(self, state: Dict[str, Any] = None):
        """
        Save current session state to disk.
        
        Args:
            state: State dictionary to save. If None, saves current state.
        """
        if state is not None:
            self.state.update(state)
        
        # Add timestamp
        self.state['last_saved'] = datetime.now().isoformat()
        
        try:
            # Ensure directory exists
            session_dir = os.path.dirname(self.session_file)
            if session_dir:
                os.makedirs(session_dir, exist_ok=True)
            
            # Save with atomic write (write to temp, then rename)
            temp_file = self.session_file + '.tmp'
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(self.state, f, indent=2, ensure_ascii=False)
            
            # Atomic rename
            if os.path.exists(self.session_file):
                os.remove(self.session_file)
            os.rename(temp_file, self.session_file)
            
        except (IOError, OSError) as e:
            print(f"Warning: Could not save session: {e}")
    
    def update_progress(self, files_processed: int, total_files: int,
                       current_file: Optional[str] = None):
        """
        Update progress information in session.
        
        Args:
            files_processed: Number of files processed so far
            total_files: Total number of files to process
            current_file: Current file being processed
        """
        self.state['progress'] = {
            'files_processed': files_processed,
            'total_files': total_files,
            'current_file': current_file,
            'percent_complete': round((files_processed / total_files * 100) if total_files > 0 else 0, 2),
            'timestamp': datetime.now().isoformat()
        }
        self.save_session()
    
    def set_operation_info(self, operation_type: str, sd_path: str,
                          destination: str, topic: str = None):
        """
        Set information about current operation.
        
        Args:
            operation_type: Type of operation ('copy' or 'move')
            sd_path: Source SD card path
            destination: Destination path
            topic: Optional topic/event name
        """
        self.state['operation'] = {
            'type': operation_type,
            'sd_path': sd_path,
            'destination': destination,
            'topic': topic,
            'started_at': datetime.now().isoformat()
        }
        self.save_session()
    
    def add_processed_file(self, source: str, destination: str):
        """
        Record a successfully processed file.
        
        Args:
            source: Source file path
            destination: Destination file path
        """
        if 'processed_files' not in self.state:
            self.state['processed_files'] = []
        
        self.state['processed_files'].append({
            'source': source,
            'destination': destination,
            'timestamp': datetime.now().isoformat()
        })
    
    def mark_completed(self, success: bool = True):
        """
        Mark operation as completed.
        
        Args:
            success: Whether operation completed successfully
        """
        self.state['completed'] = True
        self.state['success'] = success
        self.state['completed_at'] = datetime.now().isoformat()
        self.save_session()
    
    def has_incomplete_session(self) -> bool:
        """
        Check if there's an incomplete session.
        
        Returns:
            True if incomplete session exists
        """
        if not self.state:
            return False
        
        if self.state.get('completed'):
            return False
        
        # Check if session has required info
        if 'operation' not in self.state:
            return False
        
        return True
    
    def get_resume_info(self) -> Optional[Dict[str, Any]]:
        """
        Get information needed to resume interrupted session.
        
        Returns:
            Dictionary with resume info, or None if no session to resume
        """
        if not self.has_incomplete_session():
            return None
        
        progress = self.state.get('progress', {})
        operation = self.state.get('operation', {})
        
        return {
            'operation_type': operation.get('type'),
            'sd_path': operation.get('sd_path'),
            'destination': operation.get('destination'),
            'topic': operation.get('topic'),
            'files_processed': progress.get('files_processed', 0),
            'total_files': progress.get('total_files', 0),
            'processed_files': self.state.get('processed_files', []),
            'started_at': operation.get('started_at'),
            'last_saved': self.state.get('last_saved')
        }
    
    def clear_session(self):
        """Clear session and delete session file"""
        self.state = {}
        if os.path.exists(self.session_file):
            try:
                os.remove(self.session_file)
            except OSError as e:
                print(f"Warning: Could not delete session file: {e}")
    
    def get_state(self) -> Dict[str, Any]:
        """
        Get current session state.
        
        Returns:
            Copy of current state dictionary
        """
        return self.state.copy()
    
    def create_backup(self, backup_path: str = None):
        """
        Create backup of current session.
        
        Args:
            backup_path: Path for backup file. Defaults to session_file + .backup
        """
        if backup_path is None:
            backup_path = self.session_file + '.backup'
        
        try:
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(self.state, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Warning: Could not create session backup: {e}")
    
    def restore_from_backup(self, backup_path: str = None) -> bool:
        """
        Restore session from backup.
        
        Args:
            backup_path: Path to backup file. Defaults to session_file + .backup
            
        Returns:
            True if restored successfully
        """
        if backup_path is None:
            backup_path = self.session_file + '.backup'
        
        if not os.path.exists(backup_path):
            return False
        
        try:
            with open(backup_path, 'r', encoding='utf-8') as f:
                self.state = json.load(f)
            return True
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not restore from backup: {e}")
            return False
    
    def get_session_age_seconds(self) -> Optional[float]:
        """
        Get age of current session in seconds.
        
        Returns:
            Age in seconds, or None if no session
        """
        if not self.state or 'last_saved' not in self.state:
            return None
        
        try:
            last_saved = datetime.fromisoformat(self.state['last_saved'])
            now = datetime.now()
            age = (now - last_saved).total_seconds()
            return age
        except (ValueError, KeyError):
            return None
    
    def is_session_stale(self, max_age_hours: int = 24) -> bool:
        """
        Check if session is stale (too old).
        
        Args:
            max_age_hours: Maximum age in hours
            
        Returns:
            True if session is older than max_age_hours
        """
        age = self.get_session_age_seconds()
        if age is None:
            return False
        
        max_age_seconds = max_age_hours * 3600
        return age > max_age_seconds
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if exc_type is None:
            # No exception - mark as completed
            self.mark_completed(success=True)
        else:
            # Exception occurred - save state but don't mark as completed
            self.save_session()
        return False
