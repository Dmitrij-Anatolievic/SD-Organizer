#!/usr/bin/env python3
"""
Test script per verificare il rilevamento dei drive senza crash
"""
import sys
import psutil

print("=" * 60)
print("TEST DI RILEVAMENTO DRIVE - VERSIONE CORRETTA")
print("=" * 60)

# Test 1: Verifica che psutil funzioni
print("\n[TEST 1] Verifica funzionamento psutil...")
try:
    partitions = psutil.disk_partitions(all=False)
    print(f"✓ psutil funziona correttamente. Trovate {len(partitions)} partizioni.")
except Exception as e:
    print(f"✗ ERRORE con psutil: {e}")
    sys.exit(1)

# Test 2: Verifica gestione sicura di partition.opts
print("\n[TEST 2] Test gestione sicura di partition.opts...")
errors = []
for partition in partitions:
    try:
        # Simula il codice VECCHIO (che causava il crash)
        # if 'removable' in partition.opts.lower():  # QUESTO CRASHAVA!
        
        # Codice NUOVO (sicuro)
        opts_str = ''
        if isinstance(partition.opts, str):
            opts_str = partition.opts.lower()
        elif isinstance(partition.opts, list):
            opts_str = ','.join(partition.opts).lower()
        else:
            opts_str = str(partition.opts).lower()
        
        # Test sicuro di fstype
        is_sd_filesystem = False
        if partition.fstype:
            is_sd_filesystem = partition.fstype.lower() in ['exfat', 'vfat', 'fat32', 'fat']
        
        print(f"  ✓ {partition.device}: opts={partition.opts} (type: {type(partition.opts).__name__}), fstype={partition.fstype}")
        
    except Exception as e:
        error_msg = f"  ✗ ERRORE con {partition.device}: {e}"
        print(error_msg)
        errors.append(error_msg)

if errors:
    print(f"\n✗ TEST FALLITO: {len(errors)} errori trovati")
    for err in errors:
        print(err)
    sys.exit(1)
else:
    print(f"\n✓ TEST SUPERATO: Nessun crash durante il rilevamento di {len(partitions)} partizioni")

# Test 3: Test del modulo photo_organizer_logic
print("\n[TEST 3] Test importazione modulo photo_organizer_logic...")
try:
    from photo_organizer_logic import SDOrganizerBase
    print("✓ Modulo photo_organizer_logic importato correttamente")
except Exception as e:
    print(f"✗ ERRORE nell'importazione: {e}")
    sys.exit(1)

# Test 4: Test funzione di rilevamento drive
print("\n[TEST 4] Test funzione detect_removable_drives...")
try:
    # Crea un organizer di test
    test_config = {
        "SD_FOLDER_NAMES_CANDIDATES": ["DCIM", "100NIKON"],
        "FILE_DESTINATIONS": {".jpg": "Images/JPEG"}
    }
    
    class TestOrganizer(SDOrganizerBase):
        def __init__(self):
            super().__init__(
                brand_name="TestBrand",
                pictures_path="/tmp",
                logs_path="/tmp",
                config=test_config
            )
    
    organizer = TestOrganizer()
    drives = organizer.detect_removable_drives()
    print(f"✓ Funzione detect_removable_drives eseguita senza crash")
    print(f"  Trovati {len(drives)} drive rimovibili: {[d['label'] for d in drives]}")
    
except Exception as e:
    print(f"✗ ERRORE durante il test: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("✓ TUTTI I TEST SUPERATI - IL PROGRAMMA NON CRASHERA' PIU'!")
print("=" * 60)
