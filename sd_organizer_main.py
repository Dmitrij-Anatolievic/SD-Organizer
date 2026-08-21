from is_admin_check import is_admin
import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
    QWidget, QPushButton, QLabel, QComboBox, QProgressBar,
    QTextEdit, QFileDialog, QMessageBox, QLineEdit,
    QGroupBox, QDialog, QFormLayout, QDialogButtonBox, QListWidget, QListWidgetItem,
    QAbstractItemView
)
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from core_logic_fuji import FujifilmSDOrganizer
from core_logic_nikon import NikonSDOrganizer
from core_logic_olympus import OlympusSDOrganizer
from sd_organizer_base import SDOrganizerBase
from themes import THEMES
import json

# --- GESTIONE PERCORSO ASSOLUTO E PERMESSI ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def is_admin():
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False

def run_as_admin():
    import ctypes
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)


# --- THREAD FOR THE OPERATION ---
class WorkerThread(QThread):
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
        try:
            def progress_callback(progress, filename):
                self.progress_updated.emit(progress, filename)
                
            success = self.organizer.organize_sd_files(
                self.sd_full_path, 
                topic=self.topic,
                move_files=self.move_files,
                progress_callback=progress_callback
            )
            self.operation_finished.emit(success)
        except Exception as e:
            self.log_message.emit(f"ERROR: Unexpected error in worker thread: {e}")
            self.operation_finished.emit(False)

# --- DIALOG FOR ADVANCED CONFIGURATION ---
class AdvancedConfigDialog(QDialog):
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
        sd_group = QGroupBox("SD Card Candidate Folders")
        sd_layout = QFormLayout()
        self.sd_folders_edit = QLineEdit()
        self.sd_folders_edit.setToolTip("Enter folder names, separated by commas (e.g., 100_FUJI, 101_FUJI)")
        sd_layout.addRow("Folder Names:", self.sd_folders_edit)
        sd_group.setLayout(sd_layout)
        self.layout.addWidget(sd_group)

        dest_group = QGroupBox("File Destinations by Extension")
        dest_layout = QVBoxLayout()
        self.dest_list = QListWidget()
        self.dest_list.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        dest_layout.addWidget(self.dest_list)
        
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add")
        self.edit_button = QPushButton("Edit")
        self.remove_button = QPushButton("Remove")
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.remove_button)
        dest_layout.addLayout(button_layout)
        
        dest_group.setLayout(dest_layout)
        self.layout.addWidget(dest_group)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        self.layout.addWidget(self.button_box)
        
        self.button_box.accepted.connect(self.save_config_and_accept)
        self.button_box.rejected.connect(self.reject)
        self.add_button.clicked.connect(self.add_destination)
        self.edit_button.clicked.connect(self.edit_destination)
        self.remove_button.clicked.connect(self.remove_destination)

    def load_config_data(self):
        sd_folders = self.config.get("SD_FOLDER_NAMES_CANDIDATES", [])
        self.sd_folders_edit.setText(", ".join(sd_folders))
        
        self.dest_list.clear()
        file_dest = self.config.get("FILE_DESTINATIONS", {})
        for ext, path in file_dest.items():
            self.dest_list.addItem(f"{ext}:{path}")
    
    def add_destination(self):
        self.edit_destination(add_new=True)

    def edit_destination(self, add_new=False):
        if add_new:
            item = None
            text = ""
        else:
            item = self.dest_list.currentItem()
            if not item:
                QMessageBox.warning(self, "Selection Error", "Please select an item to edit.")
                return
            text = item.text()

        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Destination")
        form = QFormLayout(dialog)
        
        ext_edit = QLineEdit()
        path_edit = QLineEdit()
        
        if not add_new and ':' in text:
            ext, path = text.split(':', 1)
            ext_edit.setText(ext)
            path_edit.setText(path)
            
        form.addRow("Extension (e.g., .jpg):", ext_edit)
        form.addRow("Subfolder (leave empty for main folder):", path_edit)
        
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        form.addWidget(button_box)
        
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        
        if dialog.exec():
            ext = ext_edit.text().strip().lower()
            if not ext.startswith('.'):
                ext = '.' + ext
            path = path_edit.text().strip()
            
            if not add_new:
                item.setText(f"{ext}:{path}")
            else:
                self.dest_list.addItem(f"{ext}:{path}")
                
    def remove_destination(self):
        item = self.dest_list.currentItem()
        if not item:
            QMessageBox.warning(self, "Selection Error", "Please select an item to remove.")
            return
        self.dest_list.takeItem(self.dest_list.row(item))

    def save_config_and_accept(self):
        try:
            config_path = os.path.join(BASE_DIR, "config.json")
            with open(config_path, "r") as f:
                full_config = json.load(f)
            
            brand_config = full_config["CONFIGURATIONS"][self.brand]
            
            sd_folders_text = self.sd_folders_edit.text()
            brand_config["SD_FOLDER_NAMES_CANDIDATES"] = [folder.strip() for folder in sd_folders_text.split(',') if folder.strip()]
            
            new_file_dest = {}
            for i in range(self.dest_list.count()):
                text = self.dest_list.item(i).text()
                if ':' in text:
                    ext, path = text.split(':', 1)
                    new_file_dest[ext] = path
            brand_config["FILE_DESTINATIONS"] = new_file_dest

            with open(config_path, "w") as f:
                json.dump(full_config, f, indent=4)
            
            QMessageBox.information(self, "Success", "Configuration saved successfully!")
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"An error occurred while saving: {e}")

