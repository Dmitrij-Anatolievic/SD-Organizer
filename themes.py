# themes.py

STYLE_WARM_SUNSET = """
    QMainWindow { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FF5F6D, stop:1 #FFC371); color: #333333; }
    QLabel { color: #333333; }
    QGroupBox { border: 2px solid #E67E22; border-radius: 8px; margin-top: 1ex; font-weight: bold; color: #BF360C; font-size: 14px; }
    QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 8px; background-color: #E67E22; border-radius: 5px; }
    QPushButton { background-color: #F39C12; color: white; border-radius: 5px; padding: 10px 20px; font-weight: bold; font-size: 13px; border: 1px solid #D35400; }
    QPushButton:hover { background-color: #D35400; }
    QLineEdit, QSpinBox, QComboBox, QListWidget { background-color: white; color: #333333; border: 1px solid #F39C12; border-radius: 4px; padding: 4px; font-size: 13px; }
    QStatusBar { background-color: #D35400; color: white; border-top: 1px solid #F39C12; padding: 5px; font-size: 12px; }
    QProgressBar { border: 1px solid #F39C12; background-color: white; color: #333333; }
    QProgressBar::chunk { background-color: #E74C3C; }
    QCheckBox { color: #333333; }
    QTextEdit#consoleOutput { background-color: #333333; color: #F39C12; border: 1px solid #E67E22; padding: 5px; }
    QDialog { background-color: #FFC371; color: #333333; }
    QDialog QPushButton { background-color: #F39C12; color: white; border-radius: 5px; padding: 5px 10px; }
    QDialog QPushButton:hover { background-color: #D35400; }
"""

STYLE_COOL_OCEAN = """
    QMainWindow { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2C3E50, stop:1 #3498DB); color: #ECF0F1; }
    QLabel { color: #ECF0F1; }
    QGroupBox { border: 2px solid #2980B9; border-radius: 8px; margin-top: 1ex; font-weight: bold; color: #BBDEFB; font-size: 14px; }
    QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 8px; background-color: #2980B9; border-radius: 5px; }
    QPushButton { background-color: #1ABC9C; color: white; border-radius: 5px; padding: 10px 20px; font-weight: bold; font-size: 13px; border: 1px solid #16A085; }
    QPushButton:hover { background-color: #16A085; }
    QLineEdit, QSpinBox, QComboBox, QListWidget { background-color: #ECF0F1; color: #2C3E50; border: 1px solid #1ABC9C; border-radius: 4px; padding: 4px; font-size: 13px; }
    QStatusBar { background-color: #2980B9; color: #ECF0F1; border-top: 1px solid #3498DB; padding: 5px; font-size: 12px; }
    QProgressBar { border: 1px solid #1ABC9C; background-color: #ECF0F1; color: #2C3E50; }
    QProgressBar::chunk { background-color: #3498DB; }
    QCheckBox { color: #ECF0F1; }
    QTextEdit#consoleOutput { background-color: #2C3E50; color: #1ABC9C; border: 1px solid #2980B9; padding: 5px; }
    QDialog { background-color: #3498DB; color: #ECF0F1; }
    QDialog QPushButton { background-color: #1ABC9C; color: white; border-radius: 5px; padding: 5px 10px; }
    QDialog QPushButton:hover { background-color: #16A085; }
"""

STYLE_MONOCHROME_DARK = """
    QMainWindow { background-color: #212121; color: #F5F5F5; }
    QLabel { color: #F5F5F5; }
    QGroupBox { border: 2px solid #424242; border-radius: 8px; margin-top: 1ex; font-weight: bold; color: #BDBDBD; font-size: 14px; }
    QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 8px; background-color: #424242; border-radius: 5px; }
    QPushButton { background-color: #616161; color: white; border-radius: 5px; padding: 10px 20px; font-weight: bold; font-size: 13px; border: 1px solid #424242; }
    QPushButton:hover { background-color: #757575; }
    QLineEdit, QSpinBox, QComboBox, QListWidget { background-color: #424242; color: #F5F5F5; border: 1px solid #616161; border-radius: 4px; padding: 4px; font-size: 13px; }
    QStatusBar { background-color: #424242; color: #F5F5F5; border-top: 1px solid #212121; padding: 5px; font-size: 12px; }
    QProgressBar { border: 1px solid #616161; background-color: #424242; color: #F5F5F5; }
    QProgressBar::chunk { background-color: #9E9E9E; }
    QCheckBox { color: #F5F5F5; }
    QTextEdit#consoleOutput { background-color: #212121; color: #BDBDBD; border: 1px solid #424242; padding: 5px; }
    QDialog { background-color: #424242; color: #F5F5F5; }
    QDialog QPushButton { background-color: #616161; color: white; border-radius: 5px; padding: 5px 10px; }
    QDialog QPushButton:hover { background-color: #757575; }
"""

STYLE_MONOCHROME_LIGHT = """
    QMainWindow { background-color: #F5F5F5; color: #212121; }
    QLabel { color: #212121; }
    QGroupBox { border: 2px solid #E0E0E0; border-radius: 8px; margin-top: 1ex; font-weight: bold; color: #757575; font-size: 14px; }
    QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 8px; background-color: #E0E0E0; border-radius: 5px; }
    QPushButton { background-color: #BDBDBD; color: #212121; border-radius: 5px; padding: 10px 20px; font-weight: bold; font-size: 13px; border: 1px solid #9E9E9E; }
    QPushButton:hover { background-color: #E0E0E0; }
    QLineEdit, QSpinBox, QComboBox, QListWidget { background-color: white; color: #212121; border: 1px solid #BDBDBD; border-radius: 4px; padding: 4px; font-size: 13px; }
    QStatusBar { background-color: #E0E0E0; color: #212121; border-top: 1px solid #F5F5F5; padding: 5px; font-size: 12px; }
    QProgressBar { border: 1px solid #BDBDBD; background-color: white; color: #212121; }
    QProgressBar::chunk { background-color: #757575; }
    QCheckBox { color: #212121; }
    QTextEdit#consoleOutput { background-color: white; color: #212121; border: 1px solid #BDBDBD; padding: 5px; }
    QDialog { background-color: #F5F5F5; color: #212121; }
    QDialog QPushButton { background-color: #BDBDBD; color: #212121; border-radius: 5px; padding: 5px 10px; }
    QDialog QPushButton:hover { background-color: #E0E0E0; }
"""

STYLE_FOREST_GREEN = """
    QMainWindow { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2E7D32, stop:1 #4CAF50); color: #F1F8E9; }
    QLabel { color: #F1F8E9; }
    QGroupBox { border: 2px solid #388E3C; border-radius: 8px; margin-top: 1ex; font-weight: bold; color: #C5E1A5; font-size: 14px; }
    QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 8px; background-color: #388E3C; border-radius: 5px; }
    QPushButton { background-color: #689F38; color: white; border-radius: 5px; padding: 10px 20px; font-weight: bold; font-size: 13px; border: 1px solid #558B2F; }
    QPushButton:hover { background-color: #558B2F; }
    QLineEdit, QSpinBox, QComboBox, QListWidget { background-color: #F1F8E9; color: #2E7D32; border: 1px solid #689F38; border-radius: 4px; padding: 4px; font-size: 13px; }
    QStatusBar { background-color: #388E3C; color: #F1F8E9; border-top: 1px solid #2E7D32; padding: 5px; font-size: 12px; }
    QProgressBar { border: 1px solid #689F38; background-color: #F1F8E9; color: #2E7D32; }
    QProgressBar::chunk { background-color: #8BC34A; }
    QCheckBox { color: #F1F8E9; }
    QTextEdit#consoleOutput { background-color: #2E7D32; color: #C5E1A5; border: 1px solid #388E3C; padding: 5px; }
    QDialog { background-color: #4CAF50; color: #F1F8E9; }
    QDialog QPushButton { background-color: #689F38; color: white; border-radius: 5px; padding: 5px 10px; }
    QDialog QPushButton:hover { background-color: #558B2F; }
"""

