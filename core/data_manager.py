import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QLabel, QTabWidget, QPushButton
)
from PySide6.QtCore import Qt

class DataManager:
    def __init__(self):
        self.last_text = ""

    def save_text(self, text):
        self.last_text = text

    def get_text(self):
        return self.last_text
        

