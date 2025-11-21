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

    def define_soft (self) :

        if self.soft == "maya" :

            self.color = "#4a78d3"
            self.dark_color = "#162064"
            self.hover_color = "#698dd4"
            self.soft_path = paths.ICON_RFM_LOAD
            self.path_folder = paths.RFM_ICON_FOLDER
            self.path_folder_hover = paths.RFM_ICON_FOLDER_HOVER
            self.ui_layer_maya()

        else :

            self.color = "#d6582a"
            self.dark_color = "#3F170A"
            self.hover_color = "#ee6736"
            self.soft_path = paths.ICON_RFH_LOAD
            self.path_folder =paths.RFH_ICON_FOLDER
            self.path_folder_hover = paths.RFH_ICON_FOLDER_HOVER
            self.ui_layer_houdini()

    def ui_layer_maya (self) :

        pass

    def ui_layer_houdini (self) :

        pass