STYLE_ROYAL_PURPLE = """
    QMainWindow { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4A148C, stop:1 #8E24AA); color: #FFEB3B; }
    QLabel { color: #FFEB3B; }
    QGroupBox { border: 2px solid #6A1B9A; border-radius: 8px; margin-top: 1ex; font-weight: bold; color: #E1BEE7; font-size: 14px; }
    QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 8px; background-color: #6A1B9A; border-radius: 5px; }
    QPushButton { background-color: #AB47BC; color: white; border-radius: 5px; padding: 10px 20px; font-weight: bold; font-size: 13px; border: 1px solid #8E24AA; }
    QPushButton:hover { background-color: #8E24AA; }
    QLineEdit, QSpinBox, QComboBox, QListWidget { background-color: #F3E5F5; color: #4A148C; border: 1px solid #AB47BC; border-radius: 4px; padding: 4px; font-size: 13px; }
    QStatusBar { background-color: #6A1B9A; color: #FFEB3B; border-top: 1px solid #4A148C; padding: 5px; font-size: 12px; }
    QProgressBar { border: 1px solid #AB47BC; background-color: #F3E5F5; color: #4A148C; }
    QProgressBar::chunk { background-color: #CDDC39; }
    QCheckBox { color: #FFEB3B; }
    QTextEdit#consoleOutput { background-color: #4A148C; color: #E1BEE7; border: 1px solid #6A1B9A; padding: 5px; }
    QDialog { background-color: #8E24AA; color: #F3E5F5; }
    QDialog QPushButton { background-color: #AB47BC; color: white; border-radius: 5px; padding: 5px 10px; }
    QDialog QPushButton:hover { background-color: #8E24AA; }
"""

STYLE_CYBERPUNK_NEON = """
    QMainWindow { background-color: #0A0A0A; color: #00FFFF; }
    QLabel { color: #00FFFF; }
    QGroupBox { border: 2px solid #FF00FF; border-radius: 8px; margin-top: 1ex; font-weight: bold; color: #FF00FF; font-size: 14px; }
    QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 8px; background-color: #333333; border-radius: 5px; }
    QPushButton { background-color: #00FF00; color: #0A0A0A; border-radius: 5px; padding: 10px 20px; font-weight: bold; font-size: 13px; border: 1px solid #00AA00; }
    QPushButton:hover { background-color: #FF00FF; color: #0A0A0A; }
    QLineEdit, QSpinBox, QComboBox, QListWidget { background-color: #222222; color: #00FFFF; border: 1px solid #00FFFF; border-radius: 4px; padding: 4px; font-size: 13px; }
    QStatusBar { background-color: #333333; color: #00FFFF; border-top: 1px solid #FF00FF; padding: 5px; font-size: 12px; }
    QProgressBar { border: 1px solid #00FFFF; background-color: #222222; color: #00FFFF; }
    QProgressBar::chunk { background-color: #FF00FF; }
    QCheckBox { color: #00FFFF; }
    QTextEdit#consoleOutput { background-color: #0A0A0A; color: #00FFFF; border: 1px solid #FF00FF; padding: 5px; }
    QDialog { background-color: #222222; color: #00FFFF; }
    QDialog QPushButton { background-color: #00FF00; color: #0A0A0A; border-radius: 5px; padding: 5px 10px; }
    QDialog QPushButton:hover { background-color: #FF00FF; color: #0A0A0A; }
"""

STYLE_PASTEL_DREAM = """
    QMainWindow { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FFD1DC, stop:1 #ADD8E6); color: #6A5ACD; }
    QLabel { color: #6A5ACD; }
    QGroupBox { border: 2px solid #B0E0E6; border-radius: 8px; margin-top: 1ex; font-weight: bold; color: #6A5ACD; font-size: 14px; }
    QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 8px; background-color: #E0BBE4; border-radius: 5px; }
    QPushButton { background-color: #C3B1E1; color: #333333; border-radius: 5px; padding: 10px 20px; font-weight: bold; font-size: 13px; border: 1px solid #A29BCC; }
    QPushButton:hover { background-color: #A29BCC; }
    QLineEdit, QSpinBox, QComboBox, QListWidget { background-color: white; color: #6A5ACD; border: 1px solid #C3B1E1; border-radius: 4px; padding: 4px; font-size: 13px; }
    QStatusBar { background-color: #B0E0E6; color: #6A5ACD; border-top: 1px solid #FFD1DC; padding: 5px; font-size: 12px; }
    QProgressBar { border: 1px solid #C3B1E1; background-color: white; color: #6A5ACD; }
    QProgressBar::chunk { background-color: #FFB6C1; }
    QCheckBox { color: #6A5ACD; }
    QTextEdit#consoleOutput { background-color: white; color: #6A5ACD; border: 1px solid #C3B1E1; padding: 5px; }
    QDialog { background-color: #ADD8E6; color: #6A5ACD; }
    QDialog QPushButton { background-color: #C3B1E1; color: #333333; border-radius: 5px; padding: 5px 10px; }
    QDialog QPushButton:hover { background-color: #A29BCC; }
"""

STYLE_VIBRANT_POP = """
    QMainWindow { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FF416C, stop:1 #FF4B2B); color: #FDFEFE; }
    QLabel { color: #FDFEFE; }
    QGroupBox { border: 2px solid #28B463; border-radius: 8px; margin-top: 1ex; font-weight: bold; color: #28B463; font-size: 14px; }
    QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 8px; background-color: #28B463; border-radius: 5px; }
    QPushButton { background-color: #3498DB; color: white; border-radius: 5px; padding: 10px 20px; font-weight: bold; font-size: 13px; border: 1px solid #217DBB; }
    QPushButton:hover { background-color: #217DBB; }
    QLineEdit, QSpinBox, QComboBox, QListWidget { background-color: #FDFEFE; color: #333333; border: 1px solid #3498DB; border-radius: 4px; padding: 4px; font-size: 13px; }
    QStatusBar { background-color: #28B463; color: #FDFEFE; border-top: 1px solid #FF416C; padding: 5px; font-size: 12px; }
    QProgressBar { border: 1px solid #3498DB; background-color: #FDFEFE; color: #333333; }
    QProgressBar::chunk { background-color: #FFC300; }
    QCheckBox { color: #FDFEFE; }
    QTextEdit#consoleOutput { background-color: #333333; color: #FDFEFE; border: 1px solid #28B463; padding: 5px; }
    QDialog { background-color: #FF4B2B; color: #FDFEFE; }
    QDialog QPushButton { background-color: #3498DB; color: white; border-radius: 5-px; padding: 5px 10px; }
    QDialog QPushButton:hover { background-color: #217DBB; }
"""

STYLE_INDUSTRIAL_STEEL = """
    QMainWindow { background-color: #424242; color: #E0E0E0; }
    QLabel { color: #E0E0E0; }
    QGroupBox { border: 2px solid #616161; border-radius: 8px; margin-top: 1ex; font-weight: bold; color: #B0BEC5; font-size: 14px; }
    QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 8px; background-color: #616161; border-radius: 5px; }
    QPushButton { background-color: #78909C; color: white; border-radius: 5px; padding: 10px 20px; font-weight: bold; font-size: 13px; border: 1px solid #546E7A; }
    QPushButton:hover { background-color: #546E7A; }
    QLineEdit, QSpinBox, QComboBox, QListWidget { background-color: #616161; color: #E0E0E0; border: 1px solid #78909C; border-radius: 4px; padding: 4px; font-size: 13px; }
    QStatusBar { background-color: #616161; color: #E0E0E0; border-top: 1px solid #424242; padding: 5px; font-size: 12px; }
    QProgressBar { border: 1px solid #78909C; background-color: #616161; color: #E0E0E0; }
    QProgressBar::chunk { background-color: #9E9E9E; }
    QCheckBox { color: #E0E0E0; }
    QTextEdit#consoleOutput { background-color: #424242; color: #E0E0E0; border: 1px solid #616161; padding: 5px; }
    QDialog { background-color: #616161; color: #E0E0E0; }
    QDialog QPushButton { background-color: #78909C; color: white; border-radius: 5px; padding: 5px 10px; }
    QDialog QPushButton:hover { background-color: #546E7A; }
"""