# --- MAIN APPLICATION ---
class SDOrganizerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SD Card Organizer Multi-Brand")
        self.setMinimumSize(800, 700) # Imposta una dimensione minima
        self.organizer = None
        self.full_config = None
        
        self._load_preferences()
        self._init_ui()
        self._load_config()
        self._apply_theme(self.preferred_theme)

    def _init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # --- Brand and Paths Group ---
        setup_group = QGroupBox("1. Setup")
        
        ## --- CORREZIONE: Utilizzo di QFormLayout ---
        # QFormLayout è ideale per form label-campo, previene il taglio del testo.
        setup_form_layout = QFormLayout()

        self.brand_combo = QComboBox()
        self.brand_combo.addItems(["Nikon", "Fujifilm", "Olympus"])
        self.brand_combo.currentTextChanged.connect(self._on_brand_changed)
        setup_form_layout.addRow("Select Camera Brand:", self.brand_combo)
        
        self.sd_combo = QComboBox()
        self.sd_combo.setPlaceholderText("Click 'Refresh SD' to search...")
        setup_form_layout.addRow("Detected SD Card:", self.sd_combo)
        
        # Layout per campo di testo e bottone browse
        dest_layout = QHBoxLayout()
        self.dest_path_edit = QLineEdit(self.pictures_path)
        self.browse_dest_button = QPushButton("Browse...")
        self.browse_dest_button.clicked.connect(self._browse_destination)
        dest_layout.addWidget(self.dest_path_edit)
        dest_layout.addWidget(self.browse_dest_button)
        setup_form_layout.addRow("Destination Path:", dest_layout)

        self.topic_edit = QLineEdit()
        self.topic_edit.setPlaceholderText("e.g., Birthday, Trip_To_Rome, etc.")
        setup_form_layout.addRow("Event/Topic Name:", self.topic_edit)

        setup_group.setLayout(setup_form_layout)
        main_layout.addWidget(setup_group)
        
        # --- Actions Group ---
        actions_group = QGroupBox("2. Actions")
        actions_layout = QHBoxLayout()
        self.refresh_sd_button = QPushButton("Refresh SD Card List")
        self.refresh_sd_button.clicked.connect(self._refresh_sd_cards)
        self.start_button = QPushButton("Organize & Move")
        self.start_button.clicked.connect(lambda: self._start_organization(move_files=True))
        self.copy_button = QPushButton("Copy Only")
        self.copy_button.clicked.connect(lambda: self._start_organization(move_files=False))
        actions_layout.addWidget(self.refresh_sd_button)
        actions_layout.addWidget(self.start_button)
        actions_layout.addWidget(self.copy_button)
        actions_group.setLayout(actions_layout)
        main_layout.addWidget(actions_group)

        # --- Progress ---
        progress_group = QGroupBox("3. Progress")
        progress_layout = QVBoxLayout()
        self.progress_bar = QProgressBar()
        self.progress_label = QLabel("Waiting for task...")
        self.progress_label.setStyleSheet("font-style: italic;")
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.progress_label)
        progress_group.setLayout(progress_layout)
        main_layout.addWidget(progress_group)
        
        # --- Log Output ---
        log_group = QGroupBox("Log")
        log_layout = QVBoxLayout()
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setObjectName("consoleOutput")
        log_layout.addWidget(self.log_output)
        log_group.setLayout(log_layout)
        main_layout.addWidget(log_group)
        main_layout.setStretchFactor(log_group, 1) # Permette al log di espandersi
        
        # --- Undo Group ---
        undo_group = QGroupBox("Undo Operation")
        undo_layout = QFormLayout()
        self.undo_log_path_edit = QLineEdit()
        self.undo_log_path_edit.setPlaceholderText("Select the undo_log.json file...")
        self.browse_undo_log_button = QPushButton("Choose Log...")
        self.browse_undo_log_button.clicked.connect(self._browse_undo_log)
        
        undo_browse_layout = QHBoxLayout()
        undo_browse_layout.addWidget(self.undo_log_path_edit)
        undo_browse_layout.addWidget(self.browse_undo_log_button)

        self.undo_button = QPushButton("Undo Last Operation")
        self.undo_button.setEnabled(False)
        self.undo_button.clicked.connect(self._undo_last_operation)

        undo_layout.addRow(undo_browse_layout)
        undo_layout.addRow(self.undo_button)
        undo_group.setLayout(undo_layout)
        main_layout.addWidget(undo_group)

        # --- Bottom Bar ---
        bottom_layout = QHBoxLayout()
        self.browse_log_button = QPushButton("Open Log Folder")
        self.browse_log_button.clicked.connect(self._open_log_folder)
        self.advanced_config_button = QPushButton("Advanced Config")
        self.advanced_config_button.clicked.connect(self._open_advanced_config)
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(sorted(THEMES.keys()))
        self.theme_combo.currentTextChanged.connect(self._apply_theme)
        
        bottom_layout.addWidget(self.browse_log_button)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.advanced_config_button)
        bottom_layout.addWidget(QLabel("Theme:"))
        bottom_layout.addWidget(self.theme_combo)
        main_layout.addLayout(bottom_layout)
        
        self.brand_combo.setCurrentText(self.preferred_brand)
        self.dest_path_edit.setText(self.pictures_path)
        self.theme_combo.setCurrentText(self.preferred_theme)
        self._on_brand_changed(self.brand_combo.currentText())
        
    def _load_preferences(self):
        prefs_path = os.path.join(BASE_DIR, "preferences.json")
        try:
            with open(prefs_path, "r") as f:
                prefs = json.load(f)
                self.pictures_path = prefs.get("pictures_path", os.path.join(os.path.expanduser("~"), "Pictures"))
                self.logs_path = prefs.get("logs_path", os.path.join(BASE_DIR, "logs"))
                self.preferred_brand = prefs.get("preferred_brand", "Nikon")
                self.preferred_theme = prefs.get("preferred_theme", "Cool Ocean")
        except (FileNotFoundError, json.JSONDecodeError):
            self.pictures_path = os.path.join(os.path.expanduser("~"), "Pictures")
            self.logs_path = os.path.join(BASE_DIR, "logs")
            self.preferred_brand = "Nikon"
            self.preferred_theme = "Cool Ocean"
    
    def _save_preferences(self):
        prefs_path = os.path.join(BASE_DIR, "preferences.json")
        prefs = {
            "pictures_path": self.pictures_path,
            "logs_path": self.logs_path,
            "preferred_brand": self.brand_combo.currentText(),
            "preferred_theme": self.theme_combo.currentText()
        }
        try:
            os.makedirs(os.path.dirname(prefs_path), exist_ok=True)
            with open(prefs_path, "w") as f:
                json.dump(prefs, f, indent=4)
        except Exception as e:
            self.log_message_to_gui(f"ERROR: Error saving preferences: {e}")

    def _load_config(self):
        config_path = os.path.join(BASE_DIR, "config.json")
        try:
            with open(config_path, "r") as f:
                self.full_config = json.load(f)
                app_config = self.full_config.get("APP_CONFIG", {})
                self.pictures_path = app_config.get("PICTURES_PATH", self.pictures_path)
                self.logs_path = app_config.get("LOGS_PATH", self.logs_path)
                self.dest_path_edit.setText(self.pictures_path) 
        except FileNotFoundError:
            QMessageBox.critical(self, "Configuration Error", f"The 'config.json' file was not found at:\n{config_path}\nPlease ensure it exists.")
            self.close()
            return
        except json.JSONDecodeError:
            QMessageBox.critical(self, "Configuration Error", "The 'config.json' file is malformed. Please check its syntax.")
            self.close()
            return

    def _open_advanced_config(self):
        if not self.full_config:
            QMessageBox.warning(self, "Warning", "The configuration file has not been loaded correctly.")
            return

        brand = self.brand_combo.currentText()
        brand_config = self.full_config["CONFIGURATIONS"].get(brand)

        if not brand_config:
            QMessageBox.warning(self, "Warning", f"Configuration for brand '{brand}' not found.")
            return

        dialog = AdvancedConfigDialog(self, config=brand_config, brand=brand)
        if dialog.exec():
            self._load_config()
            self._on_brand_changed(self.brand_combo.currentText())

    def _on_brand_changed(self, brand):
        self.log_output.clear()
        pictures_path = self.dest_path_edit.text()
        logs_path = self.logs_path
        
        organizer_class = {
            "Nikon": NikonSDOrganizer,
            "Fujifilm": FujifilmSDOrganizer,
            "Olympus": OlympusSDOrganizer
        }.get(brand)

        if organizer_class:
            self.organizer = organizer_class(pictures_path, logs_path, self.log_message_to_gui)
        
        self.start_button.setText(f"Organize & Move {brand}")
        self.sd_combo.clear()
        self.sd_combo.setPlaceholderText("Click 'Refresh SD' to search...")
        
    def _refresh_sd_cards(self):
        self.sd_combo.clear()
        self.sd_combo.setPlaceholderText("Scanning for SD cards, please wait...")
        self.set_ui_enabled(False, is_scanning=True)
        QApplication.processEvents()
        self.log_message_to_gui("INFO: Searching for SD cards...")
        
        if self.organizer:
            found_sds = self.organizer.find_sd_card_path()
            self.sd_combo.clear()
            if found_sds:
                for sd in found_sds:
                    self.sd_combo.addItem(f"{sd['brand_folder']} on {sd['drive_path']}", sd['full_path'])
                self.log_message_to_gui(f"INFO: Found {len(found_sds)} compatible folder(s). Please select from the dropdown.")
            else:
                self.sd_combo.setPlaceholderText("No compatible SD Card found...")
                self.log_message_to_gui("WARNING: No compatible SD cards found. Check connection or Advanced Config.")
        
        self.set_ui_enabled(True)

    def _browse_destination(self):
        selected_dir = QFileDialog.getExistingDirectory(self, "Select Destination Directory", self.pictures_path)
        if selected_dir:
            self.dest_path_edit.setText(selected_dir)
            self.pictures_path = selected_dir
            if self.organizer:
                self.organizer.pictures_path = selected_dir
                self.log_message_to_gui(f"INFO: Destination path updated to: {selected_dir}")

    def _open_log_folder(self):
        log_path = self.logs_path
        try:
            os.makedirs(log_path, exist_ok=True)
            if sys.platform == "win32":
                os.startfile(log_path)
            elif sys.platform == "darwin":
                os.system(f'open "{log_path}"')
            else:
                os.system(f'xdg-open "{log_path}"')
        except Exception as e:
            QMessageBox.warning(self, "Warning", f"Could not open the log folder: {e}")

    def _start_organization(self, move_files):
        if not self.organizer:
            QMessageBox.warning(self, "Warning", "Please select a brand before starting.")
            return

        sd_full_path = self.sd_combo.currentData()
        if not sd_full_path:
            QMessageBox.warning(self, "Warning", "No SD card selected.")
            return

        topic = self.topic_edit.text().strip().replace(" ", "_")
        if not topic:
            QMessageBox.warning(self, "Warning", "Please enter a topic for the photo session.")
            return

        self.set_ui_enabled(False)
        self.progress_bar.setValue(0)
        self.progress_label.setText("Starting...")
        action_str = "Moving" if move_files else "Copying"
        self.log_message_to_gui(f"INFO: Operation started ({action_str} files).")

        self._save_preferences()
        self.organizer.pictures_path = self.dest_path_edit.text()

        self.worker_thread = WorkerThread(self.organizer, sd_full_path, topic, move_files)
        self.worker_thread.progress_updated.connect(self._update_progress)
        self.worker_thread.log_message.connect(self.log_message_to_gui)
        self.worker_thread.operation_finished.connect(self._organization_finished)
        self.worker_thread.start()

    def _update_progress(self, progress, filename):
        self.progress_bar.setValue(progress)
        self.progress_label.setText(f"Processing: {filename}")

    def _organization_finished(self, success):
        self.set_ui_enabled(True)
        self.progress_bar.setValue(100)
        
        if success:
            self.progress_label.setText("Operation completed successfully!")
            QMessageBox.information(self, "Operation Complete", "File organization completed successfully!")
            self.log_message_to_gui("INFO: Operation completed.")
            if self.organizer and self.organizer.last_undo_log_path:
                self.undo_log_path_edit.setText(self.organizer.last_undo_log_path)
                self.undo_button.setEnabled(True)
        else:
            self.progress_label.setText("Operation failed. Check log for details.")
            QMessageBox.critical(self, "Operation Failed", "An error occurred during file organization. Check the log for details.")
            self.log_message_to_gui("ERROR: Operation failed.")
        
        if self.organizer and self.organizer.logs_path:
            self.log_message_to_gui(f"INFO: Full operation details have been saved in: {self.organizer.logs_path}")

    def log_message_to_gui(self, message):
        self.log_output.append(message)
        self.log_output.verticalScrollBar().setValue(self.log_output.verticalScrollBar().maximum())
    
    def _apply_theme(self, theme_name):
        style = THEMES.get(theme_name)
        if style is not None:
            self.setStyleSheet(style)
            self.preferred_theme = theme_name
            self._save_preferences()
    
    def set_ui_enabled(self, enabled, is_scanning=False):
        # Disabilita/Abilita tutti i controlli principali
        self.start_button.setEnabled(enabled)
        self.copy_button.setEnabled(enabled)
        self.browse_dest_button.setEnabled(enabled)
        self.browse_log_button.setEnabled(enabled)
        self.theme_combo.setEnabled(enabled)
        self.brand_combo.setEnabled(enabled)
        self.dest_path_edit.setEnabled(enabled)
        self.topic_edit.setEnabled(enabled)
        self.advanced_config_button.setEnabled(enabled)
        self.undo_button.setEnabled(enabled)
        self.browse_undo_log_button.setEnabled(enabled)
        
        # Gestione speciale per il bottone di refresh
        self.refresh_sd_button.setEnabled(enabled)
        if is_scanning:
            self.refresh_sd_button.setText("Scanning...")
        else:
            self.refresh_sd_button.setText("Refresh SD Card List")

    def _browse_undo_log(self):
        undo_logs_dir = os.path.join(self.logs_path, "undo_logs")
        os.makedirs(undo_logs_dir, exist_ok=True)
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Undo Log", undo_logs_dir, "JSON Log Files (*.json)")
        if file_name:
            self.undo_log_path_edit.setText(file_name)
            self.undo_button.setEnabled(True)

    def _undo_last_operation(self):
        log_file_path = self.undo_log_path_edit.text()
        if not log_file_path or not os.path.exists(log_file_path):
            QMessageBox.warning(self, "Warning", "Please select a valid log file to undo the operation.")
            return

        reply = QMessageBox.question(self, "Confirm Undo",
                                     "Are you sure you want to undo this operation? Files will be moved back to their original locations.",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.set_ui_enabled(False)
            self.log_message_to_gui("INFO: Starting undo...")
            success = SDOrganizerBase.undo_last_operation(log_file_path, self.log_message_to_gui)
            
            if success:
                QMessageBox.information(self, "Undo Complete", "The operation was successfully undone.")
            else:
                QMessageBox.critical(self, "Undo Failed", "An error occurred during the undo operation. Please check the log.")
            
            self.set_ui_enabled(True)

if __name__ == "__main__":
    # --- CORREZIONE: Logica di avvio migliorata ---
    # Controlla se lo script è stato avviato con il flag speciale dal launcher.
    # sys.argv è la lista degli argomenti passati da riga di comando.
    started_by_admin_launcher = "--started-as-admin" in sys.argv

    # Esegui il controllo dei permessi solo se è Windows E non è stato avviato
    # da un launcher che è già admin.
    if sys.platform == "win32" and not started_by_admin_launcher:
        if not is_admin():
            app_temp = QApplication.instance() 
            if app_temp is None:
                app_temp = QApplication(sys.argv)
            
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setText("Administrator Privileges Required")
            msg_box.setInformativeText("This application needs administrator privileges to correctly detect all drives. Please click OK to restart with the correct permissions.")
            msg_box.setWindowTitle("Permission Required")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            
            response = msg_box.exec()
            
            if response == QMessageBox.StandardButton.Ok:
                run_as_admin()

            # Termina il processo corrente non-admin in ogni caso
            sys.exit(0)

    # Questo codice viene raggiunto se:
    # 1. Non è Windows
    # 2. È Windows ed è già admin
    # 3. È Windows ed è stato lanciato dal nostro launcher con privilegi elevati
    app = QApplication(sys.argv)
    
    # Assicurati di avere la definizione della classe SDOrganizerApp prima di questo punto
    # Esempio:
    # class SDOrganizerApp(QMainWindow):
    #     ...
    
    # window = SDOrganizerApp()  <-- DECOMMENTA QUESTA LINEA NEL TUO FILE REALE
    # window.show()             <-- DECOMMENTA QUESTA LINEA NEL TUO FILE REALE
    
    # sys.exit(app.exec())      <-- DECOMMENTA QUESTA LINEA NEL TUO FILE REALE
    
    # Per favore, assicurati di incollare questa logica if __name__ == "__main__":
    # alla fine del tuo file sd_organizer_main.py, sostituendo il blocco esistente.
    # Le righe sopra sono commentate perché non ho la definizione completa della classe qui.
    pass # Rimuovi questa riga nel tuo file finale