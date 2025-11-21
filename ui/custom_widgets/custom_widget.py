from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import QSize

import core.config as paths

class Cstm_Widgets :

    def title_sidebar_style (name, layout, icon, hover_color) :
        """
        Default button style for side bar with icon path inside
        """
        btn_default_sidebar = QtWidgets.QPushButton(name)
        btn_default_sidebar.setStyleSheet(f"""
            QPushButton{{
                color: #ffffff;
                font-weight : 12px;
                font-size : 14px;
                padding : 4px;     
                letter-spacing : 2px; 
                border : none;
                icon : url({icon});
                icon-size : 25px;    
                text-align : left;                          
            }}
            QPushButton::hover{{
                border-top-left-radius : 4px;
                border-bottom-left-radius : 4px;
                background-color: qlineargradient(
                x1:0, y1:0, x2:0.5, y2:0.8,
                stop:0 {hover_color},
                stop:1 transparent
                );          
            }}                         
        """)
        layout.addWidget(btn_default_sidebar)

        return btn_default_sidebar
    
    def create_separator(layout):
        """
        Default separator style 
        """
        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        layout.addWidget(separator)

    def default_form_style (layout, lbl, text_edit, place_holder):
        """
        Default form style for my workspace form
        """
        lbl_default_form = QtWidgets.QLabel(lbl)
        lbl_default_form.setStyleSheet("""
            QLabel {
                color: #ffffff; 
                margin-left : 25px;
            }
        """)

        edit_default_form = QtWidgets.QLineEdit(text_edit,placeholderText=place_holder)
        edit_default_form.setStyleSheet("""
            QLineEdit {
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

        layout.addRow(lbl_default_form , edit_default_form)

        return edit_default_form
    
    # ---------------------------------------- # Property Bin # ---------------------------------------- #

    def default_node_title (layout, title, icon_path, soft="maya" or "houdini") :
        """
            Default title for property bin ui
        """
        if soft == "maya" :
            stop0 = "#4b76ce"
            stop1 = "#0e0d1b"
            hover_stop0 = "#6f98ec"
            hover_stop1 = "#1b1a33"
        else :
            stop0 = "#d6582a"
            stop1 = "#1a0600"
            hover_stop0 = "#ee6736"
            hover_stop1 = "#250d05"

        #- Degraded group for title
        grp_default_title = QtWidgets.QWidget()
        grp_default_title.setObjectName("grp_default_title")
        grp_default_title.setMinimumHeight(35)
        grp_default_title.setStyleSheet(f"""
            #grp_default_title {{ 
                border-radius : 2px;                      
                background-color: qlineargradient(
                x1:0, y1:0, x2:0.8, y2:0.4,
                stop:0 {stop0},
                stop:1 {stop1} ); 
            }}
            #grp_default_title::hover {{
                background-color: qlineargradient(
                x1:0, y1:0, x2:0.6, y2:0.7,
                stop:0 {hover_stop0},
                stop:1 {hover_stop1});                  
            }}
            """)

        #- Layout Title
        lyt_default_title = QtWidgets.QHBoxLayout()
        grp_default_title.setLayout(lyt_default_title)
        lyt_default_title.setContentsMargins(10, 1, 1, 1)  

        #- Icon of node
        lbl_default_icon = QtWidgets.QLabel()

        default_icon = QtGui.QPixmap(icon_path)

        lbl_default_icon.setPixmap(default_icon)
        lbl_default_icon.setPixmap(default_icon.scaled(20,20))
        lyt_default_title.addWidget(lbl_default_icon)

        #- Title
        lbl_default_title = QtWidgets.QLabel(title)
        lbl_default_title.setStyleSheet("""
            QLabel {  
                font-size : 16px;
                padding-left : 2px;
                color : #ffffff;   
        } """)

        lyt_default_title.addWidget(lbl_default_title, alignment=QtCore.Qt.AlignCenter)
        lyt_default_title.addStretch()

        layout.addWidget(grp_default_title)

        layout.addSpacing(10)

    def default_node_subtitle (layout, subtitle, soft="maya" or "houdini") :
        """
            Default title for define category in nodes
        """
        if soft == "maya" :
            lbl_color = "#5489f2"
            lbl_color_hover = "#759ef0"
        else :
            lbl_color = "#fe4703"
            lbl_color_hover = "#ff6b35"

        grp_default_subtitle = QtWidgets.QWidget()
        grp_default_subtitle.setObjectName("grp_default_subtitle")
        grp_default_subtitle.setMinimumHeight(20)
        grp_default_subtitle.setStyleSheet("""
            #grp_default_subtitle { 
                border-radius : 2px;                      
                background-color: qlineargradient(
                x1:0, y1:1, x2:0.6, y2:0.6,
                stop:0 #303030,
                stop:1 transparent ); 
            }
            #grp_default_subtitle::hover {
                background-color: qlineargradient(
                x1:0, y1:1, x2:0.8, y2:0.5,
                stop:0 #454545,
                stop:1 transparent );               
            }
            """)

        lyt_default_subtitle = QtWidgets.QHBoxLayout()
        lyt_default_subtitle.setContentsMargins(1,1,1,1)
        grp_default_subtitle.setLayout(lyt_default_subtitle)

        lbl_info_node = QtWidgets.QLabel(subtitle)
        lbl_info_node.setStyleSheet(f"""
            QLabel {{
                color : {lbl_color};
                font-size : 16px;
                margin-left : 5px;
            }}
            QLabel {{
                color : {lbl_color_hover};
            }}
        """)
        lyt_default_subtitle.addWidget(lbl_info_node)

        layout.addWidget(grp_default_subtitle)