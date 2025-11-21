from PySide6 import QtWidgets, QtGui, QtCore
import core.config as paths
from ui.custom_widgets.custom_widget import Cstm_Widgets

# =========================================================
# Class : Load
# =========================================================

class Load (QtWidgets.QWidget) :

    def __init__(self, soft) :
        super().__init__()

        self.soft = soft
        self.define_soft()
        self.ui_load()

    def define_soft (self) :

        if self.soft == "maya" :

            self.color = "#4a78d3"
            self.dark_color = "#162064"
            self.hover_color = "#698dd4"
            self.soft_path = paths.ICON_RFM_LOAD
            self.path_folder = paths.RFM_ICON_FOLDER
            self.path_folder_hover = paths.RFM_ICON_FOLDER_HOVER
            self.extention = "*ma *mb"

        else :

            self.color = "#d6582a"
            self.dark_color = "#3F170A"
            self.hover_color = "#ee6736"
            self.soft_path = paths.ICON_RFH_LOAD
            self.path_folder =paths.RFH_ICON_FOLDER
            self.path_folder_hover = paths.RFH_ICON_FOLDER_HOVER
            self.extention = "*usd"

    def ui_load (self) :

        lyt_main = QtWidgets.QVBoxLayout(self)
        lyt_main.setContentsMargins(0, 0, 0, 0)  

        # ============================================================================ Title

        if self.soft == "maya" :
            node_title = "RFM Load"
        else :
            node_title = "RFH Load"

        Cstm_Widgets.default_node_title(lyt_main, node_title, self.soft_path, self.soft)

        # ============================================================================ Loading File

        #- Title size
        Cstm_Widgets.default_node_subtitle(lyt_main, "Loading Scene", self.soft)

        #- Browser 

        lyt_browser = QtWidgets.QHBoxLayout()
        lyt_main.addLayout(lyt_browser)

        self.edit_browser = QtWidgets.QLineEdit()
        self.edit_browser.setMinimumWidth(220)
        self.edit_browser.setFixedHeight(34)
        self.edit_browser.setAlignment(QtGui.Qt.AlignRight)
        self.edit_browser.setStyleSheet(f"""
            QLineEdit {{
                border-radius:2px;
                margin:5px;
                padding-left:2px;
                padding-right:30px;
                background-color:#e4e4e4;
            }}
                QLineEdit::hover {{
                border : 1px solid {self.color};
            }}
        """)
        lyt_browser.addWidget(self.edit_browser)

        btn_open_browser = QtWidgets.QPushButton()
        #btn_open_browser.setFixedSize(20,20)
        btn_open_browser.setStyleSheet(f"""
            QPushButton {{
                border: none;
                icon : url("{self.path_folder}");
                icon-size : 22px;
                margin-right : 10px;
            }}
            QPushButton::hover{{
                icon: url("{self.path_folder_hover}");
            }}
            QPushButton::pressed{{
                margin-top : 2px;
                margin-bottom : -2px;
            }}
        """)
        btn_open_browser.clicked.connect(self.open_browser_load)
        lyt_browser.addWidget(btn_open_browser, alignment=QtGui.Qt.AlignCenter)

        lyt_main.addStretch()

    # ---------------------------------------------------------------- EVENT ----------------------------------------------------------------

    def open_browser_load(self):
        file_dialog = QtWidgets.QFileDialog.getOpenFileName(self,"Select Folder","",self.extention)
        print(">>> Result:", file_dialog) 
        if file_dialog:
            self.edit_browser.setText(file_dialog[0])