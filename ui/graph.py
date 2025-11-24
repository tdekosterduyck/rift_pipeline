# =============================================================
# Nom du fichier :    main_graph.py
# Auteur :            Thomas Dekoster-Duyck
# Contact             dkthomas.pro@gmail.com
# Date de création :  22/09/2025
# Description :       Main Graph UI
# Version :           1.1
# Python :            3.12+
# =============================================================

"""
TO DO :

- Create my own propertyBin
- Modify load, import and save session to adapt to a real pipe

CHANGELOG :

1.1 : graph creation and adding my own nodes
1.2 : add context menu

SUMMARY

line 00 : .....

"""

from Qt import QtWidgets
from Qt import QtWidgets, QtGui, QtCore 
from NodeGraphQt import NodeGraph, BaseNode, NodeBaseWidget
from NodeGraphQt import NodeGraph, PropertiesBinWidget, constants

import os
import sys
import json

#from ui.main_window import Rift
from core.utils.rfm_nodes import * 
from core.utils.rfh_nodes import *
import core.config as paths


# =========================================================
# Class : Hotkeys
# =========================================================

class hotkeys () :

    """
        All hotkeys in the graph   
    """

    def __init__(self, graph):
        self.graph = graph

    # ---------- Browsing / UI ---------- #

    def open_node_search(self):

        self.graph.toggle_node_search()

    def duplicate_node (self) :
        
        self.graph.selected_nodes()
        self.graph.copy_nodes()
        self.graph.paste_nodes()

    def clear (self) :

        self.graph.clear_session()

    def delete_selected_nodes(self):
        
        selected = self.graph.selected_nodes()
        print(selected)
        print(selected[0].name())

        with open (f"{paths.JSON_PATH}/nodegraph.json", "r", encoding="utf-8") as f :
            self.nodegraph = json.load(f)

        for node in selected :
            del self.nodegraph[node.name()]

        with open (f"{paths.JSON_PATH}/nodegraph.json", "w", encoding="utf-8") as nodegraph :
            json.dump(self.nodegraph, nodegraph, ensure_ascii=False, indent=4) 

        if selected:
            self.graph.delete_nodes(selected)

    def fit_zoom (self) :

        self.graph.fit_to_selection()
    
    def layout_dir (self) :

        lyt_dir = self.graph.layout_direction()

        if lyt_dir == 0 : 
            self.graph.set_layout_direction(1)

        else : 
            self.graph.set_layout_direction(0)

    def pipe_layout (self) : 

        pipe_style = self.graph.pipe_style()
        
        if pipe_style == 2 : 
            self.graph.set_pipe_style(0)
        if pipe_style == 0 : 
            self.graph.set_pipe_style(1)
        if pipe_style == 1 : 
            self.graph.set_pipe_style(2)

    def maximise(self):
        window = self.graph.widget.window()
        if window.isFullScreen():
            window.showNormal()
        else:
            window.showFullScreen()

    # ---------- Creating Nodes ---------- #

    def rfm_load(self):

        self.graph.create_node('IMPORT.Rfm_Load', name='Rfm Load', pos=[300, 300])
    
    def rfh_load(self):

        self.graph.create_node('IMPORT.Rfh_Load', name='Rfh Load', pos=[300, 300])

    def merge(self):

        self.graph.create_node('MERGE.Rfm_Merge', name='Rfm Merge', pos=[300, 300])
    
    def rfm_camera(self):

        self.graph.create_node('IMPORT.Rfm_Camera', name='Rfm Camera', pos=[300, 300])

    def rfh_camera(self):

        self.graph.create_node('IMPORT.Rfh_Camera', name='Rfh Camera', pos=[300, 300])

    def rfm_render(self):

        self.graph.create_node('RENDER.Rfm_Render', name='Rfm Render', pos=[300, 300])

    def rfh_render(self):

        self.graph.create_node('RENDER.Rfh_Render', name='Rfh Render', pos=[300, 300])

    # ---------- Management ---------- #

    def find_json_path (self) :

        script_path = os.path.abspath(__file__)
        script_path.split("Farm")[0]

    def save_graph (self) :

        self.graph.save_session(paths.SAVE_PATH)

        print("#-------# Scene graph has been saved #-------#")

    def load_graph (self) :

        load_file_dialog = QtWidgets.QFileDialog.getOpenFileName(parent=None,caption="Load Graph",dir=paths.LOAD_PATH, filter="Json Files (*.json)")[0]
        self.graph.load_session(load_file_dialog)

    def import_graph (self) :

        import_file_dialog = QtWidgets.QFileDialog.getOpenFileName(parent=None,caption="Import Graph",dir=paths.BASE_PATH, filter="Json Files (*.json)")[0]
        self.graph.load_session(import_file_dialog)

    def quit_graph () :

        app.quit()
        sys.exit()


