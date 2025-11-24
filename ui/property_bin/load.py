from PySide6 import QtWidgets, QtGui, QtCore
import core.config as paths
from ui.custom_widgets.custom_widget import Cstm_Widgets

import json

# =========================================================
# Class : Load
# =========================================================

class Load (QtWidgets.QWidget) :

    def __init__(self, soft, data_manager) :
        super().__init__()

        self.soft = soft
        self.data_manager = data_manager
        self.loader()
        self.ui_load()

    def loader (self) :

        with open (f"{paths.JSON_PATH}/nodegraph.json", "r", encoding="utf-8") as f :
            self.nodegraph = json.load(f)

        if self.data_manager.get_text()[0] in self.nodegraph:
            self.folder_path = self.nodegraph[self.data_manager.get_text()[0]]["folder_path"]
        else:
            self.folder_path = ""
            self.node_not_exist()

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

        self.edit_browser = QtWidgets.QLineEdit(self.folder_path)
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

    #def node_exist (self) :
        
        

    def node_not_exist (self) :
    
        fodler_path = {
            "id" : self.data_manager.get_text()[2],
            "folder_path" : ""
        }

        self.nodegraph[self.data_manager.get_text()[0]] = fodler_path

        with open (f"{paths.JSON_PATH}/nodegraph.json", "w", encoding="utf-8") as nodegraph :
            json.dump(self.nodegraph, nodegraph, ensure_ascii=False, indent=4)

    def open_browser_load(self):
        file_dialog = QtWidgets.QFileDialog.getOpenFileName(self,"Select Folder","",self.extention)
        print(">>> Result:", file_dialog) 
        if file_dialog:
            self.edit_browser.setText(file_dialog[0])

        #- write selected path to json nodegraph

        self.nodegraph[self.data_manager.get_text()[0]]["folder_path"] = file_dialog[0]

        with open (f"{paths.JSON_PATH}/nodegraph.json", "w", encoding="utf-8") as nodegraph :
            json.dump(self.nodegraph, nodegraph, ensure_ascii=False, indent=4) 