STYLE_DEEP_FOREST = """
    QMainWindow { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #004D40, stop:1 #1B5E20); color: #DCEDC8; }
    QLabel { color: #DCEDC8; }
    QGroupBox { border: 2px solid #2E7D32; border-radius: 8px; margin-top: 1ex; font-weight: bold; color: #8BC34A; font-size: 14px; }
    QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 8px; background-color: #2E7D32; border-radius: 5px; }
    QPushButton { background-color: #4CAF50; color: white; border-radius: 5px; padding: 10px 20px; font-weight: bold; font-size: 13px; border: 1px solid #388E3C; }
    QPushButton:hover { background-color: #388E3C; }
    QLineEdit, QSpinBox, QComboBox, QListWidget { background-color: #E8F5E9; color: #004D40; border: 1px solid #4CAF50; border-radius: 4px; padding: 4px; font-size: 13px; }
    QStatusBar { background-color: #2E7D32; color: #DCEDC8; border-top: 1px solid #004D40; padding: 5px; font-size: 12px; }
    QProgressBar { border: 1px solid #4CAF50; background-color: #E8F5E9; color: #004D40; }
    QProgressBar::chunk { background-color: #A5D6A7; }
    QCheckBox { color: #DCEDC8; }
    QTextEdit#consoleOutput { background-color: #004D40; color: #DCEDC8; border: 1px solid #2E7D32; padding: 5px; }
    QDialog { background-color: #1B5E20; color: #DCEDC8; }
    QDialog QPushButton { background-color: #4CAF50; color: white; border-radius: 5px; padding: 5px 10px; }
    QDialog QPushButton:hover { background-color: #388E3C; }
"""

STYLE_AUTUMN_HARVEST = """
    QMainWindow { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #C0392B, stop:1 #D35400); color: #FDEBD0; }
    QLabel { color: #FDEBD0; }
    QGroupBox { border: 2px solid #E67E22; border-radius: 8px; margin-top: 1ex; font-weight: bold; color: #F39C12; font-size: 14px; }
    QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 8px; background-color: #D35400; border-radius: 5px; }
    QPushButton { background-color: #E74C3C; color: white; border-radius: 5px; padding: 10px 20px; font-weight: bold; font-size: 13px; border: 1px solid #C0392B; }
    QPushButton:hover { background-color: #C0392B; }
    QLineEdit, QSpinBox, QComboBox, QListWidget { background-color: #FDEBD0; color: #C0392B; border: 1px solid #E74C3C; border-radius: 4px; padding: 4px; font-size: 13px; }
    QStatusBar { background-color: #D35400; color: #FDEBD0; border-top: 1px solid #C0392B; padding: 5px; font-size: 12px; }
    QProgressBar { border: 1px solid #E74C3C; background-color: #FDEBD0; color: #C0392B; }
    QProgressBar::chunk { background-color: #E67E22; }
    QCheckBox { color: #FDEBD0; }
    QTextEdit#consoleOutput { background-color: #C0392B; color: #FDEBD0; border: 1px solid #D35400; padding: 5px; }
    QDialog { background-color: #D35400; color: #FDEBD0; }
    QDialog QPushButton { background-color: #E74C3C; color: white; border-radius: 5px; padding: 5px 10px; }
    QDialog QPushButton:hover { background-color: #C0392B; }
"""

STYLE_MIDNIGHT_SKY = """
    QMainWindow { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0D1B2A, stop:1 #1B263B); color: #E0E1DD; }
    QLabel { color: #E0E1DD; }
    QGroupBox { border: 2px solid #415A77; border-radius: 8px; margin-top: 1ex; font-weight: bold; color: #778DA9; font-size: 14px; }
    QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 8px; background-color: #1B263B; border-radius: 5px; }
    QPushButton { background-color: #0D1B2A; color: white; border-radius: 5px; padding: 10px 20px; font-weight: bold; font-size: 13px; border: 1px solid #415A77; }
    QPushButton:hover { background-color: #415A77; }
    QLineEdit, QSpinBox, QComboBox, QListWidget { background-color: #2D3A50; color: #E0E1DD; border: 1px solid #778DA9; border-radius: 4px; padding: 4px; font-size: 13px; }
    QStatusBar { background-color: #1B263B; color: #E0E1DD; border-top: 1px solid #0D1B2A; padding: 5px; font-size: 12px; }
    QProgressBar { border: 1px solid #778DA9; background-color: #2D3A50; color: #E0E1DD; }
    QProgressBar::chunk { background-color: #1B263B; }
    QCheckBox { color: #E0E1DD; }
    QTextEdit#consoleOutput { background-color: #0D1B2A; color: #E0E1DD; border: 1px solid #415A77; padding: 5px; }
    QDialog { background-color: #1B263B; color: #E0E1DD; }
    QDialog QPushButton { background-color: #0D1B2A; color: white; border-radius: 5px; padding: 5px 10px; }
    QDialog QPushButton:hover { background-color: #415A77; }
"""

STYLE_OCEAN_BREEZE = """
    QMainWindow { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #A1C4FD, stop:1 #C2E9FB); color: #34495E; }
    QLabel { color: #34495E; }
    QGroupBox { border: 2px solid #85C1E9; border-radius: 8px; margin-top: 1ex; font-weight: bold; color: #34495E; font-size: 14px; }
    QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 8px; background-color: #A1C4FD; border-radius: 5px; }
    QPushButton { background-color: #5DADE2; color: white; border-radius: 5px; padding: 10px 20px; font-weight: bold; font-size: 13px; border: 1px solid #3498DB; }
    QPushButton:hover { background-color: #3498DB; }
    QLineEdit, QSpinBox, QComboBox, QListWidget { background-color: white; color: #34495E; border: 1px solid #5DADE2; border-radius: 4px; padding: 4px; font-size: 13px; }
    QStatusBar { background-color: #85C1E9; color: #34495E; border-top: 1px solid #A1C4FD; padding: 5px; font-size: 12px; }
    QProgressBar { border: 1px solid #5DADE2; background-color: white; color: #34495E; }
    QProgressBar::chunk { background-color: #C2E9FB; }
    QCheckBox { color: #34495E; }
    QTextEdit#consoleOutput { background-color: white; color: #34495E; border: 1px solid #85C1E9; padding: 5px; }
    QDialog { background-color: #C2E9FB; color: #34495E; }
    QDialog QPushButton { background-color: #5DADE2; color: white; border-radius: 5px; padding: 5px 10px; }
    QDialog QPushButton:hover { background-color: #3498DB; }
"""

STYLE_GRAPE_CRUSH = """
    QMainWindow { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #6A1B9A, stop:1 #9C27B0); color: #E1BEE7; }
    QLabel { color: #E1BEE7; }
    QGroupBox { border: 2px solid #8E24AA; border-radius: 8px; margin-top: 1ex; font-weight: bold; color: #CE93D8; font-size: 14px; }
    QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 8px; background-color: #6A1B9A; border-radius: 5px; }
    QPushButton { background-color: #AB47BC; color: white; border-radius: 5px; padding: 10px 20px; font-weight: bold; font-size: 13px; border: 1px solid #8E24AA; }
    QPushButton:hover { background-color: #8E24AA; }
    QLineEdit, QSpinBox, QComboBox, QListWidget { background-color: #F3E5F5; color: #6A1B9A; border: 1px solid #AB47BC; border-radius: 4px; padding: 4px; font-size: 13px; }
    QStatusBar { background-color: #8E24AA; color: #E1BEE7; border-top: 1px solid #6A1B9A; padding: 5px; font-size: 12px; }
    QProgressBar { border: 1px solid #AB47BC; background-color: #F3E5F5; color: #6A1B9A; }
    QProgressBar::chunk { background-color: #BA68C8; }
    QCheckBox { color: #E1BEE7; }
    QTextEdit#consoleOutput { background-color: #6A1B9A; color: #F3E5F5; border: 1px solid #8E24AA; padding: 5px; }
    QDialog { background-color: #9C27B0; color: #F3E5F5; }
    QDialog QPushButton { background-color: #AB47BC; color: white; border-radius: 5px; padding: 5px 10px; }
    QDialog QPushButton:hover { background-color: #8E24AA; }
"""

STYLE_SUNSET_ORANGE = """
    QMainWindow { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #F37335, stop:1 #FDC830); color: #333333; }
    QLabel { color: #333333; }
    QGroupBox { border: 2px solid #FF8C00; border-radius: 8px; margin-top: 1ex; font-weight: bold; color: #CD5700; font-size: 14px; }
    QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 8px; background-color: #FFA500; border-radius: 5px; }
    QPushButton { background-color: #FF8C00; color: white; border-radius: 5px; padding: 10px 20px; font-weight: bold; font-size: 13px; border: 1px solid #CD5700; }
    QPushButton:hover { background-color: #CD5700; }
    QLineEdit, QSpinBox, QComboBox, QListWidget { background-color: white; color: #333333; border: 1px solid #FF8C00; border-radius: 4px; padding: 4px; font-size: 13px; }
    QStatusBar { background-color: #FFA500; color: white; border-top: 1px solid #FF8C00; padding: 5px; font-size: 12px; }
    QProgressBar { border: 1px solid #FF8C00; background-color: white; color: #333333; }
    QProgressBar::chunk { background-color: #FFA500; }
    QCheckBox { color: #333333; }
    QTextEdit#consoleOutput { background-color: #333333; color: #FF8C00; border: 1px solid #FFA500; padding: 5px; }
    QDialog { background-color: #FFC371; color: #333333; }
    QDialog QPushButton { background-color: #FF8C00; color: white; border-radius: 5px; padding: 5px 10px; }
    QDialog QPushButton:hover { background-color: #CD5700; }
"""

