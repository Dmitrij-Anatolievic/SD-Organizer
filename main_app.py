"""
SD Organizer Main Application
Fixed and Enhanced Version with PyQt6
"""
import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
    QWidget, QPushButton, QLabel, QComboBox, QProgressBar,
    QTextEdit, QFileDialog, QMessageBox, QLineEdit,
    QGroupBox, QDialog, QFormLayout, QDialogButtonBox, QListWidget,
    QTabWidget
)
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QFont
import json
import themes

# --- UNIFIED IMPORT ---
from photo_organizer_logic import PhotoOrganizer

# =========================================================
# === EMBEDDED CONFIGURATION AND THEMES (HARDENED) ========
# =========================================================

# --- COMPLETE INCORPORATION OF themes.py ---
STYLE_WARM_SUNSET = """
    QMainWindow { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FF5F6D, stop:1 #FFC371); color: #333333; }
    QLabel { color: #333333; }
    QGroupBox { border: 2px solid #E67E22; border-radius: 8px; margin-top: 1ex; font-weight: bold; color: #BF360C; font-size: 14px; }
    QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 8px; background-color: #E67E22; border-radius: 5px; }
    QPushButton { background-color: #F39C12; color: white; border-radius: 5px; padding: 10px 20px; font-weight: bold; font-size: 13px; border: 1px solid #D35400; }
    QPushButton:hover { background-color: #D35400; }
    QLineEdit, QSpinBox, QComboBox, QListWidget { background-color: white; color: #333333; border: 1px solid #F39C12; border-radius: 4px; padding: 4px; font-size: 13px; }
    QStatusBar { background-color: #D35400; color: white; }
    QProgressBar::chunk { background-color: #E67E22; }
"""

STYLE_COOL_OCEAN = """
    QMainWindow {background-color: #3b4252; color: #eceff4;} 
    QWidget {color: #eceff4;} 
    QPushButton {background-color: #5e81ac; color: #eceff4; border: 1px solid #88c0d0; border-radius: 5px; padding: 5px;} 
    QPushButton:hover {background-color: #88c0d0; color: #3b4252;} 
    QComboBox, QLineEdit, QTextEdit {background-color: #4c566a; color: #eceff4; border: 1px solid #4c566a; padding: 2px;} 
    QProgressBar::chunk {background-color: #a3be8c;} 
    QGroupBox {border: 1px solid #5e81ac; margin-top: 10px; padding-top: 5px;} 
    QGroupBox::title {subcontrol-origin: margin; subcontrol-position: top left; padding: 0 3px; color: #88c0d0;}
"""

STYLE_DARK_MODE = """
    QMainWindow {background-color: #2e3440; color: #d8dee9;} 
    QWidget {color: #d8dee9;} 
    QPushButton {background-color: #4c566a; color: #d8dee9; border: 1px solid #81a1c1; border-radius: 5px; padding: 5px;} 
    QPushButton:hover {background-color: #81a1c1; color: #2e3440;} 
    QComboBox, QLineEdit, QTextEdit {background-color: #3b4252; color: #d8dee9; border: 1px solid #3b4252; padding: 2px;} 
    QProgressBar::chunk {background-color: #bf616a;} 
    QGroupBox {border: 1px solid #4c566a; margin-top: 10px; padding-top: 5px;} 
    QGroupBox::title {subcontrol-origin: margin; subcontrol-position: top left; padding: 0 3px; color: #81a1c1;}
"""

# THEMES DICTIONARY
THEMES = themes.THEMES

# --- COMPLETE INCORPORATION OF config.json ---
CONFIG_STRING = """
{
    "APP_CONFIG": {
        "PICTURES_PATH": "C:/Users/Dmitr/Pictures",
        "LOGS_PATH": "C:/Users/Dmitr/Pictures/logs",
        "MIN_FREE_SPACE_GB": 5
    },
    "CONFIGURATIONS": {
        "Nikon": {"SD_FOLDER_NAMES_CANDIDATES": ["100NIKON", "101NIKON", "102NIKON", "103NIKON", "104NIKON", "105NIKON", "106NIKON", "107NIKON", "103NZ_FC", "DCIM"], "FILE_DESTINATIONS": {".jpg": "Images/JPEG", ".jpeg": "Images/JPEG", ".heic": "Images/HEIF", ".heif": "Images/HEIF", ".nef": "Images/RAW", ".nrw": "Images/RAW", ".raw": "Images/RAW", ".mov": "Videos", ".mp4": "Videos"}},
        "Fujifilm": {"SD_FOLDER_NAMES_CANDIDATES": ["100_FUJI", "101_FUJI", "DCIM"], "FILE_DESTINATIONS": {".jpg": "Images/JPEG", ".jpeg": "Images/JPEG", ".raf": "Images/RAW", ".dng": "Images/RAW", ".mov": "Videos", ".mp4": "Videos"}},
        "Olympus": {"SD_FOLDER_NAMES_CANDIDATES": ["100_OLYMP", "DCIM"], "FILE_DESTINATIONS": {".jpg": "Images/JPEG", ".jpeg": "Images/JPEG", ".orf": "Images/RAW", ".mov": "Videos", ".mp4": "Videos"}},
        "Canon": {"SD_FOLDER_NAMES_CANDIDATES": ["100CANON", "101CANON", "DCIM"], "FILE_DESTINATIONS": {".jpg": "Images/JPEG", ".jpeg": "Images/JPEG", ".cr2": "Images/RAW", ".cr3": "Images/RAW", ".dng": "Images/RAW", ".mov": "Videos", ".mp4": "Videos"}},
        "Hasselblad": {"SD_FOLDER_NAMES_CANDIDATES": ["DCIM", "HBL"], "FILE_DESTINATIONS": {".jpg": "Images/JPEG", ".jpeg": "Images/JPEG", ".3fr": "Images/RAW", ".dng": "Images/RAW", ".mp4": "Videos", ".mov": "Videos"}},
        "Leica": {"SD_FOLDER_NAMES_CANDIDATES": ["100LEICA", "101LEICA", "DCIM"], "FILE_DESTINATIONS": {".jpg": "Images/JPEG", ".dng": "Images/RAW", ".rwl": "Images/RAW", ".mp4": "Videos", ".mov": "Videos"}},
        "Lumix": {"SD_FOLDER_NAMES_CANDIDATES": ["100_PANA", "101_PANA", "DCIM"], "FILE_DESTINATIONS": {".jpg": "Images/JPEG", ".rw2": "Images/RAW", ".dng": "Images/RAW", ".mp4": "Videos", ".mov": "Videos"}},
        "Kodak": {"SD_FOLDER_NAMES_CANDIDATES": ["100KODAK", "DCIM"], "FILE_DESTINATIONS": {".jpg": "Images/JPEG", ".jpeg": "Images/JPEG", ".kdc": "Images/RAW", ".dng": "Images/RAW", ".mov": "Videos", ".mp4": "Videos"}},
        "Sony": {"SD_FOLDER_NAMES_CANDIDATES": ["100MSDCF", "101MSDCF", "DCIM"], "FILE_DESTINATIONS": {".jpg": "Images/JPEG", ".jpeg": "Images/JPEG", ".arw": "Images/RAW", ".dng": "Images/RAW", ".mp4": "Videos", ".mov": "Videos", ".m2ts": "Videos"}},
        "Pentax": {"SD_FOLDER_NAMES_CANDIDATES": ["100_PENTX", "101_PENTX", "DCIM"], "FILE_DESTINATIONS": {".jpg": "Images/JPEG", ".jpeg": "Images/JPEG", ".pef": "Images/RAW", ".dng": "Images/RAW", ".mov": "Videos", ".mp4": "Videos", ".avi": "Videos"}},
        "Sigma": {"SD_FOLDER_NAMES_CANDIDATES": ["100SIGMA", "DCIM"], "FILE_DESTINATIONS": {".jpg": "Images/JPEG", ".jpeg": "Images/JPEG", ".x3f": "Images/RAW", ".dng": "Images/RAW", ".mov": "Videos", ".mp4": "Videos"}},
        "GoPro": {"SD_FOLDER_NAMES_CANDIDATES": ["100GOPRO", "101GOPRO", "DCIM"], "FILE_DESTINATIONS": {".jpg": "Images/JPEG", ".jpeg": "Images/JPEG", ".gpr": "Images/RAW", ".mp4": "Videos", ".mov": "Videos", ".lrv": "Videos/LowResolution"}},
        "DJI": {"SD_FOLDER_NAMES_CANDIDATES": ["100MEDIA", "DCIM"], "FILE_DESTINATIONS": {".jpg": "Images/JPEG", ".jpeg": "Images/JPEG", ".dng": "Images/RAW", ".mp4": "Videos", ".mov": "Videos"}}
    }
}
"""
# =========================================================


