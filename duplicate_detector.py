"""
Duplicate Detector Module - Find and manage duplicate files
Uses MD5 hashing for accurate duplicate detection
"""
import os
import hashlib
from collections import defaultdict
from typing import Dict, List, Tuple, Callable, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed


class DuplicateDetector:
    """
    Detect duplicate files by content (MD5 hash).
    Can handle large file sets efficiently.
    """
    
    def __init__(self, progress_callback: Optional[Callable] = None):
        """
        Initialize duplicate detector.
        
        Args:
            progress_callback: Optional callback for progress updates (current, total, filename)
        """
        self.progress_callback = progress_callback
        self.duplicates = {}
        
    def calculate_file_hash(self, file_path: str, chunk_size: int = 8192) -> Optional[str]:
        """
        Calculate MD5 hash of file.
        
        Args:
            file_path: Path to file
            chunk_size: Size of chunks to read
            
        Returns:
            MD5 hash as hex string, or None if error
        """
        try:
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(chunk_size), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except (IOError, OSError) as e:
            print(f"Error hashing {file_path}: {e}")
            return None
    
    def _quick_check_duplicate(self, file1: str, file2: str) -> bool:
        """
        Quick check if two files might be duplicates (size comparison).
        
        Args:
            file1: First file path
            file2: Second file path
            
        Returns:
            True if files have same size
        """
        try:
            size1 = os.path.getsize(file1)
            size2 = os.path.getsize(file2)
            return size1 == size2
        except OSError:
            return False
    
    def find_duplicates(self, file_paths: List[str], 
                       use_parallel: bool = True,
                       max_workers: int = 4) -> Dict[str, List[str]]:
        """
        Find duplicate files in the given list.
        
        Args:
            file_paths: List of file paths to check
            use_parallel: Use parallel processing
            max_workers: Number of parallel workers
            
        Returns:
            Dictionary mapping hash to list of duplicate file paths
        """
        if not file_paths:
            return {}
        
        # Group files by size first (quick pre-filter)
        size_groups = defaultdict(list)
        for file_path in file_paths:
            try:
                size = os.path.getsize(file_path)
                size_groups[size].append(file_path)
            except OSError:
                continue
        
        # Only check files that have the same size as another file
        candidates = []
        for size, files in size_groups.items():
            if len(files) > 1:
                candidates.extend(files)
        
        if not candidates:
            return {}
        
        # Calculate hashes
        hash_map = defaultdict(list)
        total = len(candidates)
        
        if use_parallel and total > 10:
            # Parallel processing for large sets
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                future_to_file = {
                    executor.submit(self.calculate_file_hash, file_path): file_path
                    for file_path in candidates
                }
                
                completed = 0
                for future in as_completed(future_to_file):
                    file_path = future_to_file[future]
                    try:
                        file_hash = future.result()
                        if file_hash:
                            hash_map[file_hash].append(file_path)
                        
                        completed += 1
                        if self.progress_callback:
                            self.progress_callback(completed, total, os.path.basename(file_path))
                    except Exception as e:
                        print(f"Error processing {file_path}: {e}")
        else:
            # Sequential processing for small sets
            for i, file_path in enumerate(candidates):
                file_hash = self.calculate_file_hash(file_path)
                if file_hash:
                    hash_map[file_hash].append(file_path)
                
                if self.progress_callback:
                    self.progress_callback(i + 1, total, os.path.basename(file_path))
        
        # Filter to only include actual duplicates (hash appears multiple times)
        duplicates = {
            file_hash: paths 
            for file_hash, paths in hash_map.items() 
            if len(paths) > 1
        }
        
        self.duplicates = duplicates
        return duplicates
    
    def get_duplicate_groups(self) -> List[List[str]]:
        """
        Get duplicate files grouped by content.
        
        Returns:
            List of groups, where each group is a list of duplicate file paths
        """
        return list(self.duplicates.values())
    
    def get_statistics(self) -> Dict[str, int]:
        """
        Get duplicate detection statistics.
        
        Returns:
            Dictionary with statistics
        """
        num_groups = len(self.duplicates)
        total_duplicates = sum(len(paths) - 1 for paths in self.duplicates.values())
        
        # Calculate wasted space
        wasted_space = 0
        for paths in self.duplicates.values():
            if paths:
                # Size of one file * (number of copies - 1)
                try:
                    file_size = os.path.getsize(paths[0])
                    wasted_space += file_size * (len(paths) - 1)
                except OSError:
                    pass
        
        return {
            'duplicate_groups': num_groups,
            'total_duplicate_files': total_duplicates,
            'wasted_space_bytes': wasted_space,
            'wasted_space_mb': round(wasted_space / (1024 * 1024), 2),
            'wasted_space_gb': round(wasted_space / (1024 * 1024 * 1024), 2)
        }
    
    def suggest_files_to_remove(self, keep_strategy: str = 'first') -> List[str]:
        """
        Suggest which duplicate files to remove.
        
        Args:
            keep_strategy: Strategy for which file to keep:
                - 'first': Keep first file in list
                - 'newest': Keep newest file (by mtime)
                - 'oldest': Keep oldest file (by mtime)
                - 'shortest_path': Keep file with shortest path
                
        Returns:
            List of file paths that can be removed
        """
        to_remove = []
        
        for paths in self.duplicates.values():
            if len(paths) <= 1:
                continue
            
            if keep_strategy == 'first':
                # Keep first, remove rest
                to_remove.extend(paths[1:])
            
            elif keep_strategy == 'newest':
                # Keep newest, remove rest
                sorted_paths = sorted(paths, key=lambda p: os.path.getmtime(p), reverse=True)
                to_remove.extend(sorted_paths[1:])
            
            elif keep_strategy == 'oldest':
                # Keep oldest, remove rest
                sorted_paths = sorted(paths, key=lambda p: os.path.getmtime(p))
                to_remove.extend(sorted_paths[1:])
            
            elif keep_strategy == 'shortest_path':
                # Keep file with shortest path
                sorted_paths = sorted(paths, key=lambda p: len(p))
                to_remove.extend(sorted_paths[1:])
        
        return to_remove
    
    def remove_duplicates(self, files_to_remove: List[str], 
                         dry_run: bool = True) -> Tuple[int, int]:
        """
        Remove duplicate files.
        
        Args:
            files_to_remove: List of file paths to remove
            dry_run: If True, don't actually delete files
            
        Returns:
            Tuple of (number of files removed, number of errors)
        """
        removed = 0
        errors = 0
        
        for file_path in files_to_remove:
            try:
                if not dry_run:
                    os.remove(file_path)
                removed += 1
            except OSError as e:
                print(f"Error removing {file_path}: {e}")
                errors += 1
        
        return removed, errors
    
    def create_report(self, output_file: str = None) -> str:
        """
        Create a detailed duplicate report.
        
        Args:
            output_file: Optional file to save report to
            
        Returns:
            Report as string
        """
        stats = self.get_statistics()
        
        lines = []
        lines.append("=" * 70)
        lines.append("DUPLICATE FILES REPORT")
        lines.append("=" * 70)
        lines.append(f"Duplicate Groups: {stats['duplicate_groups']}")
        lines.append(f"Total Duplicate Files: {stats['total_duplicate_files']}")
        lines.append(f"Wasted Space: {stats['wasted_space_mb']} MB ({stats['wasted_space_gb']} GB)")
        lines.append("")
        lines.append("DUPLICATE GROUPS:")
        lines.append("-" * 70)
        
        for i, (file_hash, paths) in enumerate(self.duplicates.items(), 1):
            lines.append(f"\nGroup {i} (Hash: {file_hash[:8]}...):")
            lines.append(f"  Files: {len(paths)}")
            try:
                size = os.path.getsize(paths[0])
                size_mb = size / (1024 * 1024)
                lines.append(f"  Size: {size_mb:.2f} MB each")
            except OSError:
                pass
            
            for path in paths:
                lines.append(f"    - {path}")
        
        lines.append("")
        lines.append("=" * 70)
        
        report = "\n".join(lines)
        
        if output_file:
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(report)
            except IOError as e:
                print(f"Error saving report: {e}")
        
        return report


def find_duplicates_simple(file_paths: List[str]) -> Dict[str, List[str]]:
    """
    Simple function to find duplicates without progress tracking.
    
    Args:
        file_paths: List of file paths to check
        
    Returns:
        Dictionary mapping hash to list of duplicate file paths
    """
    detector = DuplicateDetector()
    return detector.find_duplicates(file_paths)
