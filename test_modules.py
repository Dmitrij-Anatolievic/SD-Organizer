#!/usr/bin/env python3
"""
Test script per verificare che tutti i moduli siano corretti
Prima di avviare l'applicazione vera, esegui questo script
"""
import sys
import os

print("=" * 70)
print("SD ORGANIZER V3 - PRE-FLIGHT CHECK")
print("=" * 70)
print()

errors_found = []
warnings_found = []

# Test 1: Verifica sintassi Python
print("[ 1 ] Verifica sintassi Python...")
modules_to_check = [
    'photo_organizer_logic.py',
    'main_app.py',
    'multi_event_dialog.py',
    'database_manager.py',
    'auto_import_service.py',
    'processing_tools.py',
    'themes.py'
]

for module in modules_to_check:
    if not os.path.exists(module):
        warnings_found.append(f"File {module} non trovato")
        continue
    
    try:
        with open(module, 'r', encoding='utf-8') as f:
            code = f.read()
        compile(code, module, 'exec')
        print(f"  ✓ {module}")
    except SyntaxError as e:
        errors_found.append(f"Errore sintassi in {module}: {e}")
        print(f"  ✗ {module} - ERRORE: {e}")

print()

# Test 2: Verifica import base (senza PyQt6)
print("[ 2 ] Verifica import moduli base...")
try:
    sys.path.insert(0, '.')
    
    # Test import photo_organizer_logic
    print("  → Importando photo_organizer_logic...")
    try:
        from photo_organizer_logic import SDOrganizerBase
        print("    ✓ photo_organizer_logic OK")
    except Exception as e:
        errors_found.append(f"Import photo_organizer_logic: {e}")
        print(f"    ✗ ERRORE: {e}")
    
    # Test import database_manager
    print("  → Importando database_manager...")
    try:
        from database_manager import PhotoDatabase
        print("    ✓ database_manager OK")
    except Exception as e:
        errors_found.append(f"Import database_manager: {e}")
        print(f"    ✗ ERRORE: {e}")
    
    # Test import processing_tools
    print("  → Importando processing_tools...")
    try:
        from processing_tools import ImageProcessor
        print("    ✓ processing_tools OK")
    except Exception as e:
        errors_found.append(f"Import processing_tools: {e}")
        print(f"    ✗ ERRORE: {e}")
    
    # Test import auto_import_service
    print("  → Importando auto_import_service...")
    try:
        from auto_import_service import AutoImportService
        print("    ✓ auto_import_service OK")
    except Exception as e:
        errors_found.append(f"Import auto_import_service: {e}")
        print(f"    ✗ ERRORE: {e}")
    
except Exception as e:
    errors_found.append(f"Errore generale import: {e}")
    print(f"  ✗ ERRORE GENERALE: {e}")

print()

# Test 3: Verifica dipendenze
print("[ 3 ] Verifica dipendenze Python...")
required_packages = {
    'PIL': 'Pillow',
    'psutil': 'psutil',
}

for import_name, package_name in required_packages.items():
    try:
        __import__(import_name)
        print(f"  ✓ {package_name}")
    except ImportError:
        warnings_found.append(f"Pacchetto {package_name} non installato")
        print(f"  ✗ {package_name} - NON INSTALLATO")

print()

# Test 4: Verifica PyQt6 (opzionale per GUI)
print("[ 4 ] Verifica PyQt6 (richiesto per GUI)...")
try:
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtCore import QThread, pyqtSignal
    print("  ✓ PyQt6 installato correttamente")
    pyqt6_installed = True
except ImportError as e:
    warnings_found.append(f"PyQt6 non installato: {e}")
    print(f"  ✗ PyQt6 NON INSTALLATO")
    print(f"     Installa con: pip install PyQt6")
    pyqt6_installed = False

print()

# Test 5: Verifica file di configurazione
print("[ 5 ] Verifica file di configurazione...")
config_files = ['config.json', 'preferences.json']

for config_file in config_files:
    if os.path.exists(config_file):
        print(f"  ✓ {config_file} trovato")
        try:
            import json
            with open(config_file, 'r') as f:
                json.load(f)
            print(f"    ✓ {config_file} formato valido")
        except json.JSONDecodeError as e:
            errors_found.append(f"{config_file} non è un JSON valido: {e}")
            print(f"    ✗ {config_file} - JSON NON VALIDO")
    else:
        warnings_found.append(f"{config_file} non trovato")
        print(f"  ⚠ {config_file} non trovato (verrà creato automaticamente)")