def get_base_dir():
    """Get base directory for the application"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


BASE_DIR = get_base_dir()


def is_admin():
    """Check if running with admin privileges"""
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False


def run_as_admin():
    """Relaunch the application with admin privileges"""
    try:
        import ctypes
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
    except Exception as e:
        print(f"Error running as admin: {e}")


class WorkerThread(QThread):
    """Worker thread for file organization operations"""
    progress_updated = pyqtSignal(int, str)
    log_message = pyqtSignal(str)
    operation_finished = pyqtSignal(bool)

    def __init__(self, organizer, sd_full_path, topic, move_files=True):
        super().__init__()
        self.organizer = organizer
        self.sd_full_path = sd_full_path
        self.topic = topic
        self.move_files = move_files

    def run(self):
        """Execute the organization operation"""
        try:
            success = self.organizer.organize_sd_files(
                self.sd_full_path,
                topic=self.topic,
                move_files=self.move_files,
                progress_callback=lambda p, f: self.progress_updated.emit(p, f)
            )
            self.operation_finished.emit(success)
        except Exception as e:
            self.log_message.emit(f"ERROR: Unexpected error in worker thread: {e}")
            self.operation_finished.emit(False)


class MultiEventWorkerThread(QThread):
    """Worker thread for multi-event file organization operations"""
    progress_updated = pyqtSignal(int, str)
    log_message = pyqtSignal(str)
    operation_finished = pyqtSignal(bool)

    def __init__(self, organizer, sd_full_path, event_mapping, move_files=True):
        super().__init__()
        self.organizer = organizer
        self.sd_full_path = sd_full_path
        self.event_mapping = event_mapping
        self.move_files = move_files

    def run(self):
        """Execute the multi-event organization operation"""
        try:
            success = self.organizer.organize_sd_files_multi_event(
                self.sd_full_path,
                event_mapping=self.event_mapping,
                move_files=self.move_files,
                progress_callback=lambda p, f: self.progress_updated.emit(p, f)
            )
            self.operation_finished.emit(success)
        except Exception as e:
            self.log_message.emit(f"ERROR: Unexpected error in multi-event worker thread: {e}")
            self.operation_finished.emit(False)


class AdvancedConfigDialog(QDialog):
    """Dialog for advanced brand configuration"""
    
    def __init__(self, parent=None, config=None, brand=None):
        super().__init__(parent)
        self.setWindowTitle(f"Advanced Configuration for {brand}")
        self.setMinimumWidth(500)
        self.config = config
        self.brand = brand
        self.layout = QVBoxLayout(self)
        
        if self.config:
            self.setup_ui()
            self.load_config_data()

    def setup_ui(self):
        """Setup the UI for advanced configuration"""
        # SD Folder Names Section
        sd_group = QGroupBox("SD Card Candidate Folders")
        sd_layout = QFormLayout()
        self.sd_folders_edit = QLineEdit()
        self.sd_folders_edit.setToolTip("Enter folder names, separated by commas")
        sd_layout.addRow("Folder Names:", self.sd_folders_edit)
        sd_group.setLayout(sd_layout)
        
        # File Destinations Section
        dest_group = QGroupBox("File Destinations by Extension")
        dest_layout = QVBoxLayout()
        self.dest_list = QListWidget()
        dest_layout.addWidget(self.dest_list)
        
        # Buttons for managing destinations
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add")
        self.edit_btn = QPushButton("Edit")
        self.remove_btn = QPushButton("Remove")
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.remove_btn)
        dest_layout.addLayout(btn_layout)
        dest_group.setLayout(dest_layout)
        
        # Dialog buttons
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        
        self.layout.addWidget(sd_group)
        self.layout.addWidget(dest_group)
        self.layout.addWidget(self.button_box)
        
        # Connect signals
        self.button_box.accepted.connect(self.save_config_and_accept)
        self.button_box.rejected.connect(self.reject)
        self.add_btn.clicked.connect(self.add_destination)
        self.edit_btn.clicked.connect(self.edit_destination)
        self.remove_btn.clicked.connect(self.remove_destination)

    def load_config_data(self):
        """Load configuration data into the UI"""
        self.sd_folders_edit.setText(
            ", ".join(self.config.get("SD_FOLDER_NAMES_CANDIDATES", []))
        )
        self.dest_list.clear()
        for ext, path in self.config.get("FILE_DESTINATIONS", {}).items():
            self.dest_list.addItem(f"{ext} → {path}")
    
    def add_destination(self):
        """Add a new destination"""
        self.edit_destination(add_new=True)

    def edit_destination(self, add_new=False):
        """Edit or add a destination"""
        item = None if add_new else self.dest_list.currentItem()
        if not add_new and not item:
            QMessageBox.warning(self, "Selection Required", "Please select an item to edit.")
            return
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Destination" if not add_new else "Add Destination")
        form = QFormLayout(dialog)
        
        ext_edit = QLineEdit()
        path_edit = QLineEdit()
        
        if not add_new and ' → ' in item.text():
            ext, path = item.text().split(' → ', 1)
            ext_edit.setText(ext)
            path_edit.setText(path)
        
        form.addRow("Extension (e.g., .jpg):", ext_edit)
        form.addRow("Subfolder (e.g., Images/RAW):", path_edit)
        
        btn_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        form.addWidget(btn_box)
        btn_box.accepted.connect(dialog.accept)
        btn_box.rejected.connect(dialog.reject)
        
        if dialog.exec():
            ext = ext_edit.text().strip().lower()
            path = path_edit.text().strip()
            
            if not ext.startswith('.'):
                ext = '.' + ext
            
            if not add_new:
                item.setText(f"{ext} → {path}")
            else:
                self.dest_list.addItem(f"{ext} → {path}")

    def remove_destination(self):
        """Remove a destination"""
        item = self.dest_list.currentItem()
        if item:
            self.dest_list.takeItem(self.dest_list.row(item))
        else:
            QMessageBox.warning(self, "Selection Required", "Please select an item to remove.")

    def save_config_and_accept(self):
        """Handle save configuration (temporary warning)"""
        QMessageBox.warning(
            self, 
            "Warning", 
            "Configuration is embedded in the application. Changes made here are "
            "temporary and will not be saved permanently."
        )
        self.reject()


class UserManualDialog(QDialog):
    """Manuale utente completo in italiano"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("SD Organizer - Manuale Utente")
        self.setMinimumSize(900, 700)
        
        layout = QVBoxLayout(self)
        
        # Create tabs for different sections
        tabs = QTabWidget()
        
        # Tab 1: Getting Started
        tabs.addTab(self._create_getting_started_tab(), "🚀 Iniziare")
        
        # Tab 2: Basic Usage
        tabs.addTab(self._create_basic_usage_tab(), "📸 Uso Base")
        
        # Tab 3: Multi-Event Import
        tabs.addTab(self._create_multi_event_tab(), "📅 Multi-Evento")
        
        # Tab 4: Advanced Features
        tabs.addTab(self._create_advanced_tab(), "⚙️ Avanzate")
        
        # Tab 5: Troubleshooting
        tabs.addTab(self._create_troubleshooting_tab(), "🔧 Risoluzione Problemi")
        
        layout.addWidget(tabs)
        
        # Close button
        close_btn = QPushButton("Chiudi")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
    
    def _create_getting_started_tab(self):
        """Crea tab per iniziare"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        text = QTextEdit()
        text.setReadOnly(True)
        text.setHtml("""
        <h1>🚀 Iniziare con SD Organizer</h1>
        
        <h2>Cos'è SD Organizer?</h2>
        <p>SD Organizer è uno strumento professionale per organizzare foto e video dalla scheda SD della tua fotocamera. 
        Ordina automaticamente i file per data, li rinomina intelligentemente e mantiene un database per ricerche facili.</p>
        
        <h2>📋 Requisiti</h2>
        <ul>
            <li><b>Python 3.8+</b> installato sul sistema</li>
            <li><b>Pacchetti richiesti:</b> PyQt6, Pillow, psutil</li>
            <li><b>Opzionale:</b> rawpy e imageio per conversione file RAW</li>
        </ul>
        
        <h2>🔧 Installazione</h2>
        <ol>
            <li>Estrai la cartella SD_Organizer nella posizione desiderata</li>
            <li>Apri un terminale/prompt dei comandi nella cartella</li>
            <li>Installa le dipendenze:
                <pre>pip install PyQt6 Pillow psutil</pre>
            </li>
            <li>Avvia l'applicazione:
                <pre>python main_app.py</pre>
            </li>
        </ol>
        
        <h2>🎯 Configurazione Iniziale</h2>
        <ol>
            <li><b>Seleziona Marca Fotocamera:</b> Scegli la marca della tua fotocamera dal menu</li>
            <li><b>Imposta Percorso Destinazione:</b> Clicca "Browse..." per selezionare dove salvare le foto organizzate</li>
            <li><b>Inserisci Scheda SD:</b> Inserisci la scheda SD della fotocamera</li>
            <li><b>Clicca "Refresh SD Card List":</b> Rileva la tua scheda SD</li>
            <li><b>Pronto per organizzare!</b> Sei pronto!</li>
        </ol>
        
        <h2>💡 Suggerimenti Rapidi</h2>
        <ul>
            <li>✓ Fai sempre backup della scheda SD prima del primo utilizzo</li>
            <li>✓ La cartella di destinazione viene creata automaticamente se non esiste</li>
            <li>✓ L'applicazione crea una sottocartella per ogni evento/data</li>
            <li>✓ Le date originali dei file sono preservate nei dati EXIF</li>
        </ul>
        """)
        layout.addWidget(text)
        return widget
    
    def _create_basic_usage_tab(self):
        """Crea tab uso base"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        text = QTextEdit()
        text.setReadOnly(True)
        text.setHtml("""
        <h1>📸 Uso Base</h1>
        
        <h2>Processo di Importazione Standard</h2>
        
        <h3>Passo 1: Configurazione</h3>
        <ol>
            <li><b>Seleziona Marca Fotocamera:</b> Scegli dal menu (es. Nikon, Canon, Sony)</li>
            <li><b>Inserisci Scheda SD:</b> Collega la scheda di memoria della fotocamera</li>
            <li><b>Clicca "Refresh SD Card List":</b> Rileva le schede SD disponibili</li>
            <li><b>Seleziona Scheda SD:</b> Scegli la tua scheda dal menu</li>
            <li><b>Imposta Destinazione:</b> Naviga dove vuoi salvare le foto</li>
            <li><b>Inserisci Nome Evento:</b> Digita il nome evento (es. "Compleanno_Marco", "Viaggio_Italia_2025")</li>
        </ol>
        
        <h3>Passo 2: Importazione</h3>
        <ul>
            <li><b>"Organize & Move":</b> Sposta i file dalla SD (libera spazio)</li>
            <li><b>"Copy Only":</b> Copia i file (mantiene originali sulla SD)</li>
        </ul>
        
        <h3>Passo 3: Monitora Progresso</h3>
        <p>Osserva la barra di progresso e il log per:</p>
        <ul>
            <li>✓ File in elaborazione</li>
            <li>✓ Stato operazione corrente</li>
            <li>✓ Eventuali avvisi o errori</li>
            <li>✓ Messaggio di completamento</li>
        </ul>
        
        <h2>🗂️ Come Sono Organizzati i File</h2>
        
        <h3>Struttura Cartelle</h3>
        <pre>
Destinazione/
  └── NomeEvento/
      └── YYYY-MM-DD_Mese/
          ├── IMG_0001_20251016_153045.jpg
          ├── IMG_0002_20251016_153102.jpg
          └── VID_0001_20251016_154530.mp4
        </pre>
        
        <h3>Convenzione Nome File</h3>
        <p><b>Formato:</b> <code>PREFISSO_NNNN_YYYYMMDD_HHMMSS.est</code></p>
        <ul>
            <li><b>PREFISSO:</b> IMG per foto, VID per video</li>
            <li><b>NNNN:</b> Numero sequenziale (0001, 0002, ...)</li>
            <li><b>YYYYMMDD:</b> Data di scatto</li>
            <li><b>HHMMSS:</b> Ora di scatto</li>
            <li><b>est:</b> Estensione file originale</li>
        </ul>
        
        <p><b>Esempio:</b> <code>IMG_0042_20251016_153045.jpg</code></p>
        <ul>
            <li>Foto #42</li>
            <li>Scattata il 16 ottobre 2025</li>
            <li>Alle 15:30:45</li>
        </ul>
        
        <h2>🔄 Annulla Operazione</h2>
        <p>Se devi annullare l'ultima importazione:</p>
        <ol>
            <li>Clicca <b>"Choose Undo Log..."</b></li>
            <li>Seleziona il file di log annullamento</li>
            <li>Clicca <b>"Undo Last Operation"</b></li>
            <li>I file verranno ripristinati nella posizione originale</li>
        </ol>
        
        <h2>⚠️ Note Importanti</h2>
        <ul>
            <li>✓ Assicurati sempre di avere spazio su disco sufficiente prima di importare</li>
            <li>✓ L'operazione "Move" elimina i file dalla SD dopo il trasferimento riuscito</li>
            <li>✓ L'operazione "Copy" è più sicura per utenti alle prime armi</li>
            <li>✓ I log di annullamento sono salvati nella cartella logs di destinazione</li>
        </ul>
        """)
        layout.addWidget(text)
        return widget
    
    def _create_multi_event_tab(self):
        """Crea tab importazione multi-evento"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        text = QTextEdit()
        text.setReadOnly(True)
        text.setHtml("""
        <h1>📅 Importazione Multi-Evento</h1>
        
        <h2>Cos'è l'Importazione Multi-Evento?</h2>
        <p>L'Importazione Multi-Evento permette di organizzare foto da <b>eventi multipli</b> sulla stessa scheda SD 
        con <b>nomi evento diversi</b> per ogni data.</p>
        
        <h2>Quando Si Attiva?</h2>
        <p>Il dialog multi-evento appare <b>automaticamente</b> quando:</p>
        <ol>
            <li>Clicchi "Refresh SD Card List"</li>
            <li>Poi clicchi "Organize & Move" (o "Copy Only")</li>
            <li><b>E</b> la tua scheda SD contiene foto da <b>2 o più date diverse</b></li>
        </ol>
        
        <h2>📊 Esempio Scenario</h2>
        <p><b>La tua scheda SD contiene:</b></p>
        <ul>
            <li>50 foto del 10 ottobre 2025 (Matrimonio)</li>
            <li>30 foto dell'11 ottobre 2025 (Festa compleanno)</li>
            <li>20 foto del 12 ottobre 2025 (Gita al mare)</li>
        </ul>
        
        <p>→ Il dialog multi-evento apparirà con una tabella che mostra:</p>
        <table border="1" cellpadding="5" style="border-collapse: collapse;">
            <tr bgcolor="#e0e0e0">
                <th>Data</th>
                <th>Giorno</th>
                <th>File</th>
                <th>Nome Evento</th>
            </tr>
            <tr>
                <td>2025-10-10</td>
                <td>Venerdì</td>
                <td>50 file</td>
                <td><i>[Tu inserisci: Matrimonio_Maria]</i></td>
            </tr>
            <tr>
                <td>2025-10-11</td>
                <td>Sabato</td>
                <td>30 file</td>
                <td><i>[Tu inserisci: Compleanno_Luca]</i></td>
            </tr>
            <tr>
                <td>2025-10-12</td>
                <td>Domenica</td>
                <td>20 file</td>
                <td><i>[Tu inserisci: Gita_Mare]</i></td>
            </tr>
        </table>
        
        <h2>🎯 Come Usare il Dialog Multi-Evento</h2>
        
        <h3>1. Rivedi le Date</h3>
        <p>Il dialog mostra tutte le date trovate sulla tua scheda SD con il conteggio file.</p>
        
        <h3>2. Inserisci Nomi Eventi</h3>
        <p>Clicca su ogni cella "Nome Evento" e digita il nome evento per quella data.</p>
        <ul>
            <li>✓ Usa nomi descrittivi: "Matrimonio_Maria", "Viaggio_Roma_Giorno1"</li>
            <li>✓ Evita caratteri speciali: usa underscore invece di spazi</li>
            <li>✓ Puoi lasciare celle vuote (i file saranno chiamati "Uncategorized")</li>
        </ul>
        
        <h3>3. Azioni Rapide (Opzionali)</h3>
        <ul>
            <li><b>"Use Same Name for All":</b> Applica un solo nome evento a tutte le date</li>
            <li><b>"Auto-name by Date":</b> Nomina automaticamente gli eventi come "Event_2025_10_10"</li>
            <li><b>"Clear All":</b> Cancella tutti i nomi eventi per ricominciare</li>
        </ul>
        
        <h3>4. Avvia Importazione</h3>
        <p>Clicca <b>"Start Import"</b> quando pronto. Ogni data sarà organizzata nella propria cartella evento.</p>
        
        <h2>📁 Struttura Risultato</h2>
        <pre>
