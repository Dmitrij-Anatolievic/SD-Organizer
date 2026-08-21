"""
INTEGRATION EXAMPLE - Come integrare le nuove features nel main_app.py

Questo file mostra esempi di codice per integrare le 4 nuove funzionalità
nell'applicazione principale. Puoi copiare questi snippet nel tuo main_app.py.
"""

# ========================================
# 1. AUTO-IMPORT INTEGRATION
# ========================================

from auto_import_service import AutoImportService, AutoImportSettings
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QCheckBox, QPushButton

class AutoImportDialog(QDialog):
    """Dialog per configurazione auto-import"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Auto-Import Configuration")
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Enable/disable auto-import
        self.enable_checkbox = QCheckBox("Enable Auto-Import")
        layout.addWidget(self.enable_checkbox)
        
        # Save button
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_settings)
        layout.addWidget(save_btn)
    
    def save_settings(self):
        settings = AutoImportSettings()
        if self.enable_checkbox.isChecked():
            settings.enable()
        else:
            settings.disable()
        self.accept()


# Aggiungere al __init__ del MainWindow:
def init_auto_import(self):
    """Inizializza servizio auto-import"""
    self.auto_import_service = AutoImportService(
        check_interval=5,
        auto_import_callback=self.handle_auto_import
    )
    
    # Avvia se abilitato nelle preferenze
    settings = AutoImportSettings()
    if settings.is_enabled():
        self.auto_import_service.start()

def handle_auto_import(self, drive_path, rule):
    """Callback quando SD viene rilevata"""
    from PyQt6.QtWidgets import QMessageBox
    
    msg = QMessageBox(self)
    msg.setWindowTitle("SD Card Detected")
    msg.setText(f"SD card detected at {drive_path}")
    msg.setInformativeText("Do you want to import photos now?")
    msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    
    if msg.exec() == QMessageBox.StandardButton.Yes:
        # Trigger import
        self._start_organization(move_files=True)


# ========================================
# 2. TAGGING SYSTEM INTEGRATION
# ========================================

from database_manager import PhotoDatabase
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QComboBox, QPushButton, QLabel

class TaggingDialog(QDialog):
    """Dialog per aggiungere tag a foto"""
    
    def __init__(self, photo_id, parent=None):
        super().__init__(parent)
        self.photo_id = photo_id
        self.db = PhotoDatabase()
        self.setWindowTitle("Tag Photo")
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Tag input
        layout.addWidget(QLabel("Tags (comma-separated):"))
        self.tags_input = QLineEdit()
        layout.addWidget(self.tags_input)
        
        # Rating
        layout.addWidget(QLabel("Rating:"))
        self.rating_combo = QComboBox()
        self.rating_combo.addItems(["0", "1", "2", "3", "4", "5"])
        layout.addWidget(self.rating_combo)
        
        # Color flag
        layout.addWidget(QLabel("Color Flag:"))
        self.color_combo = QComboBox()
        self.color_combo.addItems(["none", "red", "green", "yellow", "blue", "purple"])
        layout.addWidget(self.color_combo)
        
        # Save button
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_tags)
        layout.addWidget(save_btn)
    
    def save_tags(self):
        # Parse tags
        tags = [t.strip() for t in self.tags_input.text().split(',') if t.strip()]
        
        # Save tags
        if tags:
            self.db.tag_photo(self.photo_id, tags)
        
        # Save rating
        rating = int(self.rating_combo.currentText())
        self.db.update_photo_rating(self.photo_id, rating)
        
        # Save color
        color = self.color_combo.currentText()
        if color != "none":
            self.db.update_photo_color_flag(self.photo_id, color)
        
        self.accept()


# ========================================
# 3. DATABASE SEARCH INTEGRATION
# ========================================

from database_manager import PhotoDatabase
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QDateEdit, 
                             QLineEdit, QSpinBox, QPushButton, QTableWidget, QLabel)

class SearchWidget(QWidget):
    """Widget per ricerca avanzata nel database"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = PhotoDatabase()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Date range
        date_layout = QHBoxLayout()
        date_layout.addWidget(QLabel("Date From:"))
        self.date_from = QDateEdit()
        date_layout.addWidget(self.date_from)
        date_layout.addWidget(QLabel("To:"))
        self.date_to = QDateEdit()
        date_layout.addWidget(self.date_to)
        layout.addLayout(date_layout)
        
        # Camera model
        camera_layout = QHBoxLayout()
        camera_layout.addWidget(QLabel("Camera:"))
        self.camera_input = QLineEdit()
        camera_layout.addWidget(self.camera_input)
        layout.addLayout(camera_layout)
        
        # ISO range
        iso_layout = QHBoxLayout()
        iso_layout.addWidget(QLabel("ISO:"))
        self.iso_min = QSpinBox()
        self.iso_min.setRange(0, 25600)
        iso_layout.addWidget(self.iso_min)
        iso_layout.addWidget(QLabel("to"))
        self.iso_max = QSpinBox()
        self.iso_max.setRange(0, 25600)
        self.iso_max.setValue(25600)
        iso_layout.addWidget(self.iso_max)
        layout.addLayout(iso_layout)
        
        # Rating
        rating_layout = QHBoxLayout()
        rating_layout.addWidget(QLabel("Min Rating:"))
        self.rating_spin = QSpinBox()
        self.rating_spin.setRange(0, 5)
        rating_layout.addWidget(self.rating_spin)
        layout.addLayout(rating_layout)
        
        # Search button
        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.perform_search)
        layout.addWidget(search_btn)
        
        # Results table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(6)
        self.results_table.setHorizontalHeaderLabels([
            "Filename", "Date", "Camera", "ISO", "Rating", "Tags"
        ])
        layout.addWidget(self.results_table)
    
    def perform_search(self):
        # Get search parameters
        date_from = self.date_from.date().toString("yyyy-MM-dd") if self.date_from.date().isValid() else None
        date_to = self.date_to.date().toString("yyyy-MM-dd") if self.date_to.date().isValid() else None
        camera = self.camera_input.text() or None
        iso_min = self.iso_min.value() if self.iso_min.value() > 0 else None
        iso_max = self.iso_max.value() if self.iso_max.value() < 25600 else None
        rating_min = self.rating_spin.value()
        
        # Perform search
        results = self.db.search_photos(
            date_from=date_from,
            date_to=date_to,
            camera_model=camera,
            iso_min=iso_min,
            iso_max=iso_max,
            rating_min=rating_min
        )
        
        # Display results
        self.results_table.setRowCount(len(results))
        for row, photo in enumerate(results):
            self.results_table.setItem(row, 0, QTableWidgetItem(photo['filename']))
            self.results_table.setItem(row, 1, QTableWidgetItem(str(photo['date_taken'])))
            self.results_table.setItem(row, 2, QTableWidgetItem(photo['camera_model'] or ''))
            self.results_table.setItem(row, 3, QTableWidgetItem(str(photo['iso'] or '')))
            self.results_table.setItem(row, 4, QTableWidgetItem(str(photo['rating'])))
            
            # Get tags
            tags = self.db.get_photo_tags(photo['id'])
            self.results_table.setItem(row, 5, QTableWidgetItem(', '.join(tags)))