STYLE_RUSTIC_EARTH = """
    QMainWindow { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #795548, stop:1 #BCAAA4); color: #EFEBE9; }
    QLabel { color: #EFEBE9; }
    QGroupBox { border: 2px solid #8D6E63; border-radius: 8px; margin-top: 1ex; font-weight: bold; color: #A1887F; font-size: 14px; }
    QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 8px; background-color: #8D6E63; border-radius: 5px; }
    QPushButton { background-color: #A1887F; color: white; border-radius: 5px; padding: 10px 20px; font-weight: bold; font-size: 13px; border: 1px solid #6D4C41; }
    QPushButton:hover { background-color: #6D4C41; }
    QLineEdit, QSpinBox, QComboBox, QListWidget { background-color: #EFEBE9; color: #795548; border: 1px solid #A1887F; border-radius: 4px; padding: 4px; font-size: 13px; }
    QStatusBar { background-color: #8D6E63; color: #EFEBE9; border-top: 1px solid #795548; padding: 5px; font-size: 12px; }
    QProgressBar { border: 1px solid #A1887F; background-color: #EFEBE9; color: #795548; }
    QProgressBar::chunk { background-color: #C5A188; }
    QCheckBox { color: #EFEBE9; }
    QTextEdit#consoleOutput { background-color: #795548; color: #EFEBE9; border: 1px solid #8D6E63; padding: 5px; }
    QDialog { background-color: #BCAAA4; color: #EFEBE9; }
    QDialog QPushButton { background-color: #A1887F; color: white; border-radius: 5px; padding: 5px 10px; }
    QDialog QPushButton:hover { background-color: #6D4C41; }
"""

STYLE_AQUATIC_BLUE = """
    QMainWindow { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1E90FF, stop:1 #4682B4); color: white; }
    QLabel { color: white; }
    QGroupBox { border: 2px solid #00BFFF; border-radius: 8px; margin-top: 1ex; font-weight: bold; color: #B0E0E6; font-size: 14px; }
    QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 8px; background-color: #00BFFF; border-radius: 5px; }
    QPushButton { background-color: #4682B4; color: white; border-radius: 5px; padding: 10px 20px; font-weight: bold; font-size: 13px; border: 1px solid #1E90FF; }
    QPushButton:hover { background-color: #1E90FF; }
    QLineEdit, QSpinBox, QComboBox, QListWidget { background-color: white; color: #1E90FF; border: 1px solid #4682B4; border-radius: 4px; padding: 4px; font-size: 13px; }
    QStatusBar { background-color: #00BFFF; color: white; border-top: 1px solid #1E90FF; padding: 5px; font-size: 12px; }
    QProgressBar { border: 1px solid #4682B4; background-color: white; color: #1E90FF; }
    QProgressBar::chunk { background-color: #87CEEB; }
    QCheckBox { color: white; }
    QTextEdit#consoleOutput { background-color: #1E90FF; color: white; border: 1px solid #00BFFF; padding: 5px; }
    QDialog { background-color: #4682B4; color: white; }
    QDialog QPushButton { background-color: #4682B4; color: white; border-radius: 5px; padding: 5px 10px; }
    QDialog QPushButton:hover { background-color: #1E90FF; }
"""

STYLE_LAVENDER_FIELDS = """
    QMainWindow { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #9370DB, stop:1 #E6E6FA); color: #4B0082; }
    QLabel { color: #4B0082; }
    QGroupBox { border: 2px solid #BA55D3; border-radius: 8px; margin-top: 1ex; font-weight: bold; color: #8A2BE2; font-size: 14px; }
    QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 8px; background-color: #BA55D3; border-radius: 5px; }
    QPushButton { background-color: #9400D3; color: white; border-radius: 5px; padding: 10px 20px; font-weight: bold; font-size: 13px; border: 1px solid #8A2BE2; }
    QPushButton:hover { background-color: #8A2BE2; }
    QLineEdit, QSpinBox, QComboBox, QListWidget { background-color: white; color: #4B0082; border: 1px solid #9400D3; border-radius: 4px; padding: 4px; font-size: 13px; }
    QStatusBar { background-color: #BA55D3; color: #4B0082; border-top: 1px solid #9370DB; padding: 5px; font-size: 12px; }
    QProgressBar { border: 1px solid #9400D3; background-color: white; color: #4B0082; }
    QProgressBar::chunk { background-color: #E0BBE4; }
    QCheckBox { color: #4B0082; }
    QTextEdit#consoleOutput { background-color: white; color: #4B0082; border: 1px solid #BA55D3; padding: 5px; }
    QDialog { background-color: #E6E6FA; color: #4B0082; }
    QDialog QPushButton { background-color: #9400D3; color: white; border-radius: 5px; padding: 5px 10px; }
    QDialog QPushButton:hover { background-color: #8A2BE2; }
"""

STYLE_EMERALD_CITY = """
    QMainWindow { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #006400, stop:1 #228B22); color: #F0FFF0; }
    QLabel { color: #F0FFF0; }
    QGroupBox { border: 2px solid #008000; border-radius: 8px; margin-top: 1ex; font-weight: bold; color: #32CD32; font-size: 14px; }
    QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 8px; background-color: #008000; border-radius: 5px; }
    QPushButton { background-color: #3CB371; color: white; border-radius: 5px; padding: 10px 20px; font-weight: bold; font-size: 13px; border: 1px solid #2E8B57; }
    QPushButton:hover { background-color: #2E8B57; }
    QLineEdit, QSpinBox, QComboBox, QListWidget { background-color: #F0FFF0; color: #006400; border: 1px solid #3CB371; border-radius: 4px; padding: 4px; font-size: 13px; }
    QStatusBar { background-color: #008000; color: #F0FFF0; border-top: 1px solid #006400; padding: 5px; font-size: 12px; }
    QProgressBar { border: 1px solid #3CB371; background-color: #F0FFF0; color: #006400; }
    QProgressBar::chunk { background-color: #66CDAA; }
    QCheckBox { color: #F0FFF0; }
    QTextEdit#consoleOutput { background-color: #006400; color: #F0FFF0; border: 1px solid #008000; padding: 5px; }
    QDialog { background-color: #228B22; color: #F0FFF0; }
    QDialog QPushButton { background-color: #3CB371; color: white; border-radius: 5px; padding: 5px 10px; }
    QDialog QPushButton:hover { background-color: #2E8B57; }
"""

STYLE_FIERY_FLAME = """
    QMainWindow { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #E53935, stop:1 #FF7043); color: white; }
    QLabel { color: white; }
    QGroupBox { border: 2px solid #D32F2F; border-radius: 8px; margin-top: 1ex; font-weight: bold; color: #FFCDD2; font-size: 14px; }
    QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 8px; background-color: #D32F2F; border-radius: 5px; }
    QPushButton { background-color: #FF5252; color: white; border-radius: 5px; padding: 10px 20px; font-weight: bold; font-size: 13px; border: 1px solid #E53935; }
    QPushButton:hover { background-color: #E53935; }
    QLineEdit, QSpinBox, QComboBox, QListWidget { background-color: #FFCDD2; color: #E53935; border: 1px solid #FF5252; border-radius: 4px; padding: 4px; font-size: 13px; }
    QStatusBar { background-color: #D32F2F; color: white; border-top: 1px solid #E53935; padding: 5px; font-size: 12px; }
    QProgressBar { border: 1px solid #FF5252; background-color: #FFCDD2; color: #E53935; }
    QProgressBar::chunk { background-color: #FF7043; }
    QCheckBox { color: white; }
    QTextEdit#consoleOutput { background-color: #E53935; color: white; border: 1px solid #D32F2F; padding: 5px; }
    QDialog { background-color: #FF7043; color: white; }
    QDialog QPushButton { background-color: #FF5252; color: white; border-radius: 5px; padding: 5px 10px; }
    QDialog QPushButton:hover { background-color: #E53935; }
"""