Destinazione/
  ├── Matrimonio_Maria/
  │   └── 2025-10-10_October/
  │       ├── IMG_0001_20251010_140000.jpg
  │       └── IMG_0002_20251010_140015.jpg
  │
  ├── Compleanno_Luca/
  │   └── 2025-10-11_October/
  │       ├── IMG_0003_20251011_180000.jpg
  │       └── IMG_0004_20251011_180030.jpg
  │
  └── Gita_Mare/
      └── 2025-10-12_October/
          ├── IMG_0005_20251012_100000.jpg
          └── IMG_0006_20251012_100045.jpg
        </pre>
        
        <h2>💡 Suggerimenti per Importazione Multi-Evento</h2>
        <ul>
            <li>✓ <b>Sii specifico:</b> Usa nomi evento chiari per trovare foto facilmente dopo</li>
            <li>✓ <b>Coerenza:</b> Usa pattern di denominazione simili (es. Luogo_Evento_Anno)</li>
            <li>✓ <b>Nessuna pressione:</b> Puoi sempre re-importare con nomi diversi usando annulla</li>
            <li>✓ <b>Celle vuote:</b> Le foto senza nome evento vanno nella cartella "Uncategorized"</li>
        </ul>
        
        <h2>🚫 Rilevamento Data Singola</h2>
        <p><b>Se tutte le foto sono da UNA sola data:</b></p>
        <p>→ Il dialog multi-evento NON apparirà<br>
        → Usa invece il campo standard "Event/Topic Name"<br>
        → Il processo continua normalmente</p>
        """)
        layout.addWidget(text)
        return widget
    
    def _create_advanced_tab(self):
        """Create advanced features tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        text = QTextEdit()
        text.setReadOnly(True)
        text.setHtml("""
        <h1>⚙️ Funzionalità Avanzate</h1>
        
        <h2>🗄️ Integrazione Database</h2>
        <p>SD Organizer mantiene un database SQLite con metadati foto per potenti capacità di ricerca.</p>
        
        <h3>Cosa è Memorizzato nel Database?</h3>
        <ul>
            <li>📁 File path and name</li>
            <li>📅 Date and time taken</li>
            <li>📷 Camera make and model</li>
            <li>⚙️ Camera settings (ISO, aperture, shutter speed)</li>
            <li>🔍 Lens information</li>
            <li>🌍 GPS coordinates (if available)</li>
            <li>🏷️ Event name and tags</li>
            <li>⭐ Rating (can be added later)</li>
        </ul>
        
        <h3>Posizione Database</h3>
        <p><code>~/.sd_organizer/photo_catalog.db</code></p>
        <p>(Hidden folder in your home directory)</p>
        
        <h2>🎨 Strumenti Elaborazione Immagini</h2>
        
        <h3>Rotazione Automatica</h3>
        <p>Ruota automaticamente le foto basandosi sui dati EXIF di orientamento.</p>
        <ul>
            <li>✓ Fixes sideways photos from vertical shots</li>
            <li>✓ Preserves original quality</li>
            <li>✓ Updates EXIF data accordingly</li>
        </ul>
        
        <h3>Conversione RAW (Opzionale)</h3>
        <p>Converte file RAW in JPEG per visualizzazione facilitata.</p>
        <ul>
            <li>Requires: <code>pip install rawpy imageio</code></li>
            <li>Supported formats: NEF, CR2, ARW, DNG, etc.</li>
            <li>Preserves original RAW file</li>
            <li>Creates high-quality JPEG copy</li>
        </ul>
        
        <h2>⚙️ Configurazione Avanzata</h2>
        <p>Click <b>"Advanced Config"</b> button to customize:</p>
        
        <h3>Estensioni File</h3>
        <ul>
            <li>Supported photo formats</li>
            <li>Supported video formats</li>
            <li>Custom extensions</li>
        </ul>
        
        <h3>Pattern Denominazione</h3>
        <ul>
            <li>Photo prefix (default: IMG)</li>
            <li>Video prefix (default: VID)</li>
            <li>Sequential numbering start</li>
        </ul>
        
        <h3>Opzioni Elaborazione</h3>
        <ul>
            <li>Enable/disable auto-rotation</li>
            <li>JPEG quality settings</li>
            <li>Thumbnail generation</li>
            <li>Watermark settings</li>
        </ul>
        
        <h2>🤖 Servizio Auto-Import</h2>
        <p>Rileva e importa automaticamente le foto quando la scheda SD è inserita.</p>
        
        <h3>Come Abilitare</h3>
        <ol>
            <li>Configure rules in Advanced Config</li>
            <li>Set default event naming pattern</li>
            <li>Enable "Auto-import on detection"</li>
            <li>Service monitors for SD card insertion</li>
        </ol>
        
        <h3>Funzionalità di Sicurezza</h3>
        <ul>
            <li>✓ Checks free disk space before importing</li>
            <li>✓ Verifies file integrity after transfer</li>
            <li>✓ Creates automatic backups</li>
            <li>✓ Logs all operations</li>
        </ul>
        
        <h2>📊 Log e Monitoraggio</h2>
        
        <h3>Tipi di Log</h3>
        <ul>
            <li><b>Operation logs:</b> Detailed record of all imports</li>
            <li><b>Undo logs:</b> Information needed to reverse operations</li>
            <li><b>Error logs:</b> Problems encountered during processing</li>
        </ul>
        
        <h3>Visualizza Log</h3>
        <p>Click <b>"Open Log Folder"</b> to access all log files.</p>
        
        <h2>🎨 Temi</h2>
        <p>Personalizza l'aspetto dell'applicazione:</p>
        <ul>
            <li><b>Cool Ocean</b> (Default - Blue theme)</li>
            <li><b>Dark Mode</b> (Easy on eyes)</li>
            <li><b>Forest</b> (Green theme)</li>
            <li><b>Sunset</b> (Warm orange theme)</li>
            <li><b>Professional</b> (Minimalist gray)</li>
        </ul>
        <p>La selezione del tema è salvata e persiste tra le sessioni.</p>
        """)
        layout.addWidget(text)
        return widget
    
    def _create_troubleshooting_tab(self):
        """Create troubleshooting tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        text = QTextEdit()
        text.setReadOnly(True)
        text.setHtml("""
        <h1>🔧 Risoluzione Problemi</h1>
        
        <h2>❌ Problemi Comuni</h2>
        
        <h3>1. "Scheda SD non rilevata"</h3>
        <p><b>Soluzioni:</b></p>
        <ul>
            <li>✓ Ensure SD card is properly inserted</li>
            <li>✓ Try a different USB port</li>
            <li>✓ Check if SD card is readable in File Explorer</li>
            <li>✓ Click "Refresh SD Card List" again</li>
            <li>✓ Restart the application</li>
        </ul>
        
        <h3>2. Errori "Permesso negato"</h3>
        <p><b>Windows:</b></p>
        <ul>
            <li>Run application as Administrator</li>
            <li>Check destination folder is not write-protected</li>
        </ul>
        <p><b>Mac/Linux:</b></p>
        <ul>
            <li>Check folder permissions: <code>chmod 755 /path/to/folder</code></li>
            <li>Ensure you own the destination folder</li>
        </ul>
        
        <h3>3. "Spazio su disco insufficiente"</h3>
        <p><b>Soluzioni:</b></p>
        <ul>
            <li>Free up space on destination drive</li>
            <li>Choose a different destination with more space</li>
            <li>Use "Copy Only" and manually delete SD card later</li>
        </ul>
        
        <h3>4. "Nessun file compatibile trovato"</h3>
        <p><b>Possible causes:</b></p>
        <ul>
            <li>Wrong SD card selected</li>
            <li>Files are in unsupported format</li>
            <li>Camera brand configuration incorrect</li>
        </ul>
        <p><b>Soluzioni:</b></p>
        <ul>
            <li>Verify correct brand is selected</li>
            <li>Check Advanced Config for supported extensions</li>
            <li>Manually inspect SD card contents</li>
        </ul>
        
        <h3>5. "Dialog multi-evento non appare"</h3>
        <p><b>Questo è normale se:</b></p>
        <ul>
            <li>All photos are from the same date</li>
            <li>SD card has no date metadata</li>
        </ul>
        <p><b>Soluzione:</b></p>
        <ul>
            <li>Use standard event name field instead</li>
            <li>Import will work normally</li>
        </ul>
        
        <h2>🐛 Strumenti Debug</h2>
        
        <h3>Avvia con Modalità Debug</h3>
        <pre>python launch_with_debug.py</pre>
        <p>Fornisce logging dettagliato di tutte le operazioni.</p>
        
        <h3>Verifica Signature</h3>
        <pre>python verify_signature.py</pre>
        <p>Controlla se tutti i componenti sono configurati correttamente.</p>
        
        <h3>Test Moduli</h3>
        <pre>python test_modules.py</pre>
        <p>Esegue test completi su tutti i moduli.</p>
        
        <h2>📝 File di Log</h2>
        <p><b>Posizione:</b> Clicca il pulsante "Open Log Folder"</p>
        <p><b>Controlla i log per:</b></p>
        <ul>
            <li>Error messages</li>
            <li>Stack traces</li>
            <li>Operation details</li>
            <li>Timestamp of issues</li>
        </ul>
        
        <h2>🔄 Reset Applicazione</h2>
        
        <h3>Cancella Database</h3>
        <p>Delete: <code>~/.sd_organizer/photo_catalog.db</code></p>
        <p>Database will be recreated on next launch.</p>
        
        <h3>Reset Preferenze</h3>
        <p>Delete: <code>preferences.json</code> in app folder</p>
        <p>Preferences reset to defaults.</p>
        
        <h3>Reset Configurazione</h3>
        <p>Restore: <code>config.json</code> from backup or re-extract app</p>
        
        <h2>💡 Suggerimenti Prestazioni</h2>
        <ul>
            <li>✓ Close other applications during large imports</li>
            <li>✓ Use SSD for destination folder (faster)</li>
            <li>✓ Keep SD card clean and formatted regularly</li>
            <li>✓ Update to latest version of SD Organizer</li>
        </ul>
        
        <h2>❓ Ottenere Aiuto</h2>
        <p><b>Hai ancora problemi?</b></p>
        <ul>
            <li>Check log files for error details</li>
            <li>Run debug tools to diagnose</li>
            <li>Document the exact error message</li>
            <li>Note steps to reproduce the issue</li>
        </ul>
        
        <p><b>Informazioni Sistema da Includere:</b></p>
        <ul>
            <li>Operating System and version</li>
            <li>Python version</li>
            <li>SD Organizer version</li>
            <li>Camera brand/model</li>
            <li>Error message from log</li>
        </ul>
        """)
        layout.addWidget(text)
        return widget


class AboutDialog(QDialog):
    """About and credits dialog"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Informazioni SD Organizer")
        self.setMinimumSize(700, 600)
        
        layout = QVBoxLayout(self)
        
        # Logo/Title area
        title_label = QLabel("<h1>📸 SD Organizer V3</h1>")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        subtitle_label = QLabel("<h3>Strumento Professionale per Organizzazione Foto e Video</h3>")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle_label)
        
        # Version info
        version_label = QLabel("<p><b>Versione:</b> 3.3 Final Fixed + Debug Tools<br>"
                              "<b>Data Rilascio:</b> 16 Ottobre 2025<br>"
                              "<b>Build:</b> Pronto per Produzione</p>")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version_label)
        
        layout.addSpacing(20)
        
        # Tabs for different info sections
        tabs = QTabWidget()
        
        # Credits tab
        credits_widget = QWidget()
        credits_layout = QVBoxLayout(credits_widget)
        credits_text = QTextEdit()
        credits_text.setReadOnly(True)
        credits_text.setHtml("""
        <h2>👨‍💻 Development</h2>
        <p><b>Lead Developer:</b> Dmitr (with AI assistance)<br>
        <b>AI Assistant:</b> Claude (Anthropic)<br>
        <b>Development Period:</b> October 2025</p>
        
        <h2>🙏 Acknowledgments</h2>
        <p>This project was developed with the assistance of Claude AI, an AI assistant by Anthropic. 
        The collaboration between human creativity and AI capabilities made this comprehensive tool possible.</p>
        
        <h2>🛠️ Technologies Used</h2>
        <ul>
            <li><b>Python 3.8+</b> - Core programming language</li>
            <li><b>PyQt6</b> - Graphical user interface framework</li>
            <li><b>Pillow (PIL)</b> - Image processing</li>
            <li><b>psutil</b> - System and drive detection</li>
            <li><b>SQLite</b> - Database management</li>
            <li><b>rawpy</b> (optional) - RAW image processing</li>
            <li><b>imageio</b> (optional) - Image I/O operations</li>
        </ul>
        
        <h2>📚 Open Source Libraries</h2>
        <p>Special thanks to all open-source contributors whose libraries made this project possible:</p>
        <ul>
            <li>The PyQt/Qt team for excellent GUI framework</li>
            <li>PIL/Pillow contributors for image processing capabilities</li>
            <li>Python Software Foundation for the amazing language</li>
            <li>All package maintainers and contributors</li>
        </ul>
        
        <h2>💝 Special Thanks</h2>
        <ul>
            <li>Beta testers who provided valuable feedback</li>
            <li>Photography community for feature suggestions</li>
            <li>Users who reported bugs and helped improve the software</li>
        </ul>
        """)
        credits_layout.addWidget(credits_text)
        tabs.addTab(credits_widget, "Crediti")
        
        # Features tab
        features_widget = QWidget()
        features_layout = QVBoxLayout(features_widget)
        features_text = QTextEdit()
        features_text.setReadOnly(True)
        features_text.setHtml("""
        <h2>✨ Key Features</h2>
        
        <h3>📸 Intelligent Organization</h3>
        <ul>
            <li>Automatic date-based folder structure</li>
            <li>Smart file renaming with timestamps</li>
            <li>Multi-event import for cards with multiple dates</li>
            <li>Support for photos and videos</li>
        </ul>
        
        <h3>📅 Multi-Event Import</h3>
        <ul>
            <li>Automatically detects multiple dates on SD card</li>
            <li>Assign different event names to different dates</li>
            <li>Visual table for easy event management</li>
            <li>Quick actions for bulk naming</li>
        </ul>
        
        <h3>🗄️ Database Integration</h3>
        <ul>
            <li>SQLite database for photo cataloging</li>
            <li>Comprehensive EXIF data extraction</li>
            <li>Advanced search capabilities</li>
            <li>Statistics and analytics</li>
        </ul>
        
        <h3>🎨 Image Processing</h3>
        <ul>
            <li>Auto-rotation based on EXIF orientation</li>
            <li>RAW to JPEG conversion (optional)</li>
            <li>Watermark addition</li>
            <li>Batch resize operations</li>
        </ul>
        
        <h3>🔧 Advanced Features</h3>
        <ul>
            <li>Undo functionality for all operations</li>
            <li>Comprehensive logging system</li>
            <li>Multiple camera brand support</li>
            <li>Configurable file extensions</li>
            <li>Theme customization</li>
        </ul>
        
        <h3>🤖 Automation</h3>
        <ul>
            <li>Auto-import service</li>
            <li>Rule-based processing</li>
            <li>Batch operations</li>
            <li>Scheduled imports</li>
        </ul>
        
        <h3>🛡️ Safety Features</h3>
        <ul>
            <li>Disk space verification</li>
            <li>File integrity checking</li>
            <li>Safe undo operations</li>
            <li>Detailed error reporting</li>
        </ul>
        """)
        features_layout.addWidget(features_text)
        tabs.addTab(features_widget, "Funzionalità")
        
        # License tab
        license_widget = QWidget()
        license_layout = QVBoxLayout(license_widget)
        license_text = QTextEdit()
        license_text.setReadOnly(True)
        license_text.setHtml("""
        <h2>📄 License</h2>
        
        <h3>SD Organizer</h3>
        <p>This software is provided as-is for personal and professional use.</p>
        
        <h3>Terms of Use</h3>
        <ul>
            <li>✓ Free for personal use</li>
            <li>✓ Free for commercial photography businesses</li>
            <li>✓ Modify and customize as needed</li>
            <li>✓ Share with others</li>
        </ul>
        
        <h3>Disclaimer</h3>
        <p><b>No Warranty:</b> This software is provided "as is" without warranty of any kind, 
        either expressed or implied. The entire risk as to the quality and performance of 
        the software is with you.</p>
        
        <p><b>Limitation of Liability:</b> In no event will the developers be liable for any damages 
        including lost data, lost profits, or other incidental or consequential damages arising 
        out of the use or inability to use this software.</p>
        
        <h3>Recommendations</h3>
        <ul>
            <li>⚠️ Always backup your photos before processing</li>
            <li>⚠️ Test with a small set of files first</li>
            <li>⚠️ Verify imports completed successfully</li>
            <li>⚠️ Keep original SD card data until confirmed</li>
        </ul>
        
        <h3>Third-Party Licenses</h3>
        <p>This software uses open-source libraries, each with their own licenses:</p>
        <ul>
            <li><b>PyQt6:</b> GPL v3 / Commercial License</li>
            <li><b>Pillow:</b> PIL License (similar to MIT)</li>
            <li><b>psutil:</b> BSD License</li>
            <li><b>Python:</b> PSF License</li>
        </ul>
        
        <p>Please refer to each library's documentation for complete license information.</p>
        
        <h3>Privacy</h3>
        <p>SD Organizer:</p>
        <ul>
            <li>✓ Does NOT collect any user data</li>
            <li>✓ Does NOT send data over the internet</li>
            <li>✓ Operates entirely offline</li>
            <li>✓ All data stays on your computer</li>
        </ul>
        """)
        license_layout.addWidget(license_text)
        tabs.addTab(license_widget, "Licenza")
        
        # System info tab
        system_widget = QWidget()
        system_layout = QVBoxLayout(system_widget)
        system_text = QTextEdit()
        system_text.setReadOnly(True)
        
        # Gather system info
        import sys
        import platform
        system_info = f"""
        <h2>💻 System Information</h2>
        
        <h3>Application</h3>
        <ul>
            <li><b>Version:</b> 3.3 Final Fixed + Debug Tools</li>
            <li><b>Build Date:</b> October 16, 2025</li>
            <li><b>Installation Path:</b> {os.path.dirname(os.path.abspath(__file__))}</li>
        </ul>
        
        <h3>Python Environment</h3>
        <ul>
            <li><b>Python Version:</b> {sys.version}</li>
            <li><b>Platform:</b> {platform.system()} {platform.release()}</li>
            <li><b>Architecture:</b> {platform.machine()}</li>
        </ul>
        
        <h3>Installed Modules</h3>
        <ul>
            <li><b>PyQt6:</b> Installed ✓</li>
            <li><b>Pillow:</b> Installed ✓</li>
            <li><b>psutil:</b> Installed ✓</li>
        </ul>
        
        <h3>Optional Modules</h3>
        <ul>
        """
        
        try:
            import rawpy
            system_info += "<li><b>rawpy:</b> Installed ✓ (RAW conversion available)</li>"
        except ImportError:
            system_info += "<li><b>rawpy:</b> Not installed (RAW conversion unavailable)</li>"
        
        try:
            import imageio
            system_info += "<li><b>imageio:</b> Installed ✓</li>"
        except ImportError:
            system_info += "<li><b>imageio:</b> Not installed</li>"
        
        system_info += """
        </ul>
        
        <h3>Database</h3>
        <ul>
            <li><b>Type:</b> SQLite</li>
            <li><b>Location:</b> ~/.sd_organizer/photo_catalog.db</li>
        </ul>
        """
        
        system_text.setHtml(system_info)
        system_layout.addWidget(system_text)
        tabs.addTab(system_widget, "Info Sistema")
        
        layout.addWidget(tabs)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)


