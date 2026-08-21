"""
Test script per verificare il fix del bug formatter
"""
import sys
import os

# Aggiungi il path corrente per import
sys.path.insert(0, os.path.dirname(__file__))

def test_formatter_bug():
    """Test che il bug del formatter sia stato corretto"""
    print("=" * 60)
    print("TEST: Verifica fix bug formatter")
    print("=" * 60)
    
    try:
        from photo_organizer_logic import PhotoOrganizer
        
        # Crea un'istanza con parametri minimi
        config = {
            "SD_FOLDER_NAMES_CANDIDATES": ["DCIM"],
            "FILE_DESTINATIONS": {".jpg": "Images"}
        }
        
        app_config = {
            "PICTURES_PATH": os.path.expanduser("~"),
            "LOGS_PATH": os.path.join(os.path.expanduser("~"), "test_logs")
        }
        
        print("\n✓ Import successful")
        print(f"✓ Creating PhotoOrganizer instance...")
        
        organizer = PhotoOrganizer(
            brand_name="Nikon",
            pictures_path=app_config["PICTURES_PATH"],
            logs_path=app_config["LOGS_PATH"],
            config=config,
            app_config=app_config
        )
        
        print("✓ PhotoOrganizer created successfully!")
        print(f"✓ Logger initialized: {organizer.logger is not None}")
        print(f"✓ Logger handlers: {len(organizer.logger.handlers)}")
        
        # Test logging
        organizer.log_and_callback("info", "Test message 1")
        organizer.log_and_callback("warning", "Test warning")
        organizer.log_and_callback("error", "Test error")
        
        print("✓ Logging test passed!")
        
        # Test SD card detection
        print("\n" + "-" * 60)
        print("Testing SD card detection...")
        print("-" * 60)
        
        drives = organizer.detect_removable_drives()
        print(f"✓ Detected {len(drives)} removable drive(s)")
        
        for i, drive in enumerate(drives, 1):
            print(f"  {i}. {drive.get('label', 'Unknown')}")
            print(f"     Path: {drive.get('path', 'Unknown')}")
            if 'volume_serial' in drive:
                print(f"     Serial: {drive.get('volume_serial', 'N/A')}")
        
        # Test cache system
        print("\n" + "-" * 60)
        print("Testing SD card cache system...")
        print("-" * 60)
        
        if hasattr(organizer, 'sd_card_cache'):
            print(f"✓ Cache initialized: {organizer.sd_card_cache_file}")
            print(f"✓ Cached entries: {len(organizer.sd_card_cache)}")
            
            if organizer.sd_card_cache:
                print("\nCached SD cards:")
                for serial, info in organizer.sd_card_cache.items():
                    print(f"  • Serial: {serial}")
                    print(f"    Brand: {info.get('brand', 'Unknown')}")
                    print(f"    Last seen: {info.get('last_seen', 'Unknown')}")
                    print(f"    Last path: {info.get('last_path', 'Unknown')}")
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print("\nIl bug del formatter è stato corretto con successo!")
        print("Il programma ora si avvia correttamente.")
        
        return True
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ TEST FAILED!")
        print("=" * 60)
        print(f"\nErrore: {type(e).__name__}: {e}")
        
        import traceback
        print("\nTraceback completo:")
        traceback.print_exc()
        
        return False

if __name__ == "__main__":
    success = test_formatter_bug()
    sys.exit(0 if success else 1)
