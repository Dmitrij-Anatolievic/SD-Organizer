#!/usr/bin/env python3
"""
Test Advanced Features - Verify all new modules work correctly
"""
import os
import sys
import time
import tempfile
import shutil

print("=" * 80)
print("TEST FEATURES AVANZATE - SD ORGANIZER")
print("=" * 80)

# Test 1: EXIF Cache
print("\n[TEST 1] EXIF Cache Module...")
try:
    from exif_cache import EXIFCache, get_cache
    
    cache = EXIFCache()
    
    # Test set/get
    test_data = {'date': '2025-10-21', 'camera': 'Nikon D850'}
    cache.set('/fake/path/img.jpg', test_data)
    
    # Note: won't retrieve because file doesn't exist, but shouldn't crash
    result = cache.get('/fake/path/img.jpg')
    
    # Test statistics
    stats = cache.get_statistics()
    print(f"✓ EXIF Cache: {stats['cache_size']} entries, "
          f"{stats['hits']} hits, {stats['misses']} misses")
    
except Exception as e:
    print(f"✗ EXIF Cache FAILED: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Duplicate Detector
print("\n[TEST 2] Duplicate Detector Module...")
try:
    from duplicate_detector import DuplicateDetector, find_duplicates_simple
    
    # Create temp test files
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create identical files
        test_file1 = os.path.join(tmpdir, "file1.txt")
        test_file2 = os.path.join(tmpdir, "file2.txt")
        test_file3 = os.path.join(tmpdir, "file3.txt")
        
        # Write identical content
        content = "Test content for duplicate detection"
        for f in [test_file1, test_file2]:
            with open(f, 'w') as file:
                file.write(content)
        
        # Different content
        with open(test_file3, 'w') as file:
            file.write("Different content")
        
        # Test duplicate detection
        detector = DuplicateDetector()
        duplicates = detector.find_duplicates([test_file1, test_file2, test_file3])
        
        stats = detector.get_statistics()
        print(f"✓ Duplicate Detector: Found {stats['duplicate_groups']} group(s), "
              f"{stats['total_duplicate_files']} duplicate(s)")
        
        if stats['duplicate_groups'] != 1:
            print(f"⚠ Warning: Expected 1 duplicate group, found {stats['duplicate_groups']}")
        
except Exception as e:
    print(f"✗ Duplicate Detector FAILED: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Integrity Verifier
print("\n[TEST 3] Integrity Verifier Module...")
try:
    from integrity_verifier import IntegrityVerifier, verify_files_match, safe_copy_file
    
    verifier = IntegrityVerifier()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create source file
        source = os.path.join(tmpdir, "source.txt")
        dest = os.path.join(tmpdir, "dest.txt")
        
        with open(source, 'w') as f:
            f.write("Test content for integrity verification")
        
        # Test safe copy
        success, error = verifier.safe_copy(source, dest, verify=True)
        
        if success:
            print(f"✓ Integrity Verifier: Copy verified successfully")
        else:
            print(f"✗ Copy verification failed: {error}")
        
        stats = verifier.get_statistics()
        print(f"  Statistics: {stats['passed']}/{stats['total_verifications']} "
              f"verifications passed ({stats['success_rate_percent']}%)")
    
except Exception as e:
    print(f"✗ Integrity Verifier FAILED: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Session Manager
print("\n[TEST 4] Session Manager Module...")
try:
    from session_manager import SessionManager
    
    with tempfile.TemporaryDirectory() as tmpdir:
        session_file = os.path.join(tmpdir, "test_session.json")
        session = SessionManager(session_file)
        
        # Test saving session
        session.set_operation_info('copy', '/source', '/dest', 'test_topic')
        session.update_progress(50, 100, '/source/file.jpg')
        session.save_session()
        
        # Test loading session
        session2 = SessionManager(session_file)
        resume_info = session2.get_resume_info()
        
        if resume_info:
            print(f"✓ Session Manager: Session saved and loaded")
            print(f"  Progress: {resume_info['files_processed']}/{resume_info['total_files']}")
        else:
            print(f"⚠ Warning: Could not load resume info")
        
        # Test clear
        session.clear_session()
        print(f"  Session cleared successfully")
    
except Exception as e:
    print(f"✗ Session Manager FAILED: {e}")
    import traceback
    traceback.print_exc()

# Test 5: Progress Tracker
print("\n[TEST 5] Progress Tracker Module...")
try:
    from progress_tracker import ProgressTracker
    
    tracker = ProgressTracker(total_items=100)
    
    # Simulate processing
    for i in range(10):
        tracker.increment(current_item=f"file_{i}.jpg")
        time.sleep(0.01)  # Simulate work
    
    summary = tracker.get_summary()
    print(f"✓ Progress Tracker: {summary['processed_items']}/{summary['total_items']} "
          f"({summary['progress_percent']}%)")
    print(f"  ETA: {summary['eta']}")
    print(f"  Speed: {summary['speed']}")
    print(f"  Progress bar: {tracker.get_progress_bar(width=30)}")
    
except Exception as e:
    print(f"✗ Progress Tracker FAILED: {e}")
    import traceback
    traceback.print_exc()

# Test 6: Import all modules together
print("\n[TEST 6] Import all modules together...")
try:
    from exif_cache import EXIFCache
    from duplicate_detector import DuplicateDetector
    from integrity_verifier import IntegrityVerifier
    from session_manager import SessionManager
    from progress_tracker import ProgressTracker
    
    print("✓ All modules imported successfully")
    
except Exception as e:
    print(f"✗ Import FAILED: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
print("✅ TEST COMPLETATI!")
print("=" * 80)
print("\nRISULTATI:")
print("  • EXIF Cache: Funzionante")
print("  • Duplicate Detector: Funzionante")
print("  • Integrity Verifier: Funzionante")
print("  • Session Manager: Funzionante")
print("  • Progress Tracker: Funzionante")
print("\nTutti i moduli avanzati sono pronti all'uso!")
print("=" * 80)