class SDOrganizerApp(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SD Organizer - Photo & Video Manager")
        self.setMinimumSize(900, 750)
        
        self.organizer = None
        self.full_config = None
        self.worker = None
        
        self._load_preferences()
        self._load_config_internal()
        self._init_ui()
        self._apply_theme(self.preferred_theme)

    def _create_menu_bar(self):
        """Create menu bar with Help menu"""
        menubar = self.menuBar()
        
        # Help Menu
        help_menu = menubar.addMenu("&Aiuto")
        
        # User Manual
        manual_action = help_menu.addAction("📖 Manuale Utente")
        manual_action.setShortcut("F1")
        manual_action.triggered.connect(self._show_user_manual)
        
        # About & Credits
        about_action = help_menu.addAction("ℹ️ Informazioni e Crediti")
        about_action.triggered.connect(self._show_about)
        
        help_menu.addSeparator()
        
        # Multi-Event Info
        multi_info_action = help_menu.addAction("📅 Info Importazione Multi-Evento")
        multi_info_action.triggered.connect(self._show_multi_event_info)
    
    def _show_multi_event_info(self):
        """Show information about multi-event import"""
        QMessageBox.information(
            self,
            "Importazione Multi-Evento",
            "<h3>📅 Funzionalità Importazione Multi-Evento</h3>"
            "<p><b>Quando appare il dialog multi-evento?</b></p>"
            "<p>Il dialog di importazione multi-evento appare <b>automaticamente</b> quando:</p>"
            "<ul>"
            "<li>✓ Clicchi <b>'Refresh SD Card List'</b></li>"
            "<li>✓ Poi clicchi <b>'Organize & Move'</b> (o 'Copy Only')</li>"
            "<li>✓ E la tua scheda SD contiene foto scattate in <b>DATE MULTIPLE</b></li>"
            "</ul>"
            "<p><b>E se ho foto da una singola data?</b></p>"
            "<p>Se tutte le foto sono dalla stessa data, viene usato il processo di importazione standard. "
            "Semplicemente inserisci il nome evento nel campo 'Event/Topic Name'.</p>"
            "<p><b>Esempio:</b></p>"
            "<ul>"
            "<li>Foto solo del 2025-10-10 → Importazione normale</li>"
            "<li>Foto del 2025-10-10 E 2025-10-11 → Appare dialog multi-evento</li>"
            "</ul>"
        )
    
    def _show_user_manual(self):
        """Show comprehensive user manual"""
        manual = UserManualDialog(self)
        manual.exec()
    
    def _show_about(self):
        """Show about and credits dialog"""
        about = AboutDialog(self)
        about.exec()

    def _init_ui(self):
        """Initialize the user interface"""
        # Create menu bar
        self._create_menu_bar()
        
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        
        # === 1. Setup Group ===
        setup_group = QGroupBox("1. Setup")
        setup_form = QFormLayout()
        
        # Brand selection
        self.brand_combo = QComboBox()
        if self.full_config and "CONFIGURATIONS" in self.full_config:
            brand_names = sorted(self.full_config["CONFIGURATIONS"].keys())
            self.brand_combo.addItems(brand_names)
        self.brand_combo.currentTextChanged.connect(self._on_brand_changed)
        setup_form.addRow("Select Camera Brand:", self.brand_combo)
        
        # SD Card selection
        self.sd_combo = QComboBox()
        self.sd_combo.setPlaceholderText("Click 'Refresh SD'...")
        setup_form.addRow("Detected SD Card:", self.sd_combo)
        
        # Destination path
        dest_layout = QHBoxLayout()
        self.dest_path_edit = QLineEdit()
        self.browse_dest_btn = QPushButton("Browse...")
        self.browse_dest_btn.clicked.connect(self._browse_destination)
        dest_layout.addWidget(self.dest_path_edit)
        dest_layout.addWidget(self.browse_dest_btn)
        setup_form.addRow("Destination Path:", dest_layout)
        
        # Topic/Event name
        self.topic_edit = QLineEdit()
        self.topic_edit.setPlaceholderText("e.g., Compleanno, Viaggio_Roma, etc.")
        setup_form.addRow("Event/Topic Name:", self.topic_edit)
        
        setup_group.setLayout(setup_form)
        main_layout.addWidget(setup_group)
        
        # === 2. Actions Group ===
        actions_group = QGroupBox("2. Actions")
        actions_layout = QHBoxLayout()
        
        self.refresh_sd_btn = QPushButton("Refresh SD Card List")
        self.refresh_sd_btn.clicked.connect(self._refresh_sd_cards)
        
        self.start_btn = QPushButton("Organize & Move")
        self.start_btn.clicked.connect(lambda: self._start_organization(move_files=True))
        
        self.copy_btn = QPushButton("Copy Only (Keep Originals)")
        self.copy_btn.clicked.connect(lambda: self._start_organization(move_files=False))
        
        actions_layout.addWidget(self.refresh_sd_btn)
        actions_layout.addWidget(self.start_btn)
        actions_layout.addWidget(self.copy_btn)
        
        actions_group.setLayout(actions_layout)
        main_layout.addWidget(actions_group)
        
        # === 3. Progress Group ===
        progress_group = QGroupBox("3. Progress")
        progress_layout = QVBoxLayout()
        
        self.progress_bar = QProgressBar()
        self.progress_label = QLabel("Waiting for task...")
        
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.progress_label)
        progress_group.setLayout(progress_layout)
        main_layout.addWidget(progress_group)
        
        # === Log Group ===
        log_group = QGroupBox("Log")
        log_layout = QVBoxLayout()
        
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setFont(QFont("Courier", 9))
        log_layout.addWidget(self.log_output)
        
        log_group.setLayout(log_layout)
        main_layout.addWidget(log_group)
        main_layout.setStretchFactor(log_group, 1)

        # === Undo Group ===
        undo_group = QGroupBox("Undo Operation")
        undo_layout = QFormLayout()
        
        self.undo_log_path_edit = QLineEdit()
        self.undo_log_path_edit.setReadOnly(True)
        
        self.browse_undo_log_btn = QPushButton("Choose Undo Log...")
        self.browse_undo_log_btn.clicked.connect(self._browse_undo_log)
        
        undo_browse_layout = QHBoxLayout()
        undo_browse_layout.addWidget(self.undo_log_path_edit)
        undo_browse_layout.addWidget(self.browse_undo_log_btn)
        
        self.undo_btn = QPushButton("Undo Last Operation")
        self.undo_btn.setEnabled(False)
        self.undo_btn.clicked.connect(self._undo_last_operation)
        
        undo_layout.addRow(undo_browse_layout)
        undo_layout.addRow(self.undo_btn)
        
        undo_group.setLayout(undo_layout)
        main_layout.addWidget(undo_group)

        # === Bottom Controls ===
        bottom_layout = QHBoxLayout()
        
        self.browse_log_btn = QPushButton("Open Log Folder")
        self.browse_log_btn.clicked.connect(self._open_log_folder)
        
        self.advanced_config_btn = QPushButton("Advanced Config")
        self.advanced_config_btn.clicked.connect(self._open_advanced_config)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(sorted(THEMES.keys()))
        self.theme_combo.currentTextChanged.connect(self._apply_theme)
        
        bottom_layout.addWidget(self.browse_log_btn)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.advanced_config_btn)
        bottom_layout.addWidget(QLabel("Theme:"))
        bottom_layout.addWidget(self.theme_combo)
        
        main_layout.addLayout(bottom_layout)
        
        # === Load Preferences ===
        self.brand_combo.setCurrentText(self.preferred_brand)
        self.dest_path_edit.setText(self.pictures_path)
        self.theme_combo.setCurrentText(self.preferred_theme)
        self._on_brand_changed(self.brand_combo.currentText())

    def _load_preferences(self):
        """Load user preferences from file"""
        default_pics = os.path.join(os.path.expanduser("~"), "Pictures")
        default_logs = os.path.join(default_pics, "logs")
        
        try:
            prefs_path = os.path.join(BASE_DIR, "preferences.json")
            with open(prefs_path, "r", encoding='utf-8') as f:
                prefs = json.load(f)
            
            self.pictures_path = prefs.get("pictures_path", default_pics)
            self.logs_path = prefs.get("logs_path", default_logs)
            self.preferred_brand = prefs.get("preferred_brand", "Nikon")
            self.preferred_theme = prefs.get("preferred_theme", "Cool Ocean")
        except Exception as e:
            print(f"Could not load preferences: {e}")
            self.pictures_path = default_pics
            self.logs_path = default_logs
            self.preferred_brand = "Nikon"
            self.preferred_theme = "Cool Ocean"

    def _save_preferences(self):
        """Save user preferences to file"""
        try:
            prefs = {
                "pictures_path": self.pictures_path,
                "logs_path": self.logs_path,
                "preferred_brand": self.brand_combo.currentText(),
                "preferred_theme": self.theme_combo.currentText()
            }
            prefs_path = os.path.join(BASE_DIR, "preferences.json")
            with open(prefs_path, "w", encoding='utf-8') as f:
                json.dump(prefs, f, indent=4)
        except Exception as e:
            print(f"Could not save preferences: {e}")

    def _load_config_internal(self):
        """Load embedded configuration"""
        try:
            self.full_config = json.loads(CONFIG_STRING)
            app_config = self.full_config.get("APP_CONFIG", {})
            
            # Override paths only if not modified by user
            if self.pictures_path == os.path.join(os.path.expanduser("~"), "Pictures"):
                self.pictures_path = app_config.get("PICTURES_PATH", self.pictures_path)
            if self.logs_path == os.path.join(self.pictures_path, "logs"):
                self.logs_path = app_config.get("LOGS_PATH", self.logs_path)
                
        except Exception as e:
            QMessageBox.critical(
                self,
                "Config Error",
                f"Error loading internal configuration: {e}"
            )
            self.full_config = {}
            self.close()

    def _on_brand_changed(self, brand):
        """Handle brand selection change"""
        self.log_output.clear()
        
        if not brand:
            self.organizer = None
            self.start_btn.setText("Organize & Move")
            self.advanced_config_btn.setEnabled(False)
            return
        
        # Log dettagliato per debug
        self.log_message_to_gui(f"[DEBUG] Selezionato brand: {brand}")
        self.log_message_to_gui(f"[DEBUG] Pictures path: {self.dest_path_edit.text()}")
        self.log_message_to_gui(f"[DEBUG] Logs path: {self.logs_path}")
        
        try:
            self.log_message_to_gui(f"[DEBUG] Tentativo creazione PhotoOrganizer...")
            self.log_message_to_gui(f"[DEBUG] Parametri:")
            self.log_message_to_gui(f"[DEBUG]   brand_name={brand}")
            self.log_message_to_gui(f"[DEBUG]   pictures_path={self.dest_path_edit.text()}")
            self.log_message_to_gui(f"[DEBUG]   logs_path={self.logs_path}")
            
            self.organizer = PhotoOrganizer(
                brand_name=brand,
                pictures_path=self.dest_path_edit.text(),
                logs_path=self.logs_path,
                log_to_gui_callback=self.log_message_to_gui,
                app_config=self.full_config.get("APP_CONFIG", {}),
                config=self.full_config.get("CONFIGURATIONS", {}).get(brand, {})
            )
            
            self.log_message_to_gui(f"[DEBUG] ✓ PhotoOrganizer creato con successo!")
            self.start_btn.setText(f"Organize & Move {brand}")
            self.advanced_config_btn.setEnabled(True)
            
        except TypeError as e:
            # Cattura specificamente TypeError (parametro sbagliato)
            self.log_message_to_gui(f"[ERROR] TypeError durante creazione PhotoOrganizer: {e}")
            self.log_message_to_gui(f"[ERROR] Tipo errore: {type(e).__name__}")
            
            # Mostra traceback dettagliato
            import traceback
            tb_str = traceback.format_exc()
            for line in tb_str.split('\n'):
                if line.strip():
                    self.log_message_to_gui(f"[TRACEBACK] {line}")
            
            self.organizer = None
            self.start_btn.setText("Organize & Move")
            self.advanced_config_btn.setEnabled(False)
            
        except ValueError as e:
            # Cattura ValueError (configurazione invalida)
            self.log_message_to_gui(f"[ERROR] ValueError: {e}")
            self.organizer = None
            self.start_btn.setText("Organize & Move")
            self.advanced_config_btn.setEnabled(False)
            
        except Exception as e:
            # Cattura qualsiasi altro errore
            self.log_message_to_gui(f"[ERROR] Errore imprevisto durante creazione PhotoOrganizer: {e}")
            self.log_message_to_gui(f"[ERROR] Tipo errore: {type(e).__name__}")
            
            # Mostra traceback dettagliato
            import traceback
            tb_str = traceback.format_exc()
            for line in tb_str.split('\n'):
                if line.strip():
                    self.log_message_to_gui(f"[TRACEBACK] {line}")
            
            self.organizer = None
            self.start_btn.setText("Organize & Move")
            self.advanced_config_btn.setEnabled(False)
        
        self.sd_combo.clear()
        self.sd_combo.setPlaceholderText("Click 'Refresh SD'...")

    def _refresh_sd_cards(self):
        """Refresh the list of detected SD cards"""
        self.sd_combo.clear()
        self.sd_combo.setPlaceholderText("Scanning...")
        self.set_ui_enabled(False, is_scanning=True)
        QApplication.processEvents()
        
        if self.organizer:
            found_sds = self.organizer.find_sd_card_path()
            if found_sds:
                for sd in sorted(found_sds, key=lambda x: x['drive_path']):
                    display_text = f"{sd['brand_folder']} on {sd['drive_path']}"
                    self.sd_combo.addItem(display_text, sd['full_path'])
            else:
                self.sd_combo.setPlaceholderText("No compatible SD Card found.")
        
        self.set_ui_enabled(True)

    def _browse_destination(self):
        """Browse for destination folder"""
        sel_dir = QFileDialog.getExistingDirectory(
            self, "Select Destination", self.pictures_path
        )
        if sel_dir:
            self.dest_path_edit.setText(sel_dir)
            self.pictures_path = sel_dir
            if self.organizer:
                self.organizer.pictures_path = sel_dir

    def _start_organization(self, move_files):
        """Start the organization process with multi-event support"""
        if not self.organizer:
            QMessageBox.warning(
                self, "Brand Required", "Please select a camera brand first."
            )
            return
        
        sd_path = self.sd_combo.currentData()
        if not sd_path:
            QMessageBox.warning(
                self, "SD Card Required", "Please select an SD card first."
            )
            return
        
        # Update organizer's destination path
        self.organizer.pictures_path = self.dest_path_edit.text()
        
        # Save preferences
        self._save_preferences()
        
        # === NEW: Analyze dates in SD card ===
        self.log_message_to_gui("🔍 Analyzing dates in SD card...")
        self.progress_label.setText("Analyzing dates...")
        QApplication.processEvents()  # Update UI
        
        try:
            date_groups = self.organizer.analyze_dates_in_sd(sd_path)
        except Exception as e:
            QMessageBox.critical(
                self,
                "Analysis Error",
                f"Error analyzing SD card: {e}"
            )
            return
        
        if not date_groups:
            QMessageBox.warning(
                self,
                "No Files",
                "No compatible files found on SD card."
            )
            return
        
        # Check if single or multiple dates
        num_dates = len(date_groups)
        
        if num_dates == 1:
            # Single date - use normal import with topic from text field
            topic = self.topic_edit.text().strip()
            if not topic:
                QMessageBox.warning(
                    self, "Topic Required", "Please provide an event/topic name."
                )
                return
            
            self.log_message_to_gui(f"✅ Single date found. Importing with event: {topic}")
            self._start_single_event_import(sd_path, topic, move_files)
        
        else:
            # Multiple dates - show multi-event dialog
            self.log_message_to_gui(f"📅 Found {num_dates} different dates. Opening multi-event dialog...")
            
            from multi_event_dialog import MultiEventDialog
            
            dialog = MultiEventDialog(date_groups, self)
            
            if dialog.exec() == QDialog.DialogCode.Accepted:
                event_mapping = dialog.get_event_mapping()
                self.log_message_to_gui(f"✅ Event mapping configured for {len(event_mapping)} dates")
                self._start_multi_event_import(sd_path, event_mapping, move_files)
            else:
                self.log_message_to_gui("❌ Multi-event import cancelled by user")
    
    def _start_single_event_import(self, sd_path, topic, move_files):
        """Start single-event import (original behavior)"""
        # Disable UI during operation
        self.set_ui_enabled(False)
        self.progress_bar.setValue(0)
        self.progress_label.setText("Starting...")
        
        # Create and start worker thread
        self.worker = WorkerThread(self.organizer, sd_path, topic, move_files)
        self.worker.progress_updated.connect(
            lambda p, f: (
                self.progress_bar.setValue(p),
                self.progress_label.setText(f"Processing: {f}")
            )
        )
        self.worker.log_message.connect(self.log_message_to_gui)
        self.worker.operation_finished.connect(self._organization_finished)
        self.worker.start()
    
    def _start_multi_event_import(self, sd_path, event_mapping, move_files):
        """Start multi-event import (new behavior)"""
        # Disable UI during operation
        self.set_ui_enabled(False)
        self.progress_bar.setValue(0)
        self.progress_label.setText("Starting multi-event import...")
        
        # Create and start worker thread with event mapping
        self.worker = MultiEventWorkerThread(self.organizer, sd_path, event_mapping, move_files)
        self.worker.progress_updated.connect(
            lambda p, f: (
                self.progress_bar.setValue(p),
                self.progress_label.setText(f"Processing: {f}")
            )
        )
        self.worker.log_message.connect(self.log_message_to_gui)
        self.worker.operation_finished.connect(self._organization_finished)
        self.worker.start()

    def _organization_finished(self, success):
        """Handle completion of organization operation"""
        self.set_ui_enabled(True)
        self.progress_bar.setValue(100 if success else 0)
        
        if success:
            self.progress_label.setText("Operation completed successfully!")
            QMessageBox.information(
                self, "Success", "Operation completed successfully!"
            )
            
            # Enable undo if log is available
            if self.organizer and self.organizer.last_undo_log_path:
                self.undo_log_path_edit.setText(self.organizer.last_undo_log_path)
                self.undo_btn.setEnabled(True)
        else:
            self.progress_label.setText("Operation failed. Check log for details.")
            QMessageBox.warning(
                self, "Failure", "Operation failed. Please check the log for details."
            )

    def log_message_to_gui(self, message):
        """Log message to GUI text output"""
        self.log_output.append(message)

    def _apply_theme(self, name):
        """Apply selected theme"""
        self.setStyleSheet(THEMES.get(name, ""))
        self.preferred_theme = name

    def set_ui_enabled(self, enabled, is_scanning=False):
        """Enable or disable UI elements"""
        widgets_to_toggle = [
            self.start_btn, self.copy_btn, self.browse_dest_btn,
            self.browse_log_btn, self.theme_combo, self.brand_combo,
            self.dest_path_edit, self.topic_edit, self.undo_btn,
            self.browse_undo_log_btn, self.advanced_config_btn
        ]
        
        for widget in widgets_to_toggle:
            widget.setEnabled(enabled)
        
        self.refresh_sd_btn.setEnabled(enabled)
        self.refresh_sd_btn.setText(
            "Scanning..." if is_scanning else "Refresh SD Card List"
        )
    
    def _open_advanced_config(self):
        """Open advanced configuration dialog"""
        brand = self.brand_combo.currentText()
        if not brand or not self.full_config:
            return
        
        brand_config = self.full_config.get("CONFIGURATIONS", {}).get(brand)
        dialog = AdvancedConfigDialog(self, config=brand_config, brand=brand)
        dialog.exec()

    def _browse_undo_log(self):
        """Browse for undo log file - FIXED VERSION"""
        undo_dir = os.path.join(self.logs_path, "undo_logs")
        os.makedirs(undo_dir, exist_ok=True)
        
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select Undo Log",
            undo_dir,
            "Undo Logs (*.json);;All Files (*.*)"
        )
        
        if file_name:
            self.undo_log_path_edit.setText(file_name)
            self.undo_btn.setEnabled(True)
    
    def _undo_last_operation(self):
        """Undo the last operation"""
        log_file = self.undo_log_path_edit.text()
        
        if not log_file or not os.path.exists(log_file):
            QMessageBox.warning(
                self, "Input Missing", "Please select a valid undo log file."
            )
            return
        
        reply = QMessageBox.question(
            self,
            "Confirm Undo",
            "Are you sure you want to revert this operation? This will move "
            "all files back to their original locations.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.set_ui_enabled(False)
            self.log_message_to_gui(f"Starting undo operation from: {log_file}...")
            
            # Import base class for static method
            from photo_organizer_logic import SDOrganizerBase
            success = SDOrganizerBase.undo_last_operation(
                log_file, self.log_message_to_gui
            )
            
            result_msg = "Undo completed successfully." if success else \
                        "Undo failed. Check log for details."
            QMessageBox.information(self, "Undo Result", result_msg)
            self.set_ui_enabled(True)

    def _open_log_folder(self):
        """Open the log folder in file explorer"""
        try:
            os.makedirs(self.logs_path, exist_ok=True)
            
            if sys.platform == "win32":
                os.startfile(self.logs_path)
            elif sys.platform == "darwin":
                os.system(f'open "{self.logs_path}"')
            else:
                os.system(f'xdg-open "{self.logs_path}"')
                
        except Exception as e:
            QMessageBox.warning(
                self, "Warning", f"Could not open log folder: {e}"
            )

    def closeEvent(self, event):
        """Handle application close event"""
        # Cleanup organizer resources
        if self.organizer:
            try:
                self.organizer.cleanup()
            except Exception as e:
                print(f"Cleanup error: {e}")
        
        # Wait for worker thread to finish
        if self.worker and self.worker.isRunning():
            reply = QMessageBox.question(
                self,
                "Operation in Progress",
                "An operation is still running. Are you sure you want to quit?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.No:
                event.ignore()
                return
            
            self.worker.quit()
            self.worker.wait(2000)  # Wait up to 2 seconds
        
        event.accept()


def main():
    """Main application entry point"""
    # Create QApplication BEFORE any widget (including QMessageBox) is used
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Use Fusion style for better cross-platform appearance
    
    # Check for admin privileges on Windows
    if sys.platform == "win32" and not is_admin():
        reply = QMessageBox.question(
            None,
            "Permission Required",
            "Administrator privileges are recommended for reliable SD card detection.\n"
            "Would you like to restart as administrator?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            run_as_admin()
            sys.exit(0)
    
    # Create and show main window
    window = SDOrganizerApp()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
