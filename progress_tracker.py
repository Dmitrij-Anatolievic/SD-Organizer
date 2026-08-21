"""
Progress Tracker Module - Track progress and estimate time remaining
Provides accurate ETA calculations for long operations
"""
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from collections import deque


class ProgressTracker:
    """
    Track operation progress and estimate time remaining.
    Uses moving average for smooth ETA calculations.
    """
    
    def __init__(self, total_items: int, window_size: int = 50):
        """
        Initialize progress tracker.
        
        Args:
            total_items: Total number of items to process
            window_size: Number of recent samples to use for moving average
        """
        self.total_items = total_items
        self.processed_items = 0
        self.start_time = time.time()
        self.last_update_time = self.start_time
        
        # Moving average window for smoother ETA
        self.window_size = window_size
        self.time_per_item_window = deque(maxlen=window_size)
        
        # Statistics
        self.bytes_processed = 0
        self.total_bytes = 0
        self.current_item_name = None
    
    def update(self, processed: int, current_item: Optional[str] = None,
              bytes_processed: Optional[int] = None):
        """
        Update progress.
        
        Args:
            processed: Number of items processed so far
            current_item: Name of current item being processed
            bytes_processed: Optional bytes processed (for file operations)
        """
        now = time.time()
        
        # Calculate time per item for this update
        if self.processed_items > 0 and processed > self.processed_items:
            items_delta = processed - self.processed_items
            time_delta = now - self.last_update_time
            time_per_item = time_delta / items_delta
            self.time_per_item_window.append(time_per_item)
        
        self.processed_items = processed
        self.current_item_name = current_item
        self.last_update_time = now
        
        if bytes_processed is not None:
            self.bytes_processed = bytes_processed
    
    def increment(self, current_item: Optional[str] = None,
                 bytes_added: Optional[int] = None):
        """
        Increment processed count by 1.
        
        Args:
            current_item: Name of item just processed
            bytes_added: Optional bytes added in this operation
        """
        self.processed_items += 1
        self.current_item_name = current_item
        self.last_update_time = time.time()
        
        # Add to moving average window
        if self.processed_items > 1:
            elapsed = time.time() - self.start_time
            avg_time = elapsed / self.processed_items
            self.time_per_item_window.append(avg_time)
        
        if bytes_added is not None:
            self.bytes_processed += bytes_added
    
    def set_total_bytes(self, total_bytes: int):
        """
        Set total bytes to process (for file operations).
        
        Args:
            total_bytes: Total size in bytes
        """
        self.total_bytes = total_bytes
    
    def get_progress_percent(self) -> float:
        """
        Get progress as percentage.
        
        Returns:
            Progress percentage (0-100)
        """
        if self.total_items == 0:
            return 0.0
        return (self.processed_items / self.total_items) * 100
    
    def get_elapsed_time(self) -> float:
        """
        Get elapsed time in seconds.
        
        Returns:
            Elapsed time in seconds
        """
        return time.time() - self.start_time
    
    def get_elapsed_time_formatted(self) -> str:
        """
        Get elapsed time as formatted string.
        
        Returns:
            Formatted time string (e.g., "1h 23m 45s")
        """
        return self._format_seconds(self.get_elapsed_time())
    
    def get_eta_seconds(self) -> Optional[float]:
        """
        Get estimated time remaining in seconds.
        
        Returns:
            ETA in seconds, or None if cannot estimate
        """
        if self.processed_items == 0:
            return None
        
        remaining_items = self.total_items - self.processed_items
        if remaining_items <= 0:
            return 0
        
        # Use moving average if available, otherwise use overall average
        if len(self.time_per_item_window) > 0:
            avg_time_per_item = sum(self.time_per_item_window) / len(self.time_per_item_window)
        else:
            elapsed = self.get_elapsed_time()
            avg_time_per_item = elapsed / self.processed_items
        
        eta = remaining_items * avg_time_per_item
        return eta
    
    def get_eta_formatted(self) -> str:
        """
        Get ETA as formatted string.
        
        Returns:
            Formatted ETA string (e.g., "2m 15s remaining")
        """
        eta = self.get_eta_seconds()
        if eta is None:
            return "Calculating..."
        
        if eta < 1:
            return "< 1s remaining"
        
        return f"{self._format_seconds(eta)} remaining"
    
    def get_completion_time(self) -> Optional[datetime]:
        """
        Get estimated completion time.
        
        Returns:
            Datetime when operation will complete, or None
        """
        eta = self.get_eta_seconds()
        if eta is None:
            return None
        
        return datetime.now() + timedelta(seconds=eta)
    
    def get_speed(self) -> Optional[float]:
        """
        Get processing speed (items per second).
        
        Returns:
            Items per second, or None if cannot calculate
        """
        elapsed = self.get_elapsed_time()
        if elapsed == 0 or self.processed_items == 0:
            return None
        
        return self.processed_items / elapsed
    
    def get_speed_formatted(self) -> str:
        """
        Get speed as formatted string.
        
        Returns:
            Formatted speed string (e.g., "25.3 items/sec")
        """
        speed = self.get_speed()
        if speed is None:
            return "N/A"
        
        if speed < 1:
            return f"{speed:.2f} items/sec"
        return f"{speed:.1f} items/sec"
    
    def get_bytes_speed(self) -> Optional[float]:
        """
        Get byte processing speed (bytes per second).
        
        Returns:
            Bytes per second, or None if not tracking bytes
        """
        if self.bytes_processed == 0:
            return None
        
        elapsed = self.get_elapsed_time()
        if elapsed == 0:
            return None
        
        return self.bytes_processed / elapsed
    
    def get_bytes_speed_formatted(self) -> str:
        """
        Get byte speed as formatted string.
        
        Returns:
            Formatted speed (e.g., "5.2 MB/s")
        """
        speed = self.get_bytes_speed()
        if speed is None:
            return "N/A"
        
        return self._format_bytes_per_second(speed)
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get comprehensive progress summary.
        
        Returns:
            Dictionary with all progress information
        """
        return {
            'total_items': self.total_items,
            'processed_items': self.processed_items,
            'remaining_items': self.total_items - self.processed_items,
            'progress_percent': round(self.get_progress_percent(), 2),
            'elapsed_time': self.get_elapsed_time_formatted(),
            'eta': self.get_eta_formatted(),
            'completion_time': self.get_completion_time(),
            'speed': self.get_speed_formatted(),
            'current_item': self.current_item_name,
            'bytes_processed': self.bytes_processed,
            'total_bytes': self.total_bytes,
            'bytes_speed': self.get_bytes_speed_formatted()
        }
    
    def get_progress_bar(self, width: int = 50, fill_char: str = '█',
                        empty_char: str = '░') -> str:
        """
        Get text progress bar.
        
        Args:
            width: Width of progress bar in characters
            fill_char: Character for filled portion
            empty_char: Character for empty portion
            
        Returns:
            Progress bar string
        """
        percent = self.get_progress_percent()
        filled = int(width * percent / 100)
        empty = width - filled
        
        bar = fill_char * filled + empty_char * empty
        return f"[{bar}] {percent:.1f}%"
    
    def is_complete(self) -> bool:
        """
        Check if operation is complete.
        
        Returns:
            True if all items processed
        """
        return self.processed_items >= self.total_items
    
    def reset(self, total_items: Optional[int] = None):
        """
        Reset tracker for new operation.
        
        Args:
            total_items: Optional new total items count
        """
        if total_items is not None:
            self.total_items = total_items
        
        self.processed_items = 0
        self.start_time = time.time()
        self.last_update_time = self.start_time
        self.time_per_item_window.clear()
        self.bytes_processed = 0
        self.current_item_name = None
    
    @staticmethod
    def _format_seconds(seconds: float) -> str:
        """
        Format seconds as human-readable string.
        
        Args:
            seconds: Number of seconds
            
        Returns:
            Formatted string (e.g., "1h 23m 45s")
        """
        if seconds < 60:
            return f"{int(seconds)}s"
        
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        
        if minutes < 60:
            return f"{minutes}m {seconds}s"
        
        hours = minutes // 60
        minutes = minutes % 60
        
        return f"{hours}h {minutes}m {seconds}s"
    
    @staticmethod
    def _format_bytes_per_second(bytes_per_sec: float) -> str:
        """
        Format bytes per second as human-readable string.
        
        Args:
            bytes_per_sec: Bytes per second
            
        Returns:
            Formatted string (e.g., "5.2 MB/s")
        """
        if bytes_per_sec < 1024:
            return f"{bytes_per_sec:.1f} B/s"
        
        kb_per_sec = bytes_per_sec / 1024
        if kb_per_sec < 1024:
            return f"{kb_per_sec:.1f} KB/s"
        
        mb_per_sec = kb_per_sec / 1024
        if mb_per_sec < 1024:
            return f"{mb_per_sec:.1f} MB/s"
        
        gb_per_sec = mb_per_sec / 1024
        return f"{gb_per_sec:.1f} GB/s"