STYLE_NIGHT_SKY = """
    QMainWindow { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #121212, stop:1 #212121); color: #B0BEC5; }
    QLabel { color: #B0BEC5; }
    QGroupBox { border: 2px solid #37474F; border-radius: 8px; margin-top: 1ex; font-weight: bold; color: #546E7A; font-size: 14px; }
    QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 8px; background-color: #37474F; border-radius: 5px; }
    QPushButton { background-color: #546E7A; color: white; border-radius: 5px; padding: 10px 20px; font-weight: bold; font-size: 13px; border: 1px solid #455A64; }
    QPushButton:hover { background-color: #455A64; }
    QLineEdit, QSpinBox, QComboBox, QListWidget { background-color: #263238; color: #B0BEC5; border: 1px solid #546E7A; border-radius: 4px; padding: 4px; font-size: 13px; }
    QStatusBar { background-color: #37474F; color: #B0BEC5; border-top: 1px solid #121212; padding: 5px; font-size: 12px; }
    QProgressBar { border: 1px solid #546E7A; background-color: #263238; color: #B0BEC5; }
    QProgressBar::chunk { background-color: #78909C; }
    QCheckBox { color: #B0BEC5; }
    QTextEdit#consoleOutput { background-color: #121212; color: #B0BEC5; border: 1px solid #37474F; padding: 5px; }
    QDialog { background-color: #212121; color: #B0BEC5; }
    QDialog QPushButton { background-color: #546E7A; color: white; border-radius: 5px; padding: 5px 10px; }
    QDialog QPushButton:hover { background-color: #455A64; }
"""

STYLE_VINTAGE_SEPIA = """
    QMainWindow { background-color: #7B684B; color: #FFF8DC; }
    QLabel { color: #FFF8DC; }
    QGroupBox { border: 2px solid #A08F6B; border-radius: 8px; margin-top: 1ex; font-weight: bold; color: #C8B99A; font-size: 14px; }
    QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 8px; background-color: #A08F6B; border-radius: 5px; }
    QPushButton { background-color: #B2A281; color: white; border-radius: 5px; padding: 10px 20px; font-weight: bold; font-size: 13px; border: 1px solid #9A8D68; }
    QPushButton:hover { background-color: #9A8D68; }
    QLineEdit, QSpinBox, QComboBox, QListWidget { background-color: #FFF8DC; color: #7B684B; border: 1px solid #B2A281; border-radius: 4px; padding: 4px; font-size: 13px; }
    QStatusBar { background-color: #A08F6B; color: #FFF8DC; border-top: 1px solid #7B684B; padding: 5px; font-size: 12px; }
    QProgressBar { border: 1px solid #B2A281; background-color: #FFF8DC; color: #7B684B; }
    QProgressBar::chunk { background-color: #D2C2A1; }
    QCheckBox { color: #FFF8DC; }
    QTextEdit#consoleOutput { background-color: #7B684B; color: #FFF8DC; border: 1px solid #A08F6B; padding: 5px; }
    QDialog { background-color: #A08F6B; color: #FFF8DC; }
    QDialog QPushButton { background-color: #B2A281; color: white; border-radius: 5px; padding: 5px 10px; }
    QDialog QPushButton:hover { background-color: #9A8D68; }
"""

STYLE_CRIMSON_TIDE = """
    QMainWindow { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #8B0000, stop:1 #A52A2A); color: white; }
    QLabel { color: white; }
    QGroupBox { border: 2px solid #DC143C; border-radius: 8px; margin-top: 1ex; font-weight: bold; color: #F08080; font-size: 14px; }
    QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 8px; background-color: #DC143C; border-radius: 5px; }
    QPushButton { background-color: #B22222; color: white; border-radius: 5px; padding: 10px 20px; font-weight: bold; font-size: 13px; border: 1px solid #8B0000; }
    QPushButton:hover { background-color: #8B0000; }
    QLineEdit, QSpinBox, QComboBox, QListWidget { background-color: white; color: #8B0000; border: 1px solid #B22222; border-radius: 4px; padding: 4px; font-size: 13px; }
    QStatusBar { background-color: #DC143C; color: white; border-top: 1px solid #8B0000; padding: 5px; font-size: 12px; }
    QProgressBar { border: 1px solid #B22222; background-color: white; color: #8B0000; }
    QProgressBar::chunk { background-color: #CD5C5C; }
    QCheckBox { color: white; }
    QTextEdit#consoleOutput { background-color: #8B0000; color: white; border: 1px solid #DC143C; padding: 5px; }
    QDialog { background-color: #A52A2A; color: white; }
    QDialog QPushButton { background-color: #B22222; color: white; border-radius: 5px; padding: 5px 10px; }
    QDialog QPushButton:hover { background-color: #8B0000; }
"""

STYLE_MINTY_FRESH = """
    QMainWindow { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #D4EDDA, stop:1 #C8E6C9); color: #388E3C; }
    QLabel { color: #388E3C; }
    QGroupBox { border: 2px solid #81C784; border-radius: 8px; margin-top: 1ex; font-weight: bold; color: #66BB6A; font-size: 14px; }
    QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 8px; background-color: #A5D6A7; border-radius: 5px; }
    QPushButton { background-color: #4CAF50; color: white; border-radius: 5px; padding: 10px 20px; font-weight: bold; font-size: 13px; border: 1px solid #388E3C; }
    QPushButton:hover { background-color: #388E3C; }
    QLineEdit, QSpinBox, QComboBox, QListWidget { background-color: white; color: #388E3C; border: 1px solid #4CAF50; border-radius: 4px; padding: 4px; font-size: 13px; }
    QStatusBar { background-color: #81C784; color: #388E3C; border-top: 1px solid #D4EDDA; padding: 5px; font-size: 12px; }
    QProgressBar { border: 1px solid #4CAF50; background-color: white; color: #388E3C; }
    QProgressBar::chunk { background-color: #A5D6A7; }
    QCheckBox { color: #388E3C; }
    QTextEdit#consoleOutput { background-color: white; color: #388E3C; border: 1px solid #81C784; padding: 5px; }
    QDialog { background-color: #C8E6C9; color: #388E3C; }
    QDialog QPushButton { background-color: #4CAF50; color: white; border-radius: 5px; padding: 5px 10px; }
    QDialog QPushButton:hover { background-color: #388E3C; }
"""

STYLE_DESERT_SAND = """
    QMainWindow { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #D2B48C, stop:1 #F5F5DC); color: #5D4037; }
    QLabel { color: #5D4037; }
    QGroupBox { border: 2px solid #8D6E63; border-radius: 8px; margin-top: 1ex; font-weight: bold; color: #A1887F; font-size: 14px; }
    QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 8px; background-color: #8D6E63; border-radius: 5px; }
    QPushButton { background-color: #A1887F; color: white; border-radius: 5px; padding: 10px 20px; font-weight: bold; font-size: 13px; border: 1px solid #795548; }
    QPushButton:hover { background-color: #795548; }
    QLineEdit, QSpinBox, QComboBox, QListWidget { background-color: #F5F5DC; color: #5D4037; border: 1px solid #A1887F; border-radius: 4px; padding: 4px; font-size: 13px; }
    QStatusBar { background-color: #8D6E63; color: #5D4037; border-top: 1px solid #D2B48C; padding: 5px; font-size: 12px; }
    QProgressBar { border: 1px solid #A1887F; background-color: #F5F5DC; color: #5D4037; }
    QProgressBar::chunk { background-color: #CDBA96; }
    QCheckBox { color: #5D4037; }
    QTextEdit#consoleOutput { background-color: #D2B48C; color: #5D4037; border: 1px solid #8D6E63; padding: 5px; }
    QDialog { background-color: #F5F5DC; color: #5D4037; }
    QDialog QPushButton { background-color: #A1887F; color: white; border-radius: 5px; padding: 5px 10px; }
    QDialog QPushButton:hover { background-color: #795548; }
"""

