"""
Integrity Verifier Module - Verify file copy integrity
Ensures files are copied correctly without corruption
"""
import os
import hashlib
import shutil
from typing import Optional, Callable, Tuple


class IntegrityVerifier:
    """
    Verify file copy integrity using hash comparison.
    Ensures zero data loss during file operations.
    """
    
    def __init__(self):
        """Initialize integrity verifier"""
        self.verifications_performed = 0
        self.verifications_passed = 0
        self.verifications_failed = 0
    
    def calculate_hash(self, file_path: str, algorithm: str = 'md5',
                      chunk_size: int = 8192) -> Optional[str]:
        """
        Calculate hash of file.
        
        Args:
            file_path: Path to file
            algorithm: Hash algorithm ('md5', 'sha1', 'sha256')
            chunk_size: Size of chunks to read
            
        Returns:
            Hash as hex string, or None if error
        """
        try:
            if algorithm == 'md5':
                hasher = hashlib.md5()
            elif algorithm == 'sha1':
                hasher = hashlib.sha1()
            elif algorithm == 'sha256':
                hasher = hashlib.sha256()
            else:
                raise ValueError(f"Unsupported algorithm: {algorithm}")
            
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(chunk_size), b""):
                    hasher.update(chunk)
            
            return hasher.hexdigest()
        except (IOError, OSError) as e:
            print(f"Error calculating hash for {file_path}: {e}")
            return None
    
    def verify_copy(self, source: str, destination: str,
                   quick_check: bool = True) -> bool:
        """
        Verify that destination file is identical to source.
        
        Args:
            source: Source file path
            destination: Destination file path
            quick_check: If True, do quick size check first
            
        Returns:
            True if files are identical, False otherwise
        """
        self.verifications_performed += 1
        
        try:
            # Check that both files exist
            if not os.path.exists(source):
                print(f"Source file not found: {source}")
                self.verifications_failed += 1
                return False
            
            if not os.path.exists(destination):
                print(f"Destination file not found: {destination}")
                self.verifications_failed += 1
                return False
            
            # Quick check: compare sizes
            if quick_check:
                source_size = os.path.getsize(source)
                dest_size = os.path.getsize(destination)
                
                if source_size != dest_size:
                    print(f"Size mismatch: {source} ({source_size}) != {destination} ({dest_size})")
                    self.verifications_failed += 1
                    return False
            
            # Full check: compare hashes
            source_hash = self.calculate_hash(source)
            dest_hash = self.calculate_hash(destination)
            
            if source_hash is None or dest_hash is None:
                self.verifications_failed += 1
                return False
            
            if source_hash != dest_hash:
                print(f"Hash mismatch: {source} != {destination}")
                self.verifications_failed += 1
                return False
            
            self.verifications_passed += 1
            return True
            
        except Exception as e:
            print(f"Verification error: {e}")
            self.verifications_failed += 1
            return False
    
    def safe_copy(self, source: str, destination: str,
                 verify: bool = True,
                 remove_on_failure: bool = True) -> Tuple[bool, Optional[str]]:
        """
        Copy file with integrity verification.
        
        Args:
            source: Source file path
            destination: Destination file path
            verify: Verify copy after completion
            remove_on_failure: Remove destination if verification fails
            
        Returns:
            Tuple of (success: bool, error_message: Optional[str])
        """
        try:
            # Ensure destination directory exists
            dest_dir = os.path.dirname(destination)
            if dest_dir:
                os.makedirs(dest_dir, exist_ok=True)
            
            # Copy file
            shutil.copy2(source, destination)
            
            # Verify if requested
            if verify:
                if not self.verify_copy(source, destination):
                    if remove_on_failure and os.path.exists(destination):
                        try:
                            os.remove(destination)
                        except OSError:
                            pass
                    return False, "Copy verification failed"
            
            return True, None
            
        except (IOError, OSError, shutil.Error) as e:
            return False, str(e)
    
    def safe_move(self, source: str, destination: str,
                 verify: bool = True,
                 remove_on_failure: bool = True) -> Tuple[bool, Optional[str]]:
        """
        Move file with integrity verification.
        
        Args:
            source: Source file path
            destination: Destination file path
            verify: Verify after move
            remove_on_failure: Remove destination if verification fails
            
        Returns:
            Tuple of (success: bool, error_message: Optional[str])
        """
        try:
            # Ensure destination directory exists
            dest_dir = os.path.dirname(destination)
            if dest_dir:
                os.makedirs(dest_dir, exist_ok=True)
            
            # Calculate source hash before move (if verifying)
            source_hash = None
            if verify:
                source_hash = self.calculate_hash(source)
                if source_hash is None:
                    return False, "Could not calculate source hash"
            
            # Move file
            shutil.move(source, destination)
            
            # Verify if requested
            if verify:
                dest_hash = self.calculate_hash(destination)
                if dest_hash is None:
                    return False, "Could not calculate destination hash"
                
                if source_hash != dest_hash:
                    # Verification failed
                    if remove_on_failure and os.path.exists(destination):
                        try:
                            os.remove(destination)
                        except OSError:
                            pass
                    return False, "Move verification failed"
            
            return True, None
            
        except (IOError, OSError, shutil.Error) as e:
            return False, str(e)
    
    def batch_verify(self, file_pairs: list,
                    progress_callback: Optional[Callable] = None) -> dict:
        """
        Verify multiple file pairs.
        
        Args:
            file_pairs: List of (source, destination) tuples
            progress_callback: Optional callback(current, total, filename)
            
        Returns:
            Dictionary with results:
                {
                    'total': int,
                    'passed': int,
                    'failed': int,
                    'failed_files': [(source, dest), ...]
                }
        """
        total = len(file_pairs)
        passed = 0
        failed = 0
        failed_files = []
        
        for i, (source, dest) in enumerate(file_pairs):
            if self.verify_copy(source, dest):
                passed += 1
            else:
                failed += 1
                failed_files.append((source, dest))
            
            if progress_callback:
                progress_callback(i + 1, total, os.path.basename(source))
        
        return {
            'total': total,
            'passed': passed,
            'failed': failed,
            'failed_files': failed_files
        }
    
    def get_statistics(self) -> dict:
        """
        Get verification statistics.
        
        Returns:
            Dictionary with statistics
        """
        success_rate = 0
        if self.verifications_performed > 0:
            success_rate = (self.verifications_passed / self.verifications_performed) * 100
        
        return {
            'total_verifications': self.verifications_performed,
            'passed': self.verifications_passed,
            'failed': self.verifications_failed,
            'success_rate_percent': round(success_rate, 2)
        }
    
    def reset_statistics(self):
        """Reset verification statistics"""
        self.verifications_performed = 0
        self.verifications_passed = 0
        self.verifications_failed = 0


# Convenience functions
def verify_files_match(file1: str, file2: str) -> bool:
    """
    Quick function to verify two files are identical.
    
    Args:
        file1: First file path
        file2: Second file path
        
    Returns:
        True if files are identical
    """
    verifier = IntegrityVerifier()
    return verifier.verify_copy(file1, file2)


def safe_copy_file(source: str, destination: str) -> bool:
    """
    Quick function to safely copy a file with verification.
    
    Args:
        source: Source file path
        destination: Destination file path
        
    Returns:
        True if copy successful and verified
    """
    verifier = IntegrityVerifier()
    success, error = verifier.safe_copy(source, destination)
    if not success:
        print(f"Copy failed: {error}")
    return success
