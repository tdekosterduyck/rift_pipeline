# =============================================================
# Nom du fichier :    Rfh_nodes.py
# Auteur :            Thomas Dekoster-Duyck
# Contact             dkthomas.pro@gmail.com
# Date de création :  22/09/2025
# Description :       Nodes Creation
# Version :           1.2
# Python :            3.12+
# =============================================================

"""
TO DO :

- Add Rfh Load button to propertyBin
- Improve nodes
- 

CHANGELOG :

1.1 : basic node creation
1.2

SUMMARY

line 33 : Rfh Load

"""

from Qt import QtWidgets, QtGui, QtCore 
from NodeGraphQt import NodeGraph, PropertiesBinWidget, constants, BaseNode, NodeBaseWidget
import PySide6 

import sys
import os

from ui.property_bin.render_settings import Render_Settings
import core.config as paths

## ========================================================= ## DEFAULT IMAGE WIDGET ## ========================================================= ##

class Default_ImgWdgt (QtWidgets.QWidget):
    def __init__(self,icon, parent=None):
        super(Default_ImgWdgt, self).__init__(parent)

        # Créer un QLabel pour l’image
        self.label = QtWidgets.QLabel()
        self.pixmap = QtGui.QPixmap(icon)
        self.label.setPixmap(self.pixmap.scaled(30,30))

        self.lyt = QtWidgets.QVBoxLayout(self)
        self.lyt.setContentsMargins(0,0,0,0)
        self.lyt.addWidget(self.label)

class Default_ImgWrpr (NodeBaseWidget):
    def __init__(self, icon, parent=None):
        super(Default_ImgWrpr, self).__init__(parent)
        self.set_name("icon_default")
        self.set_custom_widget(Default_ImgWdgt(icon))

    def get_value(self):
        return None

    def set_value(self, value):
        pass

## ========================================================= ## Rfh LOAD ## ========================================================= ##

class Rfh_Load (BaseNode):

    """
    Creation of loading node (maya scenes, alembic, obj...)
    """

    __identifier__ = 'IMPORT'
    NODE_NAME = 'Rfh Load'

    def __init__(self):
        super(Rfh_Load, self).__init__()

        self.set_icon(icon=paths.ICON_HOUDINI)
        self.set_name(name="Load")
        self.add_output('out')
        self.set_color(254,71,3)

        self.create_property("label", "rfh_load", items=None, range=None, widget_type=None, widget_tooltip=None, tab=None)

        # Ajouter le label comme widget dans le node
        self.add_custom_widget(Default_ImgWrpr(paths.ICON_RFH_LOAD, self.view))

## ========================================================= ## Rfh MERGE ## ========================================================= ##      

class Rfh_Merge (BaseNode):
    __identifier__ = 'MERGE'
    NODE_NAME = 'Rfh Merge'

    def __init__(self):
        super(Rfh_Merge, self).__init__()

        self.set_name(name="Merge")
        self.set_icon(icon=paths.ICON_HOUDINI)
        self.add_input('in_geo',multi_input=True,color=(13,64,179))
        self.add_input('in_light',multi_input=True,color=(227,247,4))    
        self.add_input('in_cam',multi_input=False,color=(247,4,4))
        self.add_output('out')
        self.set_color(254,71,3)

        self.add_custom_widget(Default_ImgWrpr(paths.ICON_MERGE, self.view))

## ========================================================= ## Rfh CAMERA ## ========================================================= ##

class Rfh_Camera (BaseNode):
    __identifier__ = 'IMPORT'
    NODE_NAME = 'Rfh Camera'

    def __init__(self):
        super(Rfh_Camera, self).__init__()

        self.set_name(name="Camera")
        self.set_icon(icon=paths.ICON_HOUDINI)
        self.add_output('out')
        self.set_color(254,71,3) 

        self.add_custom_widget(Default_ImgWrpr(paths.ICON_CAMERA, self.view))  

## ========================================================= ## Rfh AOVS ## ========================================================= ##

class Rfh_Aovs (BaseNode) :

    __identifier__ = 'RENDER'
    NODE_NAME = 'Rfh Aovs'

    def __init__(self):
        super(Rfh_Aovs, self).__init__()

        self.set_name(name="Aovs")
        self.set_icon(icon=paths.ICON_HOUDINI)
        self.add_input('in', multi_input=True)
        self.add_output('out')
        self.set_color(254,71,3)   

        self.add_custom_widget(Default_ImgWrpr(paths.ICON_AOVS, self.view))  


## ========================================================= ## Rfh CRYPTOS ## ========================================================= ##

class Rfh_Cryptos (BaseNode):
    __identifier__ = 'RENDER'
    NODE_NAME = 'Rfh Cryptomatte'

    def __init__(self):
        super(Rfh_Cryptos, self).__init__()

        self.set_name(name="Cryptomatte")
        self.set_icon(icon=paths.ICON_HOUDINI)
        self.add_input('in',multi_input=True)
        self.add_output('out')
        self.set_color(254,71,3)

        self.add_custom_widget(Default_ImgWrpr(paths.ICON_CRYPTOS, self.view))   

## ========================================================= ## Rfh LAYER ## ========================================================= ##

class Rfh_Layers (BaseNode):
    __identifier__ = 'RENDER'
    NODE_NAME = 'Rfh Layers'

    def __init__(self):
        super(Rfh_Layers, self).__init__()

        self.set_name(name="Layers")
        self.set_icon(icon=paths.ICON_HOUDINI)
        self.add_input('in',multi_input=True)
        self.add_output('out')
        self.set_color(254,71,3) 

        self.add_custom_widget(Default_ImgWrpr(paths.ICON_LAYERS, self.view))   

## ========================================================= ## Rfh RENDER ## ========================================================= ##

class Rfh_Render (BaseNode):
    __identifier__ = 'RENDER'
    NODE_NAME = 'Rfh Render'

    def __init__(self):
        super(Rfh_Render, self).__init__()

        self.set_name(name="Render")
        self.set_icon(icon=paths.ICON_HOUDINI)
        self.add_input('in',multi_input=True)
        self.add_output('out')
        self.set_color(254,71,3)

        self.create_property("label", "rfh_render", items=None, range=None, widget_type=None, widget_tooltip=None, tab=None)

        self.add_custom_widget(Default_ImgWrpr(paths.ICON_RFH_RENDER, self.view))  
        #self.add_custom_widget(Window_Render_Wrapper(self.view), tab='Settings')