# =========================================================
# Class : Node_Graph
# =========================================================

class Node_Graph(QtWidgets.QMainWindow):

    def __init__(self, parent=None, data_manager=None):
        super().__init__(parent)
        self.farm = parent
        self.data_manager = data_manager

        self.ui_graph()

    # ---------------------------------------------------------------- GRAPH ----------------------------------------------------------------

    def ui_graph (self) :
    
        self.setWindowTitle("Node Graph")
        self.resize(2000, 2000)

        # --- Init Qt Graph --- #
        self.graph = NodeGraph()
        self.graph_widget = self.graph.widget
        self.graph.set_layout_direction(1)  
        self.graph.set_pipe_collision(True)    
        self.graph.set_pipe_slicing(True) 
        
        self.hotkeys = hotkeys(self.graph)

        # ----- # Register Nodes # ----- #

        self.graph.register_nodes([Rfm_Load, Rfm_Camera, Rfm_Merge, Rfm_Aovs, Rfm_Layers,Rfm_Cryptos, Rfm_Render])
        self.graph.register_nodes([Rfh_Load, Rfh_Camera, Rfh_Merge, Rfh_Aovs, Rfh_Layers,Rfh_Cryptos, Rfh_Render])

        self.main_layout = QtWidgets.QHBoxLayout()

        self.central_widget = QtWidgets.QWidget()
        self.central_lyt = QtWidgets.QHBoxLayout(self.central_widget)
        self.central_widget.setLayout(self.central_lyt)
        self.central_lyt.addWidget(self.graph_widget)

        # ----- # Signal # ----- #

        self.graph.node_double_clicked.connect(self.double_clicked)
        self.graph.property_changed.connect(self.property_changed)
        self.graph.node_created.connect(self.create_json_info)

        # ----- # Context Menu # ----- #

        self.setCentralWidget(self.central_widget)

        self.context_menu = self.graph.get_context_menu('graph')

        # Menu général
        self.context_menu.add_command('Search Nodes', self.hotkeys.open_node_search, shortcut='Tab')

        # Fichier
        self.file_menu = self.context_menu.add_menu("File")
        self.file_menu.add_command('New', self.hotkeys.clear, shortcut='CTRL+N')
        self.file_menu.add_separator()
        self.file_menu.add_command('Save', self.hotkeys.save_graph, shortcut='CTRL+S')
        self.file_menu.add_command('Load', self.hotkeys.load_graph, shortcut='CTRL+L')
        self.file_menu.add_command('Import', self.hotkeys.load_graph, shortcut='CTRL+I')
        self.file_menu.add_separator()
        self.file_menu.add_command('Quit', self.hotkeys.quit_graph, shortcut='CTRL+Q')

        # Édition
        self.edit_menu = self.context_menu.add_menu("Edit")
        self.edit_menu.add_command('Delete Node', self.hotkeys.delete_selected_nodes, shortcut='Delete')
        self.edit_menu.add_command('Duplicate', self.hotkeys.duplicate_node, shortcut='CTRL+D')
        self.edit_menu.add_command('Fit', self.hotkeys.fit_zoom, shortcut='F')
        self.edit_menu.add_command('Direction', self.hotkeys.layout_dir, shortcut='CTRL+ALT+L')
        self.edit_menu.add_command('Pipe Layout', self.hotkeys.pipe_layout, shortcut='CTRL+Y')
        self.edit_menu.add_command('Maximise', self.hotkeys.maximise, shortcut='F11')

        # Raccourcis clavier
        self.hotkeys_menu = self.context_menu.add_menu("HotKeys")
        self.hotkeys_menu.add_command('Rfm Load', self.hotkeys.rfm_load, shortcut='L')
        self.hotkeys_menu.add_command('Rfh Load', self.hotkeys.rfh_load, shortcut='SHIFT+L')
        self.hotkeys_menu.add_command('Merge', self.hotkeys.merge, shortcut='M')
        self.hotkeys_menu.add_command('Rfm Camera', self.hotkeys.rfm_camera, shortcut='C')
        self.hotkeys_menu.add_command('Rfh Camera', self.hotkeys.rfh_camera, shortcut='SHIFT + C')
        self.hotkeys_menu.add_command('Rfm Render', self.hotkeys.rfm_render, shortcut='R')
        self.hotkeys_menu.add_command('Rfh Render', self.hotkeys.rfh_render, shortcut='SHIFT+R')

    # ---------------------------------------------------------------- EVENT ----------------------------------------------------------------

    def create_json_info (self, node) :
        """
            Signal when node is created
                - creating json infos
        """
        node_name = node.name()
        node_label = node.get_property("label")

        self.data_manager.save_text(node_name, node_label)

        with open (f"{paths.JSON_PATH}/nodegraph.json", "r", encoding="utf-8") as f :
            self.nodegraph = json.load(f)
        json_node_name = self.nodegraph.values()
        
        list_id = []
        for value in json_node_name :

            node_id = value.get("id")

            if node_id is None :
                list_id.append(0)
            else :
                list_id.append(int(node_id))

        create_id = list_id[-1] + 1 

        folder_path = {
            "id" : create_id,
        }

        self.nodegraph[node.name()] = folder_path

        with open (f"{paths.JSON_PATH}/nodegraph.json", "w", encoding="utf-8") as nodegraph :
            json.dump(self.nodegraph, nodegraph, ensure_ascii=False, indent=4) 

    def double_clicked (self, node) :
        """
            Signal when a node is double clicked 
                - add info for property bin
        """

        node_name = node.name()

        node_label = node.get_property("label")

        ppb_node_label = f"ppb_{node_label}"

        self.data_manager.save_text(node_name, node_label)

        self.farm.add_property(ppb_node_label, node) 

    def list_all_node (self) :
        """
            Used for list load node for layer node ui
        """

        list_all_nodes = self.graph.all_nodes()
        nodes_name = []
        for nodes in list_all_nodes :

            node_name = nodes.name()
            nodes_name.append(node_name)

        return nodes_name

    def property_changed (self, node) :
        """
            Signal when a node is renamed 
                - update json nodegraph file
        """

        with open (f"{paths.JSON_PATH}/nodegraph.json", "r", encoding="utf-8") as f :
            self.nodegraph = json.load(f)

        target_node_id = self.nodegraph[self.data_manager.get_text()[0] ]["id"]

        new_name = node.get_property("name")

        for key, value in self.nodegraph.items() :

            if value.get("id") == target_node_id:

                self.nodegraph[new_name] = self.nodegraph.pop(key)
                break

        with open (f"{paths.JSON_PATH}/nodegraph.json", "w", encoding="utf-8") as nodegraph :
            json.dump(self.nodegraph, nodegraph, ensure_ascii=False, indent=4) 

        #- Update data_manager file    
        self.data_manager.save_text(new_name)

