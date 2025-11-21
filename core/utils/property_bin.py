from PySide6 import QtWidgets, QtGui, QtCore
from NodeGraphQt import NodeGraph, BaseNode
import os
import subprocess

import core.config as paths


from ui.property_bin.render_settings import Render_Settings
from ui.property_bin.load import Load
from ui.property_bin.camera import Camera
from ui.property_bin.layer import Layer

# ========================================================= PPB ========================================================= 

class Ppb_Widget (QtWidgets.QWidget) :

    def __init__(self,data_manager, node_graph):
        super().__init__()

        self.data_manager = data_manager
        self.node_graph = node_graph
        
        #self.layer = Layer(self.node_graph)

    # ---------------------------------------------------------------- DEFAULT ----------------------------------------------------------------

    def default_widget (self, title, soft): 

        if soft == "maya" :
            bg_widget_color_top = "#4b76ce"
            bg_widget_color_bottom = "#0e0d1b"
            bg_widget_color_top_hover = "#c126c6"
            bg_widget_color_bottom_hover = "#180c18"
            bg_title_color = "#3964b0"
            border_color = "#07152c"
        else :
            bg_widget_color_top = "#fe4703"
            bg_widget_color_bottom = "#1a0600"
            bg_widget_color_top_hover = "#ec0808"
            bg_widget_color_bottom_hover = "#180000"
            bg_title_color = "#fe4703"
            border_color = "#360e00"

        #- Main 

        grp_widget_default = QtWidgets.QWidget()
        grp_widget_default.setObjectName("grp_default")
        grp_widget_default.setStyleSheet(f""" 
            #grp_default {{ 
                border-radius : 4px;             
                background-color: qlineargradient(
                x1:0, y1:0, x2:0.3, y2:0.8,
                stop:0 {bg_widget_color_top},
                stop:1 {bg_widget_color_bottom} );                              
            }}                       
            #grp_default::hover {{
                background-color: qlineargradient(
                x1:0, y1:0, x2:0.6, y2:0.7,
                stop:0 {bg_widget_color_top_hover},
                stop:1 {bg_widget_color_bottom_hover} );                  
            }}
        """)

        lyt_default = QtWidgets.QVBoxLayout(grp_widget_default)
        lyt_default.setContentsMargins(0, 0, 0, 0)  

        #- title

        grp_title = QtWidgets.QWidget()
        grp_title.setObjectName("grp_title")
        grp_title.setStyleSheet(f""" 
            #grp_title {{ 
                border-top-left-radius : 4px; 
                border-top-right-radius : 4px; 
                background-color: {bg_title_color}; 
                border-bottom-width : 2px;
                border-bottom-style:solid;
                border-bottom-color : {border_color};          
            }}                         
        """)
        lyt_default.addWidget(grp_title)
        lyt_title = QtWidgets.QHBoxLayout(grp_title)
        lyt_title.setContentsMargins(10, 3, 3, 3)  

        lbl_title = QtWidgets.QLabel(title)
        lbl_title.setObjectName("lbl_default_title")
        lbl_title.setStyleSheet("""
            #lbl_default_title {
                color : #ffffff;
                font-size : 12px;
                font : bold ;
                letter-spacing : 2px;
            }
        """)
        lyt_title.addWidget(lbl_title)

        return grp_widget_default, lyt_default

    def default_separator (self, layout) :

        default_sprt = QtWidgets.QFrame()
        default_sprt.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        default_sprt.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        default_sprt.setStyleSheet("""
            QFrame {
                color : #ffffff ;
                min-height : 1px; 
                max-height : 1px;
                margin-left:5px;
            }
        """)
        layout.addWidget(default_sprt)

    def default_file_browser (self,layout, soft) : 

        if soft == "maya" : 
            border_color = "#c126c6"
            icon_folder_load = paths.RFM_ICON_FOLDER_LOAD
            icon_folder_load_hover = paths.RFM_ICON_FOLDER_LOAD_HOVER
            icon_folder_load_pressed = paths.RFM_ICON_FOLDER_LOAD_PRESSED
        else :
            border_color = "#fe4703"
            icon_folder_load = paths.RFH_ICON_FOLDER_LOAD
            icon_folder_load_hover = paths.RFH_ICON_FOLDER_LOAD_HOVER
            icon_folder_load_pressed = paths.RFH_ICON_FOLDER_LOAD_PRESSED

        lyt_browser = QtWidgets.QHBoxLayout()
        layout.addLayout(lyt_browser)

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
                border : 1px solid {border_color};
            }}
        """)
        lyt_browser.addWidget(self.edit_browser)

        btn_open_browser = QtWidgets.QPushButton()
        btn_open_browser.setStyleSheet(f"""
            QPushButton {{
                border: none;
                icon : url("{icon_folder_load}");
                icon-size : 30px;
                margin-right : 5px;
            }}
            QPushButton::hover{{
                icon: url("{icon_folder_load_hover}");
            }}
            QPushButton::pressed{{
                icon: url("{icon_folder_load_pressed}");
            }}
        """)
        btn_open_browser.clicked.connect(self.open_browser_load)
        lyt_browser.addWidget(btn_open_browser, alignment=QtGui.Qt.AlignCenter)
    
    def default_node_info (self, layout, name, label) :

        #- info title

        lbl_info_node = QtWidgets.QLabel("Node informations")
        lbl_info_node.setStyleSheet("""QLabel{ color : #ffffff; font-size : 16px; }""")
        layout.addWidget(lbl_info_node)

        sprt_title = QtWidgets.QFrame()
        sprt_title.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        sprt_title.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        sprt_title.setStyleSheet("QFrame {color : #ffffff ;min-height : 1px; max-height : 1px;margin-bottom:5px;}")
        layout.addWidget(sprt_title)

        #- Node name

        lyt_info_name = QtWidgets.QHBoxLayout()
        layout.addLayout(lyt_info_name)

        lbl_info_title_name = QtWidgets.QLabel("Node name : ")
        lbl_info_title_name.setStyleSheet("""QLabel{ color : #ffffff; font : bold; }""")
        lyt_info_name.addWidget(lbl_info_title_name)

        lbl_info_name = QtWidgets.QLabel(name)
        lbl_info_name.setStyleSheet("""QLabel{ color : #ffffff; }""")
        lyt_info_name.addWidget(lbl_info_name)

        #- Node label

        lyt_info_label = QtWidgets.QHBoxLayout()
        layout.addLayout(lyt_info_label)

        lbl_info_title_label = QtWidgets.QLabel("Node label : ")
        lbl_info_title_label.setStyleSheet("""QLabel{ color : #ffffff; font : bold; }""")
        lyt_info_label.addWidget(lbl_info_title_label)

        lbl_info_label = QtWidgets.QLabel(label)
        lbl_info_label.setStyleSheet("""QLabel{ color : #ffffff }""")
        lyt_info_label.addWidget(lbl_info_label)

        #- Node type

        lyt_info_type = QtWidgets.QHBoxLayout()
        layout.addLayout(lyt_info_type)

        lbl_info_title_type = QtWidgets.QLabel(f"Node type : ")
        lbl_info_title_type.setStyleSheet("""QLabel{ color : #ffffff; font : bold; }""")
        lyt_info_type.addWidget(lbl_info_title_type)

        lbl_info_type = QtWidgets.QLabel("Render Settings")
        lbl_info_type.setStyleSheet("""QLabel{ color : #ffffff }""")
        lyt_info_type.addWidget(lbl_info_type)

        #- Node type

        lyt_info_color = QtWidgets.QHBoxLayout()
        layout.addLayout(lyt_info_color)

        lbl_info_title_color = QtWidgets.QLabel(f"Node color : ")
        lbl_info_title_color.setStyleSheet("""QLabel{ color : #ffffff; font : bold; }""")
        lyt_info_color.addWidget(lbl_info_title_color)

        lbl_info_color = QtWidgets.QLabel("#ffffff")
        lbl_info_color.setStyleSheet("""QLabel{ color : #ffffff }""")
        lyt_info_color.addWidget(lbl_info_color)

        #- Node explanation

        lbl_info_node = QtWidgets.QLabel("Node explanations")
        lbl_info_node.setStyleSheet("""QLabel{ color : #ffffff; font-size : 16px; }""")
        layout.addWidget(lbl_info_node)

        sprt_explanation = QtWidgets.QFrame()
        sprt_explanation.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        sprt_explanation.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        sprt_explanation.setStyleSheet("QFrame {color : #ffffff ;min-height : 1px; max-height : 1px;margin-bottom:5px;}")
        layout.addWidget(sprt_explanation)

    # ========================================================= MAYA ========================================================= 

    # ---------------------------------------------------------------- RFM LOAD ----------------------------------------------------------------

    def ppb_rfm_load (self,layout) :

        layout.addWidget(Load(soft="maya"))

        return self
    
    def ppb_rfm_load_info (self, layout) :

        grp_main_info = QtWidgets.QWidget()
        lyt_main_info = QtWidgets.QVBoxLayout()
        grp_main_info.setLayout(lyt_main_info)

        #-----# Node information #-----#

        self.default_node_info(lyt_main_info, self.data_manager.get_text()[0], self.data_manager.get_text()[1])

        #-----# Settings information #-----#

        #- Size

        lbl_info_title_size = QtWidgets.QLabel(f"File browser : ")
        lbl_info_title_size.setStyleSheet("""QLabel{ color : #ffffff; font : bold; margin-bottom : 2px; }""")
        lyt_main_info.addWidget(lbl_info_title_size)
        
        lbl_info_size = QtWidgets.QLabel(f"You can an maya or houdini file \nto pick up in file browser icon ")
        lbl_info_size.setStyleSheet("""QLabel{ color : #ffffff; margin-bottom : 2px; }""")
        lyt_main_info.addWidget(lbl_info_size)

        lyt_main_info.addStretch()

        layout.addWidget(grp_main_info)
 
    # ---------------------------------------------------------------- RFM CAM ----------------------------------------------------------------

    def ppb_rfm_camera (self,layout) :

        layout.addWidget(Camera(soft="maya"))

        return self
    
    def ppb_rfm_camera_info (self, layout) :

        grp_main_info = QtWidgets.QWidget()
        lyt_main_info = QtWidgets.QVBoxLayout()
        grp_main_info.setLayout(lyt_main_info)

        #-----# Node information #-----#

        self.default_node_info(lyt_main_info, self.data_manager.get_text()[0], self.data_manager.get_text()[1])

        #-----# Settings information #-----#

        #- Size

        lbl_info_title = QtWidgets.QLabel(f"File browser : ")
        lbl_info_title.setStyleSheet("""QLabel{ color : #ffffff; font : bold; margin-bottom : 2px; }""")
        lyt_main_info.addWidget(lbl_info_title)
        
        lbl_info = QtWidgets.QLabel(f"You can an maya or houdini file \nto pick up in file browser icon ")
        lbl_info.setStyleSheet("""QLabel{ color : #ffffff; margin-bottom : 2px; }""")
        lyt_main_info.addWidget(lbl_info)

        lyt_main_info.addStretch()

        layout.addWidget(grp_main_info)

    # ---------------------------------------------------------------- RFM MERGE ----------------------------------------------------------------

    def ppb_rfm_merge (self, layout) :
        
        grp_main_merge, lyt_main_merge = self.default_widget("Rfm Merge", "maya")

        #- recover inputs names

        list_connected_ports = self.node.connected_input_nodes()

        list_name_input = []

        for keys, values in list_connected_ports.items() :
            for e in values : 
                recover_name = str(e).split('(')[-1].split(')')[0]
                name = recover_name.replace('"',"")
                list_name_input.append(name)

        #- form a list 
        
        form_input_merge = "Inputs :\n\n"
        for name in list_name_input :
            form_input_merge += f"   {name}\n"

        #- Write into a label

        lbl_input_merge = QtWidgets.QLabel(form_input_merge)
        lbl_input_merge.setStyleSheet("""
            QLabel {
                color : #ffffff;
                margin-left : 4px;   
                margin-top : 2px;                        
            }
        """)
        lyt_main_merge.addWidget(lbl_input_merge)

        layout.addWidget(grp_main_merge)

    # ---------------------------------------------------------------- RFM CRYPTOS ----------------------------------------------------------------

    def ppb_rfm_cryptomatte (self, layout) :
        
        grp_main_cryptos, lyt_main_cryptos = self.default_widget("Rfm Cryptomatte", "maya")

        btn_title_crypto = QtWidgets.QPushButton("Cryptomatte")
        lyt_main_cryptos.addWidget(btn_title_crypto)

        layout.addWidget(grp_main_cryptos)

        return self
    
    # ---------------------------------------------------------------- RFM AOVS ----------------------------------------------------------------

    def ppb_rfm_aovs (self, layout) :
        
        grp_main_aovs, lyt_main_aovs = self.default_widget("Rfm Aovs", "maya")

        btn_title_aovs = QtWidgets.QPushButton("Aovs")
        lyt_main_aovs.addWidget(btn_title_aovs)

        layout.addWidget(grp_main_aovs)

        return self
    
    # ---------------------------------------------------------------- RFM LAYERS ----------------------------------------------------------------

    def ppb_rfm_layer (self,layout) :

        layout.addWidget(Layer(soft="maya", node_graph=self.node_graph))

        return self

    def ppb_rfm_layer_info (self, layout) :

        grp_main_info = QtWidgets.QWidget()
        lyt_main_info = QtWidgets.QVBoxLayout()
        grp_main_info.setLayout(lyt_main_info)

        #-----# Node information #-----#

        self.default_node_info(lyt_main_info, self.data_manager.get_text()[0], self.data_manager.get_text()[1])

        #-----# Settings information #-----#

        #- Size

        lbl_info_title_size = QtWidgets.QLabel(f"Size : ")
        lbl_info_title_size.setStyleSheet("""QLabel{ color : #ffffff; font : bold; margin-bottom : 2px; }""")
        lyt_main_info.addWidget(lbl_info_title_size)
        
        lbl_info_size = QtWidgets.QLabel(f"You can choose default image \nsizes from the drop-down menu or \nenter the size of your choice directly \nin the boxes.")
        lbl_info_size.setStyleSheet("""QLabel{ color : #ffffff; margin-bottom : 2px; }""")
        lyt_main_info.addWidget(lbl_info_size)

        #- Frame range 

        lbl_info_title_fr = QtWidgets.QLabel(f"Frame Range : ")
        lbl_info_title_fr.setStyleSheet("""QLabel{ color : #ffffff; font : bold; margin-bottom : 2px;}""")
        lyt_main_info.addWidget(lbl_info_title_fr)

        lbl_info_frame_range = QtWidgets.QLabel(f"Single to render one frame\n Range to render a series of \nconsecutive frames \nCustom to render several different \nframes")
        lbl_info_frame_range.setStyleSheet("""QLabel{ color : #ffffff; margin-bottom : 2px; }""")
        lyt_main_info.addWidget(lbl_info_frame_range)

        lyt_main_info.addStretch()

        layout.addWidget(grp_main_info)

    # ---------------------------------------------------------------- RFM RENDER ----------------------------------------------------------------

    def ppb_rfm_render (self, layout) :
        
        layout.addWidget(Render_Settings(soft="maya"))

        return self

    def ppb_rfm_render_info (self, layout) :

        grp_main_info = QtWidgets.QWidget()
        lyt_main_info = QtWidgets.QVBoxLayout()
        grp_main_info.setLayout(lyt_main_info)

        #-----# Node information #-----#

        self.default_node_info(lyt_main_info, self.data_manager.get_text()[0], self.data_manager.get_text()[1])

        #-----# Settings information #-----#

        #- Size

        lbl_info_title_size = QtWidgets.QLabel(f"Size : ")
        lbl_info_title_size.setStyleSheet("""QLabel{ color : #ffffff; font : bold; margin-bottom : 2px; }""")
        lyt_main_info.addWidget(lbl_info_title_size)
        
        lbl_info_size = QtWidgets.QLabel(f"You can choose default image \nsizes from the drop-down menu or \nenter the size of your choice directly \nin the boxes.")
        lbl_info_size.setStyleSheet("""QLabel{ color : #ffffff; margin-bottom : 2px; }""")
        lyt_main_info.addWidget(lbl_info_size)

        #- Frame range 

        lbl_info_title_fr = QtWidgets.QLabel(f"Frame Range : ")
        lbl_info_title_fr.setStyleSheet("""QLabel{ color : #ffffff; font : bold; margin-bottom : 2px;}""")
        lyt_main_info.addWidget(lbl_info_title_fr)

        lbl_info_frame_range = QtWidgets.QLabel(f"Single to render one frame\n Range to render a series of \nconsecutive frames \nCustom to render several different \nframes")
        lbl_info_frame_range.setStyleSheet("""QLabel{ color : #ffffff; margin-bottom : 2px; }""")
        lyt_main_info.addWidget(lbl_info_frame_range)

        lyt_main_info.addStretch()

        layout.addWidget(grp_main_info)

    # ========================================================= HOUDINI ========================================================= 

    # ---------------------------------------------------------------- RFH LOAD ----------------------------------------------------------------
    def ppb_rfh_load (self,layout) :

        layout.addWidget(Load(soft="houdini"))

        return self
    
    def ppb_rfh_load_info (self, layout) :

        grp_main_info = QtWidgets.QWidget()
        lyt_main_info = QtWidgets.QVBoxLayout()
        grp_main_info.setLayout(lyt_main_info)

        #-----# Node information #-----#

        self.default_node_info(lyt_main_info, self.data_manager.get_text()[0], self.data_manager.get_text()[1])

        #-----# Settings information #-----#

        #- Size

        lbl_info_title_size = QtWidgets.QLabel(f"Size : ")
        lbl_info_title_size.setStyleSheet("""QLabel{ color : #ffffff; font : bold; margin-bottom : 2px; }""")
        lyt_main_info.addWidget(lbl_info_title_size)
        
        lbl_info_size = QtWidgets.QLabel(f"You can choose default image \nsizes from the drop-down menu or \nenter the size of your choice directly \nin the boxes.")
        lbl_info_size.setStyleSheet("""QLabel{ color : #ffffff; margin-bottom : 2px; }""")
        lyt_main_info.addWidget(lbl_info_size)

        #- Frame range 

        lbl_info_title_fr = QtWidgets.QLabel(f"Frame Range : ")
        lbl_info_title_fr.setStyleSheet("""QLabel{ color : #ffffff; font : bold; margin-bottom : 2px;}""")
        lyt_main_info.addWidget(lbl_info_title_fr)

        lbl_info_frame_range = QtWidgets.QLabel(f"Single to render one frame\n Range to render a series of \nconsecutive frames \nCustom to render several different \nframes")
        lbl_info_frame_range.setStyleSheet("""QLabel{ color : #ffffff; margin-bottom : 2px; }""")
        lyt_main_info.addWidget(lbl_info_frame_range)

        lyt_main_info.addStretch()

        layout.addWidget(grp_main_info)

    # ---------------------------------------------------------------- RFH CAMERA ----------------------------------------------------------------

    def ppb_rfh_camera (self,layout) :

        layout.addWidget(Camera(soft="houdini"))

        return self
    
    def ppb_rfh_camera_info (self, layout) :

        grp_main_info = QtWidgets.QWidget()
        lyt_main_info = QtWidgets.QVBoxLayout()
        grp_main_info.setLayout(lyt_main_info)

        #-----# Node information #-----#

        self.default_node_info(lyt_main_info, self.data_manager.get_text()[0], self.data_manager.get_text()[1])

        #-----# Settings information #-----#

        #- Size

        lbl_info_title = QtWidgets.QLabel(f"File browser : ")
        lbl_info_title.setStyleSheet("""QLabel{ color : #ffffff; font : bold; margin-bottom : 2px; }""")
        lyt_main_info.addWidget(lbl_info_title)
        
        lbl_info = QtWidgets.QLabel(f"You can an maya or houdini file \nto pick up in file browser icon ")
        lbl_info.setStyleSheet("""QLabel{ color : #ffffff; margin-bottom : 2px; }""")
        lyt_main_info.addWidget(lbl_info)

        lyt_main_info.addStretch()

        layout.addWidget(grp_main_info)
 
    # ---------------------------------------------------------------- RFH RENDER ----------------------------------------------------------------

    def ppb_rfh_render (self,layout) :

        layout.addWidget(Render_Settings(soft="houdini"))

        return self

    def ppb_rfh_render_info (self, layout) :

        grp_main_info = QtWidgets.QWidget()
        lyt_main_info = QtWidgets.QVBoxLayout()
        grp_main_info.setLayout(lyt_main_info)

        #-----# Node information #-----#

        self.default_node_info(lyt_main_info, self.data_manager.get_text()[0], self.data_manager.get_text()[1])

        #-----# Settings information #-----#

        #- Size

        lbl_info_title_size = QtWidgets.QLabel(f"Size : ")
        lbl_info_title_size.setStyleSheet("""QLabel{ color : #ffffff; font : bold; margin-bottom : 2px; }""")
        lyt_main_info.addWidget(lbl_info_title_size)
        
        lbl_info_size = QtWidgets.QLabel(f"You can choose default image \nsizes from the drop-down menu or \nenter the size of your choice directly \nin the boxes.")
        lbl_info_size.setStyleSheet("""QLabel{ color : #ffffff; margin-bottom : 2px; }""")
        lyt_main_info.addWidget(lbl_info_size)

        #- Frame range 

        lbl_info_title_fr = QtWidgets.QLabel(f"Frame Range : ")
        lbl_info_title_fr.setStyleSheet("""QLabel{ color : #ffffff; font : bold; margin-bottom : 2px;}""")
        lyt_main_info.addWidget(lbl_info_title_fr)

        lbl_info_frame_range = QtWidgets.QLabel(f"Single to render one frame\n Range to render a series of \nconsecutive frames \nCustom to render several different \nframes")
        lbl_info_frame_range.setStyleSheet("""QLabel{ color : #ffffff; margin-bottom : 2px; }""")
        lyt_main_info.addWidget(lbl_info_frame_range)

        lyt_main_info.addStretch()

        layout.addWidget(grp_main_info)

    # ========================================================= EVENT ========================================================= 

    def open_browser_load(self):
        file_dialog = QtWidgets.QFileDialog.getOpenFileName(self,"Select Folder","","")
        print(">>> Result:", file_dialog) 
        if file_dialog:
            self.edit_browser.setText(file_dialog[0])

    def open_render_settings (self) :
            
        subprocess.Popen([paths.PYTHON_PATH, os.path.join(os.path.join(paths.BASE_PATH, "ui"), "render_settings.py")])