STYLE_GALAXY_NIGHT = """
    QMainWindow { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0F0E28, stop:1 #2C0F4A); color: #DCDCDC; }
    QLabel { color: #DCDCDC; }
    QGroupBox { border: 2px solid #4B0082; border-radius: 8px; margin-top: 1ex; font-weight: bold; color: #8A2BE2; font-size: 14px; }
    QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 8px; background-color: #4B0082; border-radius: 5px; }
    QPushButton { background-color: #6A1B9A; color: white; border-radius: 5px; padding: 10px 20px; font-weight: bold; font-size: 13px; border: 1px solid #4B0082; }
    QPushButton:hover { background-color: #8A2BE2; }
    QLineEdit, QSpinBox, QComboBox, QListWidget { background-color: #1A0A33; color: #DCDCDC; border: 1px solid #6A1B9A; border-radius: 4px; padding: 4px; font-size: 13px; }
    QStatusBar { background-color: #4B0082; color: #DCDCDC; border-top: 1px solid #0F0E28; padding: 5px; font-size: 12px; }
    QProgressBar { border: 1px solid #6A1B9A; background-color: #1A0A33; color: #DCDCDC; }
    QProgressBar::chunk { background-color: #9400D3; }
    QCheckBox { color: #DCDCDC; }
    QTextEdit#consoleOutput { background-color: #0F0E28; color: #DCDCDC; border: 1px solid #4B0082; padding: 5px; }
    QDialog { background-color: #2C0F4A; color: #DCDCDC; }
    QDialog QPushButton { background-color: #6A1B9A; color: white; border-radius: 5px; padding: 5px 10px; }
    QDialog QPushButton:hover { background-color: #8A2BE2; }
"""

STYLE_MORNING_DEW = """
    QMainWindow { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #E0FFFF, stop:1 #F0FFFF); color: #2F4F4F; }
    QLabel { color: #2F4F4F; }
    QGroupBox { border: 2px solid #AFEEEE; border-radius: 8px; margin-top: 1ex; font-weight: bold; color: #87CEEB; font-size: 14px; }
    QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 8px; background-color: #B0E0E6; border-radius: 5px; }
    QPushButton { background-color: #B0E0E6; color: #2F4F4F; border-radius: 5px; padding: 10px 20px; font-weight: bold; font-size: 13px; border: 1px solid #87CEEB; }
    QPushButton:hover { background-color: #87CEEB; }
    QLineEdit, QSpinBox, QComboBox, QListWidget { background-color: white; color: #2F4F4F; border: 1px solid #B0E0E6; border-radius: 4px; padding: 4px; font-size: 13px; }
    QStatusBar { background-color: #AFEEEE; color: #2F4F4F; border-top: 1px solid #E0FFFF; padding: 5px; font-size: 12px; }
    QProgressBar { border: 1px solid #B0E0E6; background-color: white; color: #2F4F4F; }
    QProgressBar::chunk { background-color: #ADD8E6; }
    QCheckBox { color: #2F4F4F; }
    QTextEdit#consoleOutput { background-color: white; color: #2F4F4F; border: 1px solid #AFEEEE; padding: 5px; }
    QDialog { background-color: #F0FFFF; color: #2F4F4F; }
    QDialog QPushButton { background-color: #B0E0E6; color: #2F4F4F; border-radius: 5px; padding: 5px 10px; }
    QDialog QPushButton:hover { background-color: #87CEEB; }
"""

STYLE_VOLCANIC_ASH = """
    QMainWindow { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #333333, stop:1 #444444); color: #D3D3D3; }
    QLabel { color: #D3D3D3; }
    QGroupBox { border: 2px solid #555555; border-radius: 8px; margin-top: 1ex; font-weight: bold; color: #9A9A9A; font-size: 14px; }
    QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 8px; background-color: #555555; border-radius: 5px; }
    QPushButton { background-color: #666666; color: white; border-radius: 5px; padding: 10px 20px; font-weight: bold; font-size: 13px; border: 1px solid #555555; }
    QPushButton:hover { background-color: #777777; }
    QLineEdit, QSpinBox, QComboBox, QListWidget { background-color: #444444; color: #D3D3D3; border: 1px solid #666666; border-radius: 4px; padding: 4px; font-size: 13px; }
    QStatusBar { background-color: #555555; color: #D3D3D3; border-top: 1px solid #333333; padding: 5px; font-size: 12px; }
    QProgressBar { border: 1px solid #666666; background-color: #444444; color: #D3D3D3; }
    QProgressBar::chunk { background-color: #777777; }
    QCheckBox { color: #D3D3D3; }
    QTextEdit#consoleOutput { background-color: #333333; color: #D3D3D3; border: 1px solid #555555; padding: 5px; }
    QDialog { background-color: #444444; color: #D3D3D3; }
    QDialog QPushButton { background-color: #666666; color: white; border-radius: 5px; padding: 5px 10px; }
    QDialog QPushButton:hover { background-color: #777777; }
"""

STYLE_HONEY_GOLD = """
    QMainWindow { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FFD700, stop:1 #DAA520); color: #5D4037; }
    QLabel { color: #5D4037; }
    QGroupBox { border: 2px solid #FFC107; border-radius: 8px; margin-top: 1ex; font-weight: bold; color: #FFB300; font-size: 14px; }
    QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 8px; background-color: #FFC107; border-radius: 5px; }
    QPushButton { background-color: #FFC107; color: #5D4037; border-radius: 5px; padding: 10px 20px; font-weight: bold; font-size: 13px; border: 1px solid #FFB300; }
    QPushButton:hover { background-color: #FFB300; }
    QLineEdit, QSpinBox, QComboBox, QListWidget { background-color: white; color: #5D4037; border: 1px solid #FFC107; border-radius: 4px; padding: 4px; font-size: 13px; }
    QStatusBar { background-color: #FFC107; color: #5D4037; border-top: 1px solid #FFD700; padding: 5px; font-size: 12px; }
    QProgressBar { border: 1px solid #FFC107; background-color: white; color: #5D4037; }
    QProgressBar::chunk { background-color: #DAA520; }
    QCheckBox { color: #5D4037; }
    QTextEdit#consoleOutput { background-color: #FFD700; color: #5D4037; border: 1px solid #FFC107; padding: 5px; }
    QDialog { background-color: #DAA520; color: #5D4037; }
    QDialog QPushButton { background-color: #FFC107; color: #5D4037; border-radius: 5px; padding: 5px 10px; }
    QDialog QPushButton:hover { background-color: #FFB300; }
"""

STYLE_ARCTIC_FROST = """
    QMainWindow { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #B0E0E6, stop:1 #ADD8E6); color: #34495E; }
    QLabel { color: #34495E; }
    QGroupBox { border: 2px solid #87CEFA; border-radius: 8px; margin-top: 1ex; font-weight: bold; color: #6495ED; font-size: 14px; }
    QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 8px; background-color: #87CEFA; border-radius: 5px; }
    QPushButton { background-color: #4682B4; color: white; border-radius: 5px; padding: 10px 20px; font-weight: bold; font-size: 13px; border: 1px solid #6495ED; }
    QPushButton:hover { background-color: #6495ED; }
    QLineEdit, QSpinBox, QComboBox, QListWidget { background-color: white; color: #34495E; border: 1px solid #4682B4; border-radius: 4px; padding: 4px; font-size: 13px; }
    QStatusBar { background-color: #87CEFA; color: #34495E; border-top: 1px solid #B0E0E6; padding: 5px; font-size: 12px; }
    QProgressBar { border: 1px solid #4682B4; background-color: white; color: #34495E; }
    QProgressBar::chunk { background-color: #B0E0E6; }
    QCheckBox { color: #34495E; }
    QTextEdit#consoleOutput { background-color: white; color: #34495E; border: 1px solid #87CEFA; padding: 5px; }
    QDialog { background-color: #ADD8E6; color: #34495E; }
    QDialog QPushButton { background-color: #4682B4; color: white; border-radius: 5px; padding: 5px 10px; }
    QDialog QPushButton:hover { background-color: #6495ED; }
"""