# ========================================
# 4. IMAGE PROCESSING INTEGRATION
# ========================================

from processing_tools import ImageProcessor, BatchProcessor
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QCheckBox, QPushButton, 
                             QProgressBar, QFileDialog, QSpinBox, QLineEdit, QLabel)

class ProcessingWidget(QWidget):
    """Widget per elaborazione immagini"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.processor = ImageProcessor()
        self.batch_processor = BatchProcessor()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Operations checkboxes
        layout.addWidget(QLabel("Select Operations:"))
        self.auto_rotate_cb = QCheckBox("Auto-Rotate from EXIF")
        self.auto_rotate_cb.setChecked(True)
        layout.addWidget(self.auto_rotate_cb)
        
        self.convert_raw_cb = QCheckBox("Convert RAW to JPEG")
        layout.addWidget(self.convert_raw_cb)
        
        self.resize_cb = QCheckBox("Resize Images")
        layout.addWidget(self.resize_cb)
        
        # Resize options
        resize_layout = QHBoxLayout()
        resize_layout.addWidget(QLabel("Max Width:"))
        self.resize_width = QSpinBox()
        self.resize_width.setRange(100, 10000)
        self.resize_width.setValue(1920)
        resize_layout.addWidget(self.resize_width)
        layout.addLayout(resize_layout)
        
        self.watermark_cb = QCheckBox("Add Watermark")
        layout.addWidget(self.watermark_cb)
        
        # Watermark options
        watermark_layout = QHBoxLayout()
        watermark_layout.addWidget(QLabel("Text:"))
        self.watermark_text = QLineEdit("© 2025")
        watermark_layout.addWidget(self.watermark_text)
        layout.addLayout(watermark_layout)
        
        # Process button
        process_btn = QPushButton("Process Batch")
        process_btn.clicked.connect(self.process_batch)
        layout.addWidget(process_btn)
        
        # Progress
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)
    
    def process_batch(self):
        # Select files
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Images",
            "",
            "Images (*.jpg *.jpeg *.png *.nef *.cr2 *.arw *.raf)"
        )
        
        if not files:
            return
        
        # Build operations list
        operations = []
        
        if self.auto_rotate_cb.isChecked():
            operations.append({'type': 'auto_rotate'})
        
        if self.convert_raw_cb.isChecked():
            operations.append({'type': 'convert_raw', 'quality': 95})
        
        if self.resize_cb.isChecked():
            operations.append({
                'type': 'resize',
                'max_width': self.resize_width.value()
            })
        
        if self.watermark_cb.isChecked():
            operations.append({
                'type': 'watermark',
                'text': self.watermark_text.text(),
                'position': 'bottom-right'
            })
        
        # Process
        def update_progress(current, total, filename):
            progress = int((current / total) * 100)
            self.progress_bar.setValue(progress)
        
        stats = self.batch_processor.process_batch(
            files,
            operations,
            progress_callback=update_progress
        )
        
        # Show results
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.information(
            self,
            "Processing Complete",
            f"Processed: {stats['processed']}\nFailed: {stats['failed']}"
        )


# ========================================
# MAIN WINDOW INTEGRATION EXAMPLE
# ========================================

from PyQt6.QtWidgets import QMainWindow, QTabWidget

class EnhancedMainWindow(QMainWindow):
    """Esempio di MainWindow con tutte le features"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SD Organizer V3 Enhanced")
        self.setup_ui()
        self.init_auto_import()
    
    def setup_ui(self):
        # Central widget con tab
        tabs = QTabWidget()
        self.setCentralWidget(tabs)
        
        # Tab originale (import)
        # ... codice esistente ...
        
        # NEW: Database Search tab
        search_widget = SearchWidget()
        tabs.addTab(search_widget, "🔍 Search")
        
        # NEW: Processing tab
        processing_widget = ProcessingWidget()
        tabs.addTab(processing_widget, "🎨 Processing")
        
        # NEW: Auto-Import settings in menu
        auto_import_action = self.menuBar().addAction("Auto-Import Settings")
        auto_import_action.triggered.connect(self.show_auto_import_dialog)
    
    def show_auto_import_dialog(self):
        dialog = AutoImportDialog(self)
        dialog.exec()
    
    def init_auto_import(self):
        """Vedi esempio sopra"""
        pass


"""
ISTRUZIONI PER L'INTEGRAZIONE:

1. Copia le classi di cui hai bisogno nel tuo main_app.py

2. Nel __init__ del MainWindow, aggiungi:
   - self.init_auto_import() per auto-import
   - Search tab per database
   - Processing tab per elaborazione

3. Importa i moduli necessari:
   from database_manager import PhotoDatabase
   from auto_import_service import AutoImportService
   from processing_tools import ImageProcessor

4. Il database viene popolato automaticamente quando importi foto
   (già integrato in photo_organizer_logic.py)

5. Testa le funzionalità una alla volta

DOCUMENTAZIONE COMPLETA: Vedi README.md
"""
