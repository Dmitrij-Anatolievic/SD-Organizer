#!/usr/bin/env python3
"""
SD ORGANIZER V3 - LAUNCHER CON LOGGING COMPLETO
Questo script cattura TUTTI gli errori e li mostra chiaramente
"""
import sys
import os
import traceback
import logging
from datetime import datetime

# Setup logging completo
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

log_filename = os.path.join(log_dir, f"sd_organizer_debug_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

# Configurazione logging multi-level
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("SD_Organizer_Launcher")

print("=" * 80)
print("SD ORGANIZER V3 - LAUNCHER CON DEBUG COMPLETO")
print("=" * 80)
print(f"Log file: {log_filename}")
print()

logger.info("=" * 80)
logger.info("AVVIO SD ORGANIZER V3")
logger.info("=" * 80)

# Step 1: Verifica ambiente Python
logger.info("Step 1: Verifica ambiente Python")
logger.info(f"Python version: {sys.version}")
logger.info(f"Python executable: {sys.executable}")
logger.info(f"Current directory: {os.getcwd()}")
logger.info(f"Script directory: {os.path.dirname(os.path.abspath(__file__))}")

# Step 2: Verifica file necessari
logger.info("\nStep 2: Verifica file necessari")
required_files = [
    'main_app.py',
    'photo_organizer_logic.py',
    'config.json',
    'themes.py'
]

for filename in required_files:
    exists = os.path.exists(filename)
    status = "✓ OK" if exists else "✗ MANCANTE"
    logger.info(f"  {filename}: {status}")
    if not exists:
        logger.error(f"ERRORE: File mancante: {filename}")
        sys.exit(1)

# Step 3: Test import moduli base
logger.info("\nStep 3: Test import moduli base")

try:
    logger.info("  Importando os, sys, json...")
    import os, sys, json
    logger.info("  ✓ Moduli standard OK")
except Exception as e:
    logger.error(f"  ✗ ERRORE import moduli standard: {e}")
    traceback.print_exc()
    sys.exit(1)

try:
    logger.info("  Importando Pillow...")
    from PIL import Image
    logger.info("  ✓ Pillow OK")
except Exception as e:
    logger.error(f"  ✗ ERRORE: Pillow non installato")
    logger.error(f"  Installa con: pip install Pillow")
    traceback.print_exc()
    sys.exit(1)

try:
    logger.info("  Importando psutil...")
    import psutil
    logger.info("  ✓ psutil OK")
except Exception as e:
    logger.error(f"  ✗ ERRORE: psutil non installato")
    logger.error(f"  Installa con: pip install psutil")
    traceback.print_exc()
    sys.exit(1)

try:
    logger.info("  Importando PyQt6...")
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtCore import QThread, pyqtSignal
    logger.info("  ✓ PyQt6 OK")
except Exception as e:
    logger.error(f"  ✗ ERRORE: PyQt6 non installato")
    logger.error(f"  Installa con: pip install PyQt6")
    traceback.print_exc()
    sys.exit(1)

# Step 4: Import photo_organizer_logic
logger.info("\nStep 4: Import photo_organizer_logic")
try:
    logger.info("  Importando photo_organizer_logic...")
    from photo_organizer_logic import SDOrganizerBase, PhotoOrganizer
    logger.info("  ✓ photo_organizer_logic OK")
    
    # Verifica signature __init__
    import inspect
    sig = inspect.signature(SDOrganizerBase.__init__)
    logger.info(f"  Signature SDOrganizerBase.__init__: {sig}")
    
    params = list(sig.parameters.keys())
    logger.info(f"  Parametri: {params}")
    
    if 'brand_name' in params:
        logger.info("  ✓ Parametro 'brand_name' presente")
    else:
        logger.error("  ✗ Parametro 'brand_name' MANCANTE!")
    
    if 'brand' in params:
        logger.warning("  ⚠ Parametro 'brand' presente (dovrebbe essere 'brand_name')")
    
except Exception as e:
    logger.error(f"  ✗ ERRORE import photo_organizer_logic: {e}")
    traceback.print_exc()
    sys.exit(1)

# Step 5: Import main_app
logger.info("\nStep 5: Import main_app")
try:
    logger.info("  Importando main_app...")
    from main_app import SDOrganizerApp
    logger.info("  ✓ main_app OK")
except Exception as e:
    logger.error(f"  ✗ ERRORE import main_app: {e}")
    traceback.print_exc()
    sys.exit(1)

# Step 6: Test creazione istanza PhotoOrganizer
logger.info("\nStep 6: Test creazione istanza PhotoOrganizer")
try:
    logger.info("  Tentativo 1: Con brand_name='TestBrand'")
    test_organizer = PhotoOrganizer(
        brand_name="TestBrand",
        pictures_path="/tmp/test",
        logs_path="/tmp/logs"
    )
    logger.info("  ✓ PhotoOrganizer creato con successo!")
    logger.info(f"  Brand configurato: {test_organizer.brand_name}")
except Exception as e:
    logger.error(f"  ✗ ERRORE creazione PhotoOrganizer: {e}")
    logger.error(f"  Tipo errore: {type(e).__name__}")
    traceback.print_exc()
    
    # Prova con 'brand' invece di 'brand_name'
    logger.info("\n  Tentativo 2: Con brand='TestBrand' (parametro alternativo)")
    try:
        test_organizer2 = PhotoOrganizer(
            brand="TestBrand",
            pictures_path="/tmp/test",
            logs_path="/tmp/logs"
        )
        logger.info("  ✓ PhotoOrganizer creato con 'brand' invece di 'brand_name'!")
        logger.warning("  ⚠ ATTENZIONE: Il parametro si chiama 'brand', non 'brand_name'!")
    except Exception as e2:
        logger.error(f"  ✗ Anche con 'brand' fallisce: {e2}")
        traceback.print_exc()

# Step 7: Avvio applicazione
logger.info("\nStep 7: Avvio applicazione GUI")
logger.info("  Creando QApplication...")

try:
    app = QApplication(sys.argv)
    logger.info("  ✓ QApplication creata")
    
    logger.info("  Creando SDOrganizerApp...")
    window = SDOrganizerApp()
    logger.info("  ✓ SDOrganizerApp creata")
    
    logger.info("  Mostrando finestra...")
    window.show()
    logger.info("  ✓ Finestra mostrata")
    
    logger.info("\n" + "=" * 80)
    logger.info("APPLICAZIONE AVVIATA CON SUCCESSO!")
    logger.info(f"Log salvato in: {log_filename}")
    logger.info("=" * 80)
    
    print("\n" + "=" * 80)
    print("✅ APPLICAZIONE AVVIATA CON SUCCESSO!")
    print(f"📋 Log salvato in: {log_filename}")
    print("=" * 80)
    print()
    
    # Avvia event loop
    sys.exit(app.exec())
    
except Exception as e:
    logger.error("\n" + "=" * 80)
    logger.error("ERRORE DURANTE L'AVVIO!")
    logger.error("=" * 80)
    logger.error(f"Errore: {e}")
    logger.error(f"Tipo: {type(e).__name__}")
    logger.error("\nTraceback completo:")
    traceback.print_exc()
    
    print("\n" + "=" * 80)
    print("❌ ERRORE DURANTE L'AVVIO!")
    print("=" * 80)
    print(f"Errore: {e}")
    print(f"\n📋 Controlla il log completo in: {log_filename}")
    print("=" * 80)
    
    sys.exit(1)
