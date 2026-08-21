"""
Multi-Event Dialog
Dialog per assegnare nomi evento diversi a date diverse
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox, QGroupBox, QFormLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from typing import Dict
from datetime import datetime


class MultiEventDialog(QDialog):
    """
    Dialog che mostra le date trovate nella SD e permette di assegnare
    un nome evento diverso per ogni data
    """
    
    def __init__(self, date_groups: Dict, parent=None):
        """
        Args:
            date_groups: Dictionary from analyze_dates_in_sd()
                        {'2025-10-10': {'files': [...], 'count': 5, 'date_obj': datetime}, ...}
        """
        super().__init__(parent)
        self.date_groups = date_groups
        self.event_mapping = {}  # Will store {'2025-10-10': 'EventName', ...}
        
        self.setWindowTitle("Multiple Events Detected")
        self.setMinimumWidth(700)
        self.setMinimumHeight(500)
        
        self.setup_ui()
        self.populate_table()
    
    def setup_ui(self):
        """Setup user interface"""
        layout = QVBoxLayout(self)
        
        # Info header
        info_group = QGroupBox("📅 Multiple Dates Found")
        info_layout = QVBoxLayout(info_group)
        
        info_text = QLabel(
            f"Found photos from <b>{len(self.date_groups)}</b> different dates.\n"
            "Please assign an event name for each date."
        )
        info_text.setWordWrap(True)
        info_layout.addWidget(info_text)
        layout.addWidget(info_group)
        
        # Table with dates and input fields
        table_group = QGroupBox("Event Names per Date")
        table_layout = QVBoxLayout(table_group)
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Date", "Day", "Files", "Event Name"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setRowCount(len(self.date_groups))
        
        table_layout.addWidget(self.table)
        layout.addWidget(table_group)
        
        # Quick actions
        actions_layout = QHBoxLayout()
        
        use_same_btn = QPushButton("📝 Use Same Name for All")
        use_same_btn.setToolTip("Use the same event name for all dates")
        use_same_btn.clicked.connect(self.use_same_name_for_all)
        actions_layout.addWidget(use_same_btn)
        
        auto_name_btn = QPushButton("🤖 Auto-Name by Date")
        auto_name_btn.setToolTip("Automatically name events like 'Event_2025-10-10'")
        auto_name_btn.clicked.connect(self.auto_name_by_date)
        actions_layout.addWidget(auto_name_btn)
        
        clear_btn = QPushButton("🗑️ Clear All")
        clear_btn.clicked.connect(self.clear_all_names)
        actions_layout.addWidget(clear_btn)
        
        layout.addLayout(actions_layout)
        
        # Bottom buttons
        button_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("❌ Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        button_layout.addStretch()
        
        self.ok_btn = QPushButton("✅ Start Import")
        self.ok_btn.setDefault(True)
        bold_font = QFont()
        bold_font.setBold(True)
        self.ok_btn.setFont(bold_font)
        self.ok_btn.clicked.connect(self.validate_and_accept)
        button_layout.addWidget(self.ok_btn)
        
        layout.addLayout(button_layout)
    
    def populate_table(self):
        """Populate table with dates and input fields"""
        sorted_dates = sorted(self.date_groups.keys())
        
        for row, date_str in enumerate(sorted_dates):
            info = self.date_groups[date_str]
            date_obj = info['date_obj']
            file_count = info['count']
            
            # Date column
            date_item = QTableWidgetItem(date_str)
            date_item.setFlags(date_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 0, date_item)
            
            # Day name column
            day_name = date_obj.strftime("%A")  # Monday, Tuesday, etc.
            day_item = QTableWidgetItem(day_name)
            day_item.setFlags(day_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            day_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 1, day_item)
            
            # File count column
            count_item = QTableWidgetItem(f"{file_count} files")
            count_item.setFlags(count_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            count_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 2, count_item)
            
            # Event name input (editable)
            event_item = QTableWidgetItem("")
            # Note: QTableWidgetItem doesn't have setPlaceholderText
            # The cell will be empty and editable
            self.table.setItem(row, 3, event_item)
    
    def use_same_name_for_all(self):
        """Use same event name for all dates"""
        from PyQt6.QtWidgets import QInputDialog
        
        text, ok = QInputDialog.getText(
            self,
            "Same Event Name",
            "Enter event name to use for all dates:",
            text="Event"
        )
        
        if ok and text.strip():
            for row in range(self.table.rowCount()):
                self.table.item(row, 3).setText(text.strip())
    
    def auto_name_by_date(self):
        """Auto-name events using date"""
        for row in range(self.table.rowCount()):
            date_str = self.table.item(row, 0).text()
            day_name = self.table.item(row, 1).text()
            auto_name = f"Event_{date_str}_{day_name}"
            self.table.item(row, 3).setText(auto_name)
    
    def clear_all_names(self):
        """Clear all event names"""
        for row in range(self.table.rowCount()):
            self.table.item(row, 3).setText("")
    
    def validate_and_accept(self):
        """Validate that all dates have event names"""
        self.event_mapping = {}
        empty_dates = []
        
        for row in range(self.table.rowCount()):
            date_str = self.table.item(row, 0).text()
            event_name = self.table.item(row, 3).text().strip()
            
            if not event_name:
                empty_dates.append(date_str)
            else:
                self.event_mapping[date_str] = event_name
        
        if empty_dates:
            QMessageBox.warning(
                self,
                "Missing Event Names",
                f"Please provide event names for the following dates:\n\n" +
                "\n".join(f"  • {date}" for date in empty_dates) +
                "\n\nYou can use 'Use Same Name for All' or 'Auto-Name by Date' buttons."
            )
            return
        
        # All dates have names, accept dialog
        self.accept()
    
    def get_event_mapping(self) -> Dict[str, str]:
        """
        Get the event mapping dictionary
        
        Returns:
            Dictionary mapping date string to event name
        """
        return self.event_mapping


# Example usage in main application:
"""
from multi_event_dialog import MultiEventDialog

# In your import button handler:
def start_import(self):
    # First, analyze dates in SD card
    date_groups = self.organizer.analyze_dates_in_sd(sd_path)
    
    if len(date_groups) == 0:
        QMessageBox.warning(self, "No Files", "No photos found on SD card")
        return
    
    if len(date_groups) == 1:
        # Only one date, use normal single-event import
        topic = self.topic_edit.text()
        self.organizer.organize_sd_files(sd_path, topic, move_files=True)
    else:
        # Multiple dates, show multi-event dialog
        dialog = MultiEventDialog(date_groups, self)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            event_mapping = dialog.get_event_mapping()
            
            # Start multi-event import
            self.organizer.organize_sd_files_multi_event(
                sd_path,
                event_mapping,
                move_files=True,
                progress_callback=self.update_progress
            )
"""
