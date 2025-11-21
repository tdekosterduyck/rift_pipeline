from PySide6 import QtWidgets, QtGui, QtCore
import sys

import core.config as paths
from ui.custom_widgets.custom_widget import Cstm_Widgets

"""
    A faire (dans l'ordre ):

        - clean le process de layer : 
            
            = ajouter un bouton pour ouvrir la fenetre de renaming 
            = prendre que les load, camera & light de la list d'input 
            = mettre un message d'erreur si aucun layer est selectionne
            = vider le edit quand un layer est ajouter 
            = rendre la fenetre estetique 

"""

# =========================================================
# Class : Load
# =========================================================

class Layer (QtWidgets.QWidget) :

    def __init__(self, soft, node_graph) :
        super().__init__()

        self.soft = soft
        self.node_graph = node_graph
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

        lyt_main = QtWidgets.QVBoxLayout(self)
        lyt_main.setContentsMargins(0, 0, 0, 0)  

        # ============================================================================ Title

        Cstm_Widgets.default_node_title(lyt_main, "Rfm_Layer", self.soft_path, self.soft)

        # ============================================================================ Loading File

        #- Title size
        Cstm_Widgets.default_node_subtitle(lyt_main, "List Asset", self.soft)

        lyt_list = QtWidgets.QVBoxLayout()
        lyt_main.addLayout(lyt_list)

        lbl_list_load = QtWidgets.QLabel("List of all Load node")
        lyt_list.addWidget(lbl_list_load)

        self.list_load = QtWidgets.QListWidget()
        self.show_item_load()
        self.list_load.itemDoubleClicked.connect(self.open_renaming_ui)
        lyt_list.addWidget(self.list_load)

        #- Title size
        Cstm_Widgets.default_node_subtitle(lyt_main, "Layering", self.soft)

        lbl_list_load = QtWidgets.QLabel("List of layers to render")
        lyt_list.addWidget(lbl_list_load)

        self.edit_layer_name = QtWidgets.QLineEdit()
        lyt_list.addWidget(self.edit_layer_name)

        btn_add_layer = QtWidgets.QPushButton("Add Layer")
        btn_add_layer.clicked.connect(self.add_layer_to_list)
        lyt_list.addWidget(btn_add_layer)

        self.tree_layer = QtWidgets.QTreeView()
        lyt_list.addWidget(self.tree_layer)     

        self.header = QtGui.QStandardItemModel()
        self.header.setHorizontalHeaderLabels(["Layers"])
        self.tree_layer.setModel(self.header)


    def ui_layer_houdini (self) :

        pass

    # ========================================================= EVENT ========================================================= 

    def show_item_load (self) :

        list_load = self.node_graph.list_all_node()
        for load in list_load :
            self.list_load.addItem(load)

    def add_layer_to_list (self) :

        self.add_cate = QtGui.QStandardItem(self.edit_layer_name.text())
        self.header.appendRow(self.add_cate)

    def open_renaming_ui (self) :

        # Création de la fenêtre principale directement
        self.wdw = QtWidgets.QMainWindow()
        self.wdw.setWindowTitle("Interface Vide")
        self.wdw.setGeometry(100, 100, 100, 100)  # x, y, width, height

        central_widget = QtWidgets.QWidget()
        self.wdw.setCentralWidget(central_widget)

        # Layout vertical
        lyt_renaming = QtWidgets.QVBoxLayout()
        central_widget.setLayout(lyt_renaming)

        self.edit_name = QtWidgets.QLineEdit()
        lyt_renaming.addWidget(self.edit_name)

        btn = QtWidgets.QPushButton("Save Name")
        btn.clicked.connect(self.add_item_to_list_layer)
        lyt_renaming.addWidget(btn)
        
        self.wdw.show()

    def add_item_to_list_layer (self) :

        layer_name = self.edit_name.text()
        layer_selected = self.tree_layer.selectedIndexes()
        print(layer_selected)
        parent_index = layer_selected[0]       
        parent_item = self.header.itemFromIndex(parent_index)
        #print(layer_selected)

        sub_item = QtGui.QStandardItem(layer_name)
        parent_item.appendRow(sub_item)

        self.tree_layer.expand(parent_index)

        #self.tree_layer.addItem(layer_name)
        #self.wdw.close()