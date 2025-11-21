# =============================================================
# Nom du fichier :    training_06.py
# Auteur :            Thomas Dekoster-Duyck
# Contact             dkthomas.pro@gmail.com
# Date de création :  22/09/2025
# Description :       Main Graph UI
# Version :           2.1
# Python :            3.12+
# =============================================================

"""

#== TITLE ==
#-- SubTitle --
#--# Group #--#
#- Indications
#: explications

CHANGELOG :

1.1 : graph creation and adding my own nodes
1.2 : add context menu
2.1 : total graphic refont 
3.1 : refont property bin + add relative path
4.1 : re organisation of files et folders of my soft

SUMMARY

line 00 : .....

"""

import sys
import os
import json
from pathlib import Path

from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import QSize
from NodeGraphQt import NodeGraph, BaseNode

from ui.graph import *
from core.utils.property_bin import Ppb_Widget
import core.config as paths
from ui.custom_widgets.custom_widget import Cstm_Widgets

from PySide6 import QtWidgets, QtCore, QtGui

# ========================================================= GLOBAL ========================================================= 

class Rift (QtWidgets.QMainWindow):

    def __init__(self, data_manager):
        super(Rift, self).__init__()
        self.data_manager = data_manager
        self.graph_dock = None 
        self.node_graph = Node_Graph(parent=self, data_manager=self.data_manager)

        self.setup_ui()
    
    def setup_ui(self):
        
        self.setWindowTitle("Rift")
        self.setMinimumSize(1000, 600)
        self.setStyleSheet("QMainWindow {background-color : #191919;}")

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        self.lyt_main = QtWidgets.QHBoxLayout(central_widget)

        # ---------------------------------------------------------------- SIDE BAR ----------------------------------------------------------------

        self.grp_side_bar = QtWidgets.QWidget()
        self.grp_side_bar.setFixedWidth(175)
        self.grp_side_bar.setObjectName("grp_side_bar")
        self.grp_side_bar.setStyleSheet("""
            #grp_side_bar {
                background-color: #0f0f0f; 
                border-radius: 6px; 
                
            }
            #grp_side_bar::hover {
                border: 1px solid #444;
            }
            """)
        self.lyt_main.addWidget(self.grp_side_bar)

        #- Layout

        self.lyt_side_bar = QtWidgets.QVBoxLayout(self.grp_side_bar)

        #- Widget

        self.lyt_sidebar_title = QtWidgets.QHBoxLayout()
        self.lyt_side_bar.addLayout(self.lyt_sidebar_title)

        self.lbl_icon_title = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap(paths.ICON_LOGO)
        self.lbl_icon_title.setPixmap(pixmap)
        self.lbl_icon_title.setPixmap(pixmap.scaled(32,32))

        self.lyt_sidebar_title.addWidget(self.lbl_icon_title)

        self.lbl_title_side_bar = QtWidgets.QLabel("RIFT")
        self.lbl_title_side_bar.setStyleSheet(f"""
            QLabel{{
                color: #ffffff;
                font-size : 18px;   
                letter-spacing : 2px; 
                border : none;
                text-align : left;                          
            }}                      
        """)
        self.lyt_sidebar_title.addWidget(self.lbl_title_side_bar, alignment= QtCore.Qt.AlignLeft)

        self.lyt_sidebar_title.addStretch()

        #- Separator

        self.sprt_sidebar = QtWidgets.QFrame()
        self.sprt_sidebar.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.sprt_sidebar.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.sprt_sidebar.setStyleSheet("QFrame {color : #ffffff ;min-height : 1px; max-height : 1px;}")
        self.lyt_side_bar.addWidget(self.sprt_sidebar)

        #- Label Menu

        self.lbl_menu_sidebar = QtWidgets.QLabel("Menu")
        self.lbl_menu_sidebar.setStyleSheet("color : #646464;")
        self.lyt_side_bar.addWidget(self.lbl_menu_sidebar)

        #- Button Top

        self.btn_home = Cstm_Widgets.title_sidebar_style("Home",self.lyt_side_bar, paths.ICON_HOME , "#646464")
        self.btn_render_graph = Cstm_Widgets.title_sidebar_style("Render Graph",self.lyt_side_bar, paths.ICON_GRAPH,"#646464")
        self.btn_farm = Cstm_Widgets.title_sidebar_style("Farm",self.lyt_side_bar, paths.ICON_FARM, "#646464")

        #- Button Bottom

        self.lbl_menu_sidebar = QtWidgets.QLabel("Other")
        self.lbl_menu_sidebar.setStyleSheet("color : #646464;")
        self.lyt_side_bar.addWidget(self.lbl_menu_sidebar)       

        self.btn_help = Cstm_Widgets.title_sidebar_style("Help",self.lyt_side_bar, paths.ICON_SETTINGS, "#646464")
        self.btn_exit = Cstm_Widgets.title_sidebar_style("Exit",self.lyt_side_bar, paths.ICON_EXIT, "#be2c2c")
        

        self.btn_home.clicked.connect(self.home_open)
        self.btn_render_graph.clicked.connect(self.graph_open)
        self.btn_farm.clicked.connect(self.farm_open)
        self.btn_exit.clicked.connect(self.close)

        self.lyt_side_bar.addStretch()     

        # ---------------------------------------------------------------- PAGES ----------------------------------------------------------------

        self.pages = QtWidgets.QStackedWidget()

        #- Page Home
        self.page_home = QtWidgets.QWidget()
        self.lyt_home = QtWidgets.QVBoxLayout(self.page_home)
  
        #- Page Graph
        self.page_graph = QtWidgets.QWidget()
        self.page_graph.setFixedWidth(240)
        self.layout_graph = QtWidgets.QHBoxLayout(self.page_graph)

        #- Page Farm
        page_farm = QtWidgets.QWidget()
        layout_farm = QtWidgets.QVBoxLayout(page_farm)
        layout_farm.addWidget(QtWidgets.QLabel("Page Farm"))

        self.pages.addWidget(self.page_home)    # Index 0
        self.pages.addWidget(self.page_graph)   # Index 1
        self.pages.addWidget(page_farm)   # Index 2

        self.pages.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)

        self.lyt_main.addWidget(self.pages)

        # ---------------------------------------------------------------- HOME ----------------------------------------------------------------

        self.stckd_workspace = QtWidgets.QStackedWidget()

        #- Choose Workspace
        self.grp_workspace = QtWidgets.QWidget()
        self.grp_workspace.setObjectName("grp_home")
        self.grp_workspace.setStyleSheet(f"""
        #grp_home {{
            font-weight: bold;
            border-radius: 6px;
            border-image: url("{paths.ICON_BG}") 0 0 0 0 stretch stretch;                               
        }}""")
        self.lyt_workspace = QtWidgets.QVBoxLayout(self.grp_workspace)
  
        #- Create Workspace
        self.grp_create_workspace = QtWidgets.QWidget()
        self.lyt_create_workspace = QtWidgets.QVBoxLayout(self.grp_create_workspace)
        self.lyt_create_workspace.setContentsMargins(0,0,0,0)

        #- Set Workspace
        self.grp_set_workspace = QtWidgets.QWidget()
        self.lyt_set_workspace = QtWidgets.QVBoxLayout(self.grp_set_workspace)

        self.stckd_workspace.addWidget(self.grp_workspace)    # Index 0
        self.stckd_workspace.addWidget(self.grp_create_workspace)   # Index 1
        self.stckd_workspace.addWidget(self.grp_set_workspace)   # Index 2

        self.lyt_home.addWidget(self.stckd_workspace)

        #-----# Layout #-----#

        self.lyt_top_home = QtWidgets.QHBoxLayout()
        self.lyt_workspace.addLayout(self.lyt_top_home)
        self.lyt_explain_pipe = QtWidgets.QVBoxLayout()
        self.lyt_workspace.addLayout(self.lyt_explain_pipe)
        self.lyt_workspace.addStretch(1)
        self.lyt_mid_home = QtWidgets.QHBoxLayout()
        self.lyt_workspace.addLayout(self.lyt_mid_home)
        self.lyt_workspace.addStretch(2)
        self.lyt_bottom_home = QtWidgets.QVBoxLayout()
        self.lyt_workspace.addLayout(self.lyt_bottom_home)

        #-----# Widget #-----#

        #- Welcome / Explain 

        self.lbl_welcome = QtWidgets.QLabel("Welcome")
        self.lbl_welcome.setStyleSheet("""
            QLabel {
                font-size:30px; 
                font:bold;
                padding-top:10px;
                padding-left:10px;
                color:#ffffff; 
        } """)
        self.lyt_top_home.addWidget(self.lbl_welcome, alignment=QtCore.Qt.AlignLeft)
        
        self.lbl_welcome_to = QtWidgets.QLabel("to")
        self.lbl_welcome_to.setStyleSheet(" font-size: 18px; font:bold; padding-top:19px; color: #ffffff; ")
        self.lyt_top_home.addWidget(self.lbl_welcome_to, alignment=QtCore.Qt.AlignLeft)

        self.lbl_welcome_title = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap(paths.ICON_TITLE)
        self.lbl_welcome_title.setStyleSheet(" padding-top:25px;")
        self.lbl_welcome_title.setPixmap(pixmap)
        self.lbl_welcome_title.setPixmap(pixmap.scaled(175,50))
        self.lyt_top_home.addWidget(self.lbl_welcome_title, alignment=QtCore.Qt.AlignLeft)

        self.lyt_top_home.addStretch() 

        self.lbl_explain_pipe = QtWidgets.QLabel("Cum saepe multa, tum memini domi in hemicyclio sedentem, ut solebat, \ncum et ego essem una et pauci admodum familiares, in eum sermonem illum\nincidere qui tum  forte multis erat in ore. Meministi enim profecto")
        self.lbl_explain_pipe.setStyleSheet("""
            QLabel { 
                font : italic; 
                font-size : 12px;
                padding-top : 8px;
                padding-left : 18px;
                color : #646464;   
        } """)
        self.lyt_explain_pipe.addWidget(self.lbl_explain_pipe, alignment=QtCore.Qt.AlignLeft)
        
        #- Button

        self.lyt_mid_home.addStretch()
        self.btn_create_workspace = Cstm_Widgets.title_sidebar_style("Create Workspace",self.lyt_mid_home, paths.ICON_CREATE_WP , "#7C0F73")
        self.btn_create_workspace.setFixedSize(200,40)
        self.btn_create_workspace.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
        self.btn_create_workspace.clicked.connect(self.idx_create_workspace)

        self.btn_set_workspace = Cstm_Widgets.title_sidebar_style("Set Workspace",self.lyt_mid_home, paths.ICON_HOME , "#7C0F73")
        #self.btn_set_workspace.setEnabled(False)
        self.btn_create_workspace.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
        self.btn_set_workspace.setFixedSize(200,40)
        self.btn_set_workspace.clicked.connect(self.idx_set_workspace)
        #self.lyt_mid_home.addWidget(self.btn_set_workspace, QtCore.Qt.AlignCenter)
        self.lyt_mid_home.addStretch()

        #- Author

        self.lbl_author_contact = QtWidgets.QLabel("Author")
        self.lbl_author_contact.setStyleSheet("QLabel {font-size:13px;color:#7C0F73; font:bold ; } ")
        self.lyt_bottom_home.addWidget(self.lbl_author_contact, alignment=QtCore.Qt.AlignRight)

        self.lbl_author_name = QtWidgets.QLabel("Thomas Dekoster-Duyck")
        self.lbl_author_name.setStyleSheet("QLabel {font-size:10px;color:#ffffff; } QLabel::hover {color : #4b76ce} ")
        self.lyt_bottom_home.addWidget(self.lbl_author_name, alignment=QtCore.Qt.AlignRight)

        self.lbl_author_mail = QtWidgets.QLabel("dkthomas.pro@gmail.com")
        self.lbl_author_mail.setStyleSheet("QLabel {font-size:10px;color:#ffffff; } QLabel::hover {color : #4b76ce}")
        self.lyt_bottom_home.addWidget(self.lbl_author_mail, alignment=QtCore.Qt.AlignRight)

        # ---------- # CREATE WORKSPACE # ----------- #

        self.grp_form_wksp = QtWidgets.QWidget()
        self.grp_form_wksp.setObjectName("grp_form_workspace_shot")
        self.grp_form_wksp.setStyleSheet(f"""
        #grp_form_workspace_shot {{
            font-weight: bold;
            border-image: url("{paths.ICON_BG}") 0 0 0 0 stretch stretch;
            border-radius: 6px;
        }}""")

        self.lyt_create_workspace.addWidget(self.grp_form_wksp)

        self.lyt_workspace_in = QtWidgets.QVBoxLayout()
        self.grp_form_wksp.setLayout(self.lyt_workspace_in)

        self.lbl_title_workspace = QtWidgets.QLabel("Workspace Creation")
        self.lbl_title_workspace.setStyleSheet("""
            QLabel{
                font-size:18px;
                font:bold;
                color:#ffffff;
                margin-top:5px;
                margin-left:5px;
            }
        """)
        self.lyt_workspace_in.addWidget(self.lbl_title_workspace, alignment=QtCore.Qt.AlignLeft)

        self.lyt_form_wksp = QtWidgets.QFormLayout()
        self.lyt_form_wksp.setLabelAlignment(QtCore.Qt.AlignRight)
        self.lyt_workspace_in.addLayout(self.lyt_form_wksp)

        #-----# Widget #-----#

        #- Project Name

        self.lbl_project_name = QtWidgets.QLabel("Project Name")
        self.lbl_project_name.setStyleSheet("color: #ffffff; margin-top : 25px; margin-left : 25px;")

        self.edit_project_name = QtWidgets.QLineEdit(placeholderText="Default")
        self.edit_project_name.setStyleSheet("""
            QLineEdit {
                margin-top : 25px; 
                margin-right : 25px;
                border-radius : 2px; 
                border : 1px solid #c8c8c8;
            }
            QLineEdit::hover {
                border : 1px solid #7a7a7a;                            
            }
            QLineEdit::focus {
                border : 1px solid #c126c6;                            
            }
            """)

        self.lyt_form_wksp.addRow(self.lbl_project_name , self.edit_project_name)

        #- Location

        self.lbl_location = QtWidgets.QLabel("Location")
        self.lbl_location.setStyleSheet("color: #ffffff;margin-left : 25px;")

        self.lyt_location = QtWidgets.QHBoxLayout()

        self.edit_location = QtWidgets.QLineEdit(placeholderText="E:/Folder/")
        self.edit_location.setStyleSheet("""
            QLineEdit {
                border-radius : 2px; 
                border : 1px solid #c8c8c8;
            }
            QLineEdit::hover {
                border : 1px solid #7a7a7a;                            
            }
            QLineEdit::focus {
                border : 1px solid #c126c6;                            
            }
            """)
        self.lyt_location.addWidget(self.edit_location)

        self.btn_folder_location = QtWidgets.QPushButton()
        self.btn_folder_location.setFixedSize(50,24)

        self.btn_folder_location.setStyleSheet(f"""
            QPushButton {{
                border: none;
                icon : url({paths.RFM_ICON_FOLDER});
                icon-size : 26px;
                margin-right : 25px;
            }}
            QPushButton::hover{{
                icon: url({paths.RFM_ICON_FOLDER_HOVER});
            }}
            QPushButton::pressed{{
                margin-top : 2px;
                margin-bottom : -2px;
            }}
        """)
        self.btn_folder_location.clicked.connect(self.open_browser)


        self.lyt_location.addWidget(self.btn_folder_location)
        
        self.lyt_form_wksp.addRow(self.lbl_location , self.lyt_location)

        #- Separator

        self.sprt_wksp = QtWidgets.QFrame()
        self.sprt_wksp.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.sprt_wksp.setStyleSheet("margin-right : 25px;color:#ffffff;")
        self.sprt_wksp.setLineWidth(2)

        self.lyt_form_wksp.addWidget(self.sprt_wksp)
        
        #- In

        self.edit_in = Cstm_Widgets.default_form_style(self.lyt_form_wksp, "In","in", "in")

        #- Out

        self.edit_out = Cstm_Widgets.default_form_style(self.lyt_form_wksp, "Out","out", "out")

        #- Scenes

        self.edit_scenes = Cstm_Widgets.default_form_style(self.lyt_form_wksp, "Scenes","scenes", "scenes")

        #- Out Render

        self.edit_out_render = Cstm_Widgets.default_form_style(self.lyt_form_wksp, "Out_ ender","out_render", "out_render")

        #- Ressources

        self.edit_resources = Cstm_Widgets.default_form_style(self.lyt_form_wksp, "Ressources","ressources", "ressources")

        #- Data

        self.lbl_data = QtWidgets.QLabel("Data")
        self.lbl_data.setStyleSheet("color: #ffffff;margin-left : 25px;")       

        self.edit_data = QtWidgets.QLineEdit("Data")
        self.edit_data.setStyleSheet("""
            QLineEdit {
                margin-right : 25px;
                border-radius : 2px; 
                border : 1px solid #c8c8c8;
            }
        """)
        self.edit_data.setEnabled(False)

        self.lyt_form_wksp.addRow(self.lbl_data , self.edit_data)

        #- Button 

        self.lyt_btn_workspace = QtWidgets.QHBoxLayout()
        self.lyt_btn_workspace.setContentsMargins(109,20,25,0)
        self.lyt_workspace_in.addLayout(self.lyt_btn_workspace)

        self.btn_return_home = Cstm_Widgets.title_sidebar_style("Return",self.lyt_btn_workspace, paths.ICON_RETURN , "#D41B1B")
        self.btn_return_home.setFixedHeight(30)
        self.btn_return_home.clicked.connect(self.home_open)

        self.btn_create_workspace = Cstm_Widgets.title_sidebar_style("Create",self.lyt_btn_workspace, paths.ICON_CREATE_WP , "#c126c6")
        self.btn_create_workspace.setFixedHeight(30)
        self.btn_create_workspace.clicked.connect(self.create_workspace)

        #- Informative Sentence

        self.lyt_workspace_state = QtWidgets.QHBoxLayout()
        self.lyt_workspace_in.addLayout(self.lyt_workspace_state)

        self.lbl_workspace_state = QtWidgets.QLabel("")
        self.lbl_workspace_state.setStyleSheet("font-size:16px;")
        self.lyt_workspace_state.addWidget(self.lbl_workspace_state, alignment=QtCore.Qt.AlignCenter)

        #- Stretch

        self.lyt_workspace_in.addStretch()

        # ---------- # SET WORKSPACE # ----------- #

        self.lbl_coucou = QtWidgets.QLabel("Coucou")
        self.lyt_set_workspace.addWidget(self.lbl_coucou)

        # ---------------------------------------------------------------- GRAPH ----------------------------------------------------------------

        self.tab_property_bin = QtWidgets.QTabWidget(self.page_graph)
        self.tab_property_bin.setStyleSheet("""
            QTabWidget {
                background: #2b2b2b;
            }
            QTabWidget::pane {
                background: #0f0f0f;                      
                border-top-right-radius: 4px;         
                border-bottom-right-radius: 4px;  
                border-bottom-left-radius: 4px;               
            }
            QTabWidget::pane:hover {
                border: 1px solid #444;                    
            }
            QTabBar::tab {
                background : transparent;
                color: #ffffff;
                padding: 8px 16px;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                font : bold;
            }
            QTabBar::tab:selected {
                background: #646464;
                color: #fff;
            }
            QTabBar::tab:hover {
                background: #505050;
                border: 1px solid #606060;
            }
            QTabBar::tab:!selected {
                margin-top: 2px;
            }
        """)

        self.layout_graph.addWidget(self.tab_property_bin)
        self.layout_graph.setContentsMargins(0,0,0,0)
        
        # Onglet 1
        self.tab_settings = QWidget()
        self.lyt_ppb_settings = QVBoxLayout(self.tab_settings)
        self.tab_property_bin.addTab(self.tab_settings, "Settings")

        # Onglet 2
        self.tab_infos = QWidget()
        self.lyt_ppb_infos = QVBoxLayout(self.tab_infos)
        self.tab_property_bin.addTab(self.tab_infos, "Infos")

        #self.lyt_properties_bin.addStretch(1)

        # ---------- # FARM # ----------- #

    # ---------------------------------------------------------------- EVENT ----------------------------------------------------------------

    def graph_open(self):
        self.pages.setCurrentIndex(1)
        if self.graph_dock is not None:
            self.graph_dock.show()
            self.graph_dock.raise_()
            return

        #self.node_graph = Node_Graph(parent=self, data_manager=self.data_manager)

        self.graph_dock = QtWidgets.QDockWidget("Render Graph", self)
        self.graph_dock.setWidget(self.node_graph)
        self.graph_dock.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)
        self.graph_dock.topLevelChanged.connect(self.on_dock_state_changed)
        self.graph_dock.setFloating(False) 
        if not self.graph_dock.isFloating():
            self.set_dock_max_size()

        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.graph_dock)

    def on_dock_state_changed(self, floating):
        if floating:
            self.graph_dock.setMaximumSize(
                QWidget().maximumSize()
            )
        else:
            self.set_dock_max_size()

    def set_dock_max_size(self):
        self.graph_dock.setMaximumWidth(555)

    def home_open (self) : 
    
        if self.graph_dock is not None :
            self.graph_dock.hide()

        self.pages.setCurrentIndex(0)
        self.stckd_workspace.setCurrentIndex(0)

    def farm_open (self) : 
        
        if self.graph_dock is not None :
            self.graph_dock.hide()

        self.pages.setCurrentIndex(2)

    def idx_create_workspace (self) : 

        self.stckd_workspace.setCurrentIndex(1)

    def idx_set_workspace (self) : 

        self.stckd_workspace.setCurrentIndex(2)

    def open_browser (self) : 

        self.file_dialog = QtWidgets.QFileDialog.getExistingDirectory(None,"","",QtWidgets.QFileDialog.ShowDirsOnly)
        self.edit_location.setText(self.file_dialog)

    def create_workspace (self) :

        def error (form,fields) :
            
            self.lbl_workspace_state.setText(f"The following {form} has not been completed : {fields}")
            self.lbl_workspace_state.setStyleSheet("font-size : 16px; color : #ff4246;")


        project_name = self.edit_project_name.text()
        location = self.edit_location.text()
        in_geo = self.edit_in.text()
        out_geo = self.edit_out.text()
        scenes = self.edit_scenes.text()
        out_render = self.edit_out_render.text()
        resources = self.edit_resources.text()

        if project_name == "" or location == "" :

            if project_name == "" and location == "" :
                error("fields","Project Name and Location")

            elif project_name == "" :
                error("field","Project Name")

            elif location == "" : 
                error("field","Location")  

        else :

            #- Main Directory
            main_path = os.path.join(location, project_name)
            os.mkdir(main_path)
            #- In Geo
            in_path = os.path.join(main_path, in_geo)
            os.mkdir(in_path)
            #- Out Geo
            out_path = os.path.join(main_path, out_geo)
            os.mkdir(out_path)
            #- Scenes
            scenes_path = os.path.join(main_path, scenes)
            os.mkdir(scenes_path)
            #- Out Render
            outrender_path = os.path.join(main_path, out_render)
            os.mkdir(outrender_path)
            #- Resources
            resources_path = os.path.join(main_path, resources)
            os.mkdir(resources_path)
            #- Data
            os.mkdir(f"{main_path}/data")

            #- create worspace file

            workspace_json = "workspace.json"

            workspace = {
                "project_name" : project_name,
                "location" :location,
                "in_geo" : in_geo,
                "out_geo" : out_geo,
                "scenes" : scenes,
                "out_render" : out_render,
                "resources" : resources
            }

            with open (os.path.join(main_path, workspace_json), "w", encoding="utf-8") as out_file :
                json.dump(workspace, out_file, ensure_ascii=False, indent=4)

            self.lbl_workspace_state.setText(f"The project has been created !")
            self.lbl_workspace_state.setStyleSheet("font-size : 16px; color : #5af849;")

    def add_property (self, widget, node=None) :
       
        #- Clean property bin

        while self.lyt_ppb_settings.count():
            item = self.lyt_ppb_settings.takeAt(0)
            old_widget_settings = item.widget()
            if old_widget_settings is not None:
                old_widget_settings.deleteLater()

        while self.lyt_ppb_infos.count():
            item = self.lyt_ppb_infos.takeAt(0)
            old_widget_infos = item.widget()
            if old_widget_infos is not None:
                old_widget_infos.deleteLater()

        #- Add widget to ppb settings & infos

        self.ppb_instance = Ppb_Widget(data_manager=self.data_manager)
        methods_to_call = [widget, f"{widget}_info"] # List all methods to call in property_bin.py

        for m in methods_to_call:
            method = getattr(self.ppb_instance, m, None)
            if "info" in m:
                method(self.lyt_ppb_infos)
            else :
                method(self.lyt_ppb_settings)

    def delete_properties (self) :

        while self.lyt_property_list.count():
            item = self.lyt_property_list.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

