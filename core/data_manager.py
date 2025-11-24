import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QLabel, QTabWidget, QPushButton
)
from PySide6.QtCore import Qt

class DataManager:
    def __init__(self):
        self.last_name = ""
        self.last_label = ""

    def save_text(self, name=None, label= None):
        if name is not None : 
            self.last_name = name
        if name is not None :
            self.last_label = label

    def get_text(self):
        return self.last_name, self.last_label
        