STYLE_CRIMSON_PEAK = """
    QMainWindow { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #A52A2A, stop:1 #B22222); color: #F5F5F5; }
    QLabel { color: #F5F5F5; }
    QGroupBox { border: 2px solid #DC143C; border-radius: 8px; margin-top: 1ex; font-weight: bold; color: #F08080; font-size: 14px; }
    QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 8px; background-color: #DC143C; border-radius: 5px; }
    QPushButton { background-color: #B22222; color: white; border-radius: 5px; padding: 10px 20px; font-weight: bold; font-size: 13px; border: 1px solid #A52A2A; }
    QPushButton:hover { background-color: #A52A2A; }
    QLineEdit, QSpinBox, QComboBox, QListWidget { background-color: #F5F5F5; color: #A52A2A; border: 1px solid #B22222; border-radius: 4px; padding: 4px; font-size: 13px; }
    QStatusBar { background-color: #DC143C; color: #F5F5F5; border-top: 1px solid #A52A2A; padding: 5px; font-size: 12px; }
    QProgressBar { border: 1px solid #B22222; background-color: #F5F5F5; color: #A52A2A; }
    QProgressBar::chunk { background-color: #CD5C5C; }
    QCheckBox { color: #F5F5F5; }
    QTextEdit#consoleOutput { background-color: #A52A2A; color: #F5F5F5; border: 1px solid #DC143C; padding: 5px; }
    QDialog { background-color: #B22222; color: #F5F5F5; }
    QDialog QPushButton { background-color: #B22222; color: white; border-radius: 5px; padding: 5px 10px; }
    QDialog QPushButton:hover { background-color: #A52A2A; }
"""

STYLE_NEON_FUTURE = """
    QMainWindow { background-color: #0F0F0F; color: #00FFC2; }
    QLabel { color: #00FFC2; }
    QGroupBox { border: 2px solid #FF00E5; border-radius: 8px; margin-top: 1ex; font-weight: bold; color: #FF00E5; font-size: 14px; }
    QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 8px; background-color: #323232; border-radius: 5px; }
    QPushButton { background-color: #00FFC2; color: #0F0F0F; border-radius: 5px; padding: 10px 20px; font-weight: bold; font-size: 13px; border: 1px solid #00E0A0; }
    QPushButton:hover { background-color: #FF00E5; color: #0F0F0F; }
    QLineEdit, QSpinBox, QComboBox, QListWidget { background-color: #242424; color: #00FFC2; border: 1px solid #00FFC2; border-radius: 4px; padding: 4px; font-size: 13px; }
    QStatusBar { background-color: #323232; color: #00FFC2; border-top: 1px solid #FF00E5; padding: 5px; font-size: 12px; }
    QProgressBar { border: 1px solid #00FFC2; background-color: #242424; color: #00FFC2; }
    QProgressBar::chunk { background-color: #FF00E5; }
    QCheckBox { color: #00FFC2; }
    QTextEdit#consoleOutput { background-color: #0F0F0F; color: #00FFC2; border: 1px solid #FF00E5; padding: 5px; }
    QDialog { background-color: #242424; color: #00FFC2; }
    QDialog QPushButton { background-color: #00FFC2; color: #0F0F0F; border-radius: 5px; padding: 5px 10px; }
    QDialog QPushButton:hover { background-color: #FF00E5; color: #0F0F0F; }
"""

STYLE_TROPICAL_PARADISE = """
    QMainWindow { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #00CED1, stop:1 #7FFFD4); color: #006400; }
    QLabel { color: #006400; }
    QGroupBox { border: 2px solid #20B2AA; border-radius: 8px; margin-top: 1ex; font-weight: bold; color: #48D1CC; font-size: 14px; }
    QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 8px; background-color: #20B2AA; border-radius: 5px; }
    QPushButton { background-color: #48D1CC; color: white; border-radius: 5px; padding: 10px 20px; font-weight: bold; font-size: 13px; border: 1px solid #00CED1; }
    QPushButton:hover { background-color: #00CED1; }
    QLineEdit, QSpinBox, QComboBox, QListWidget { background-color: white; color: #006400; border: 1px solid #48D1CC; border-radius: 4px; padding: 4px; font-size: 13px; }
    QStatusBar { background-color: #20B2AA; color: #006400; border-top: 1px solid #00CED1; padding: 5px; font-size: 12px; }
    QProgressBar { border: 1px solid #48D1CC; background-color: white; color: #006400; }
    QProgressBar::chunk { background-color: #7FFFD4; }
    QCheckBox { color: #006400; }
    QTextEdit#consoleOutput { background-color: white; color: #006400; border: 1px solid #20B2AA; padding: 5px; }
    QDialog { background-color: #7FFFD4; color: #006400; }
    QDialog QPushButton { background-color: #48D1CC; color: white; border-radius: 5px; padding: 5px 10px; }
    QDialog QPushButton:hover { background-color: #00CED1; }
"""

STYLE_WINTER_GLOW = """
    QMainWindow { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #EAEAEA, stop:1 #F5F5F5); color: #212121; }
    QLabel { color: #212121; }
    QGroupBox { border: 2px solid #B0C4DE; border-radius: 8px; margin-top: 1ex; font-weight: bold; color: #778899; font-size: 14px; }
    QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 8px; background-color: #B0C4DE; border-radius: 5px; }
    QPushButton { background-color: #ADD8E6; color: #212121; border-radius: 5px; padding: 10px 20px; font-weight: bold; font-size: 13px; border: 1px solid #B0C4DE; }
    QPushButton:hover { background-color: #B0C4DE; }
    QLineEdit, QSpinBox, QComboBox, QListWidget { background-color: white; color: #212121; border: 1px solid #ADD8E6; border-radius: 4px; padding: 4px; font-size: 13px; }
    QStatusBar { background-color: #B0C4DE; color: #212121; border-top: 1px solid #EAEAEA; padding: 5px; font-size: 12px; }
    QProgressBar { border: 1px solid #ADD8E6; background-color: white; color: #212121; }
    QProgressBar::chunk { background-color: #B0E0E6; }
    QCheckBox { color: #212121; }
    QTextEdit#consoleOutput { background-color: white; color: #212121; border: 1px solid #B0C4DE; padding: 5px; }
    QDialog { background-color: #F5F5F5; color: #212121; }
    QDialog QPushButton { background-color: #ADD8E6; color: #212121; border-radius: 5px; padding: 5px 10px; }
    QDialog QPushButton:hover { background-color: #B0C4DE; }
"""

STYLE_GRUNGE_GRAY = """
    QMainWindow { background-color: #2F4F4F; color: #C0C0C0; }
    QLabel { color: #C0C0C0; }
    QGroupBox { border: 2px solid #5A5A5A; border-radius: 8px; margin-top: 1ex; font-weight: bold; color: #808080; font-size: 14px; }
    QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 8px; background-color: #5A5A5A; border-radius: 5px; }
    QPushButton { background-color: #808080; color: white; border-radius: 5px; padding: 10px 20px; font-weight: bold; font-size: 13px; border: 1px solid #5A5A5A; }
    QPushButton:hover { background-color: #696969; }
    QLineEdit, QSpinBox, QComboBox, QListWidget { background-color: #3C3C3C; color: #C0C0C0; border: 1px solid #808080; border-radius: 4px; padding: 4px; font-size: 13px; }
    QStatusBar { background-color: #5A5A5A; color: #C0C0C0; border-top: 1px solid #2F4F4F; padding: 5px; font-size: 12px; }
    QProgressBar { border: 1px solid #808080; background-color: #3C3C3C; color: #C0C0C0; }
    QProgressBar::chunk { background-color: #A9A9A9; }
    QCheckBox { color: #C0C0C0; }
    QTextEdit#consoleOutput { background-color: #2F4F4F; color: #C0C0C0; border: 1px solid #5A5A5A; padding: 5px; }
    QDialog { background-color: #3C3C3C; color: #C0C0C0; }
    QDialog QPushButton { background-color: #808080; color: white; border-radius: 5px; padding: 5px 10px; }
    QDialog QPushButton:hover { background-color: #696969; }
"""

STYLE_FIREFLY_NIGHT = """
    QMainWindow { background-color: #0A0A0A; color: #ADFF2F; }
    QLabel { color: #ADFF2F; }
    QGroupBox { border: 2px solid #32CD32; border-radius: 8px; margin-top: 1ex; font-weight: bold; color: #00FF7F; font-size: 14px; }
    QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 8px; background-color: #1A1A1A; border-radius: 5px; }
    QPushButton { background-color: #ADFF2F; color: #0A0A0A; border-radius: 5px; padding: 10px 20px; font-weight: bold; font-size: 13px; border: 1px solid #32CD32; }
    QPushButton:hover { background-color: #00FF7F; color: #0A0A0A; }
    QLineEdit, QSpinBox, QComboBox, QListWidget { background-color: #1A1A1A; color: #ADFF2F; border: 1px solid #ADFF2F; border-radius: 4px; padding: 4px; font-size: 13px; }
    QStatusBar { background-color: #32CD32; color: #ADFF2F; border-top: 1px solid #0A0A0A; padding: 5px; font-size: 12px; }
    QProgressBar { border: 1px solid #ADFF2F; background-color: #1A1A1A; color: #ADFF2F; }
    QProgressBar::chunk { background-color: #00FF7F; }
    QCheckBox { color: #ADFF2F; }
    QTextEdit#consoleOutput { background-color: #0A0A0A; color: #ADFF2F; border: 1px solid #32CD32; padding: 5px; }
    QDialog { background-color: #1A1A1A; color: #ADFF2F; }
    QDialog QPushButton { background-color: #ADFF2F; color: #0A0A0A; border-radius: 5px; padding: 5px 10px; }
    QDialog QPushButton:hover { background-color: #00FF7F; color: #0A0A0A; }
"""

