import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QLabel, QTabWidget, QPushButton
)
from PySide6.QtCore import Qt

from ui.main_window import Rift
from core.data_manager import DataManager

if __name__ == "__main__":
    app = QApplication(sys.argv)
    data_manager = DataManager()
    window = Rift(data_manager)
    window.show()
    sys.exit(app.exec())