print()

# Test 6: Verifica metodi critici
print("[ 6 ] Verifica metodi critici...")
try:
    from photo_organizer_logic import SDOrganizerBase
    
    # Verifica presenza metodi
    critical_methods = [
        'analyze_dates_in_sd',
        'organize_sd_files',
        'organize_sd_files_multi_event',
        '_organize_sd_files_internal',
        '_organize_sd_files_multi_event_internal'
    ]
    
    for method_name in critical_methods:
        if hasattr(SDOrganizerBase, method_name):
            print(f"  ✓ Metodo {method_name} presente")
        else:
            errors_found.append(f"Metodo {method_name} mancante in SDOrganizerBase")
            print(f"  ✗ Metodo {method_name} MANCANTE")
    
except Exception as e:
    errors_found.append(f"Errore verifica metodi: {e}")
    print(f"  ✗ ERRORE: {e}")

print()

# Test 7: Test creazione istanza database (se disponibile)
print("[ 7 ] Test creazione istanza database...")
try:
    from database_manager import PhotoDatabase
    import tempfile
    
    # Use temp file instead of :memory: to avoid SQLite limitation
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        tmp_db_path = tmp.name
    
    try:
        db = PhotoDatabase(db_path=tmp_db_path)
        print("  ✓ Database istanziato correttamente")
        
        # Test metodi base
        stats = db.get_statistics()
        print(f"  ✓ Statistiche database: {stats['total_photos']} foto")
    finally:
        # Cleanup
        import os
        if os.path.exists(tmp_db_path):
            os.unlink(tmp_db_path)
    
except Exception as e:
    errors_found.append(f"Errore test database: {e}")
    print(f"  ✗ ERRORE: {e}")

print()

# Test 8: Test ImageProcessor
print("[ 8 ] Test ImageProcessor...")
try:
    from processing_tools import ImageProcessor
    processor = ImageProcessor()
    print("  ✓ ImageProcessor istanziato correttamente")
except Exception as e:
    errors_found.append(f"Errore test ImageProcessor: {e}")
    print(f"  ✗ ERRORE: {e}")

print()

# Test 9: Test PhotoOrganizer initialization
print("[ 9 ] Test PhotoOrganizer initialization...")
try:
    from photo_organizer_logic import PhotoOrganizer
    
    # Test with brand_name parameter (correct)
    organizer = PhotoOrganizer(
        brand_name="Nikon",
        pictures_path="/tmp/test",
        logs_path="/tmp/logs"
    )
    print("  ✓ PhotoOrganizer istanziato con brand_name (corretto)")
    
except Exception as e:
    errors_found.append(f"Errore test PhotoOrganizer: {e}")
    print(f"  ✗ ERRORE: {e}")

print()

# ======= RISULTATO FINALE =======
print("=" * 70)
print("RISULTATO FINALE")
print("=" * 70)

if errors_found:
    print(f"\n❌ ERRORI CRITICI TROVATI ({len(errors_found)}):")
    for i, error in enumerate(errors_found, 1):
        print(f"  {i}. {error}")
    print("\n⚠️  IMPOSSIBILE AVVIARE L'APPLICAZIONE!")
    print("    Correggi gli errori sopra prima di procedere.\n")
    sys.exit(1)

if warnings_found:
    print(f"\n⚠️  WARNING ({len(warnings_found)}):")
    for i, warning in enumerate(warnings_found, 1):
        print(f"  {i}. {warning}")
    
    if not pyqt6_installed:
        print("\n⚠️  PyQt6 non installato:")
        print("    L'applicazione GUI non può partire senza PyQt6")
        print("    Installa con: pip install PyQt6\n")

print("\n✅ PRE-FLIGHT CHECK COMPLETATO")

if not errors_found and pyqt6_installed:
    print("\n🚀 TUTTO OK! Puoi avviare l'applicazione con:")
    print("    python main_app.py\n")
elif not errors_found and not pyqt6_installed:
    print("\n⚠️  Installa PyQt6 per avviare l'applicazione GUI:")
    print("    pip install PyQt6")
    print("\n    Poi esegui: python main_app.py\n")

print("=" * 70)