STYLE_ROSE_QUARTZ = """
    QMainWindow { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FDDCDC, stop:1 #FFC0CB); color: #C2185B; }
    QLabel { color: #C2185B; }
    QGroupBox { border: 2px solid #E91E63; border-radius: 8px; margin-top: 1ex; font-weight: bold; color: #F8BBD0; font-size: 14px; }
    QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 8px; background-color: #E91E63; border-radius: 5px; }
    QPushButton { background-color: #EC407A; color: white; border-radius: 5px; padding: 10px 20px; font-weight: bold; font-size: 13px; border: 1px solid #C2185B; }
    QPushButton:hover { background-color: #C2185B; }
    QLineEdit, QSpinBox, QComboBox, QListWidget { background-color: white; color: #C2185B; border: 1px solid #EC407A; border-radius: 4px; padding: 4px; font-size: 13px; }
    QStatusBar { background-color: #E91E63; color: #C2185B; border-top: 1px solid #FDDCDC; padding: 5px; font-size: 12px; }
    QProgressBar { border: 1px solid #EC407A; background-color: white; color: #C2185B; }
    QProgressBar::chunk { background-color: #FFB6C1; }
    QCheckBox { color: #C2185B; }
    QTextEdit#consoleOutput { background-color: white; color: #C2185B; border: 1px solid #E91E63; padding: 5px; }
    QDialog { background-color: #FFC0CB; color: #C2185B; }
    QDialog QPushButton { background-color: #EC407A; color: white; border-radius: 5px; padding: 5px 10px; }
    QDialog QPushButton:hover { background-color: #C2185B; }
"""

STYLE_COFFEE_ROAST = """
    QMainWindow { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #6F4E37, stop:1 #8B4513); color: #D2B48C; }
    QLabel { color: #D2B48C; }
    QGroupBox { border: 2px solid #A0522D; border-radius: 8px; margin-top: 1ex; font-weight: bold; color: #D2B48C; font-size: 14px; }
    QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 8px; background-color: #A0522D; border-radius: 5px; }
    QPushButton { background-color: #CD853F; color: white; border-radius: 5px; padding: 10px 20px; font-weight: bold; font-size: 13px; border: 1px solid #A0522D; }
    QPushButton:hover { background-color: #A0522D; }
    QLineEdit, QSpinBox, QComboBox, QListWidget { background-color: #D2B48C; color: #6F4E37; border: 1px solid #CD853F; border-radius: 4px; padding: 4px; font-size: 13px; }
    QStatusBar { background-color: #A0522D; color: #D2B48C; border-top: 1px solid #6F4E37; padding: 5px; font-size: 12px; }
    QProgressBar { border: 1px solid #CD853F; background-color: #D2B48C; color: #6F4E37; }
    QProgressBar::chunk { background-color: #8B4513; }
    QCheckBox { color: #D2B48C; }
    QTextEdit#consoleOutput { background-color: #6F4E37; color: #D2B48C; border: 1px solid #A0522D; padding: 5px; }
    QDialog { background-color: #8B4513; color: #D2B48C; }
    QDialog QPushButton { background-color: #CD853F; color: white; border-radius: 5px; padding: 5px 10px; }
    QDialog QPushButton:hover { background-color: #A0522D; }
"""

STYLE_SILVER_LINING = """
    QMainWindow { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #EBEBEB, stop:1 #DCDCDC); color: #404040; }
    QLabel { color: #404040; }
    QGroupBox { border: 2px solid #A9A9A9; border-radius: 8px; margin-top: 1ex; font-weight: bold; color: #808080; font-size: 14px; }
    QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 8px; background-color: #A9A9A9; border-radius: 5px; }
    QPushButton { background-color: #C0C0C0; color: #404040; border-radius: 5px; padding: 10px 20px; font-weight: bold; font-size: 13px; border: 1px solid #A9A9A9; }
    QPushButton:hover { background-color: #A9A9A9; }
    QLineEdit, QSpinBox, QComboBox, QListWidget { background-color: white; color: #404040; border: 1px solid #C0C0C0; border-radius: 4px; padding: 4px; font-size: 13px; }
    QStatusBar { background-color: #A9A9A9; color: #404040; border-top: 1px solid #EBEBEB; padding: 5px; font-size: 12px; }
    QProgressBar { border: 1px solid #C0C0C0; background-color: white; color: #404040; }
    QProgressBar::chunk { background-color: #B0B0B0; }
    QCheckBox { color: #404040; }
    QTextEdit#consoleOutput { background-color: white; color: #404040; border: 1px solid #A9A9A9; padding: 5px; }
    QDialog { background-color: #DCDCDC; color: #404040; }
    QDialog QPushButton { background-color: #C0C0C0; color: #404040; border-radius: 5px; padding: 5px 10px; }
    QDialog QPushButton:hover { background-color: #A9A9A9; }
"""

THEMES = {
    "Warm Sunset": STYLE_WARM_SUNSET,
    "Cool Ocean": STYLE_COOL_OCEAN,
    "Monochrome Dark": STYLE_MONOCHROME_DARK,
    "Monochrome Light": STYLE_MONOCHROME_LIGHT,
    "Forest Green": STYLE_FOREST_GREEN,
    "Royal Purple": STYLE_ROYAL_PURPLE,
    "Cyberpunk Neon": STYLE_CYBERPUNK_NEON,
    "Pastel Dream": STYLE_PASTEL_DREAM,
    "Vibrant Pop": STYLE_VIBRANT_POP,
    "Industrial Steel": STYLE_INDUSTRIAL_STEEL,
    "Deep Forest": STYLE_DEEP_FOREST,
    "Autumn Harvest": STYLE_AUTUMN_HARVEST,
    "Midnight Sky": STYLE_MIDNIGHT_SKY,
    "Ocean Breeze": STYLE_OCEAN_BREEZE,
    "Grape Crush": STYLE_GRAPE_CRUSH,
    "Sunset Orange": STYLE_SUNSET_ORANGE,
    "Rustic Earth": STYLE_RUSTIC_EARTH,
    "Aquatic Blue": STYLE_AQUATIC_BLUE,
    "Lavender Fields": STYLE_LAVENDER_FIELDS,
    "Emerald City": STYLE_EMERALD_CITY,
    "Fiery Flame": STYLE_FIERY_FLAME,
    "Night Sky": STYLE_NIGHT_SKY,
    "Vintage Sepia": STYLE_VINTAGE_SEPIA,
    "Crimson Tide": STYLE_CRIMSON_TIDE,
    "Minty Fresh": STYLE_MINTY_FRESH,
    "Desert Sand": STYLE_DESERT_SAND,
    "Galaxy Night": STYLE_GALAXY_NIGHT,
    "Morning Dew": STYLE_MORNING_DEW,
    "Volcanic Ash": STYLE_VOLCANIC_ASH,
    "Honey Gold": STYLE_HONEY_GOLD,
    "Arctic Frost": STYLE_ARCTIC_FROST,
    "Crimson Peak": STYLE_CRIMSON_PEAK,
    "Neon Future": STYLE_NEON_FUTURE,
    "Tropical Paradise": STYLE_TROPICAL_PARADISE,
    "Winter Glow": STYLE_WINTER_GLOW,
    "Grunge Gray": STYLE_GRUNGE_GRAY,
    "Firefly Night": STYLE_FIREFLY_NIGHT,
    "Rose Quartz": STYLE_ROSE_QUARTZ,
    "Coffee Roast": STYLE_COFFEE_ROAST,
    "Silver Lining": STYLE_SILVER_LINING
}