# =============================================================
# Nom du fichier :    rfm_nodes.py
# Auteur :            Thomas Dekoster-Duyck
# Contact             dkthomas.pro@gmail.com
# Date de création :  22/09/2025
# Description :       Nodes Creation
# Version :           1.2
# Python :            3.12+
# =============================================================

"""
TO DO :

- Add Rfm Load button to propertyBin
- Improve nodes
- 

CHANGELOG :

1.1 : basic node creation
1.2

SUMMARY

line 33 : Rfm Load

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

## ========================================================= ## RFM LOAD ## ========================================================= ##

class Rfm_Load (BaseNode):

    """
    Creation of loading node (maya scenes, alembic, obj...)
    """

    __identifier__ = 'IMPORT'
    NODE_NAME = 'Rfm Load'

    def __init__(self):
        super(Rfm_Load, self).__init__()

        self.set_icon(icon=paths.ICON_MAYA)
        self.set_name(name="Load")
        self.add_output('out')
        self.set_color(75,118,206)

        self.create_property("label", "rfm_load", items=None, range=None, widget_type=None, widget_tooltip=None, tab=None)

        # Ajouter le label comme widget dans le node
        self.add_custom_widget(Default_ImgWrpr(paths.ICON_RFM_LOAD, self.view))

        #self.add_custom_widget(FileDialogWrapper(self.view), tab='Custom')

## ========================================================= ## RFM MERGE ## ========================================================= ##      

class Rfm_Merge (BaseNode):
    __identifier__ = 'MERGE'
    NODE_NAME = 'Rfm Merge'

    def __init__(self):
        super(Rfm_Merge, self).__init__()

        self.set_name(name="Merge")
        self.set_icon(icon=paths.ICON_MAYA)
        self.add_input('in_geo',multi_input=True,color=(13,64,179))
        self.add_input('in_light',multi_input=True,color=(227,247,4))    
        self.add_input('in_cam',multi_input=False,color=(247,4,4))
        self.add_output('out')
        self.set_color(75,118,206)

        self.create_property("label", "rfm_merge", items=None, range=None, widget_type=None, widget_tooltip=None, tab=None)

        self.add_custom_widget(Default_ImgWrpr(paths.ICON_RFM_MERGE, self.view))

## ========================================================= ## RFM CAMERA ## ========================================================= ##

class Rfm_Camera (BaseNode):
    __identifier__ = 'IMPORT'
    NODE_NAME = 'Rfm Camera'

    def __init__(self):
        super(Rfm_Camera, self).__init__()

        self.set_name(name="Camera")
        self.set_icon(icon=paths.ICON_MAYA)
        self.add_output('out')
        self.set_color(222,28,28)   

        self.create_property("label", "rfm_camera", items=None, range=None, widget_type=None, widget_tooltip=None, tab=None)

        self.add_custom_widget(Default_ImgWrpr(paths.ICON_RFM_CAMERA, self.view))  

## ========================================================= ## RFM AOVS ## ========================================================= ##

class Rfm_Aovs (BaseNode) :

    __identifier__ = 'RENDER'
    NODE_NAME = 'Rfm Aovs'

    def __init__(self):
        super(Rfm_Aovs, self).__init__()

        self.set_name(name="Aovs")
        self.set_icon(icon=paths.ICON_MAYA)
        self.add_input('in', multi_input=True)
        self.add_output('out')
        self.set_color(75,118,206)   

        self.create_property("label", "rfm_aovs", items=None, range=None, widget_type=None, widget_tooltip=None, tab=None)

        self.add_custom_widget(Default_ImgWrpr(paths.ICON_RFM_AOVS, self.view))  


## ========================================================= ## RFM CRYPTOS ## ========================================================= ##

class Rfm_Cryptos (BaseNode):
    __identifier__ = 'RENDER'
    NODE_NAME = 'Rfm Cryptomatte'

    def __init__(self):
        super(Rfm_Cryptos, self).__init__()

        self.set_name(name="Cryptomatte")
        self.set_icon(icon=paths.ICON_MAYA)
        self.add_input('in',multi_input=True)
        self.add_output('out')
        self.set_color(75,118,206)  

        self.create_property("label", "rfm_cryptos", items=None, range=None, widget_type=None, widget_tooltip=None, tab=None)

        self.add_custom_widget(Default_ImgWrpr(paths.ICON_RFM_CRYPTOS, self.view))   

## ========================================================= ## RFM LAYER ## ========================================================= ##

class Rfm_Layers (BaseNode):
    __identifier__ = 'RENDER'
    NODE_NAME = 'Rfm Layers'

    def __init__(self):
        super(Rfm_Layers, self).__init__()

        self.set_name(name="Layers")
        self.set_icon(icon=paths.ICON_MAYA)
        self.add_input('in',multi_input=True)
        self.add_output('out')
        self.set_color(75,118,206)  

        self.create_property("label", "rfm_layer", items=None, range=None, widget_type=None, widget_tooltip=None, tab=None)

        self.add_custom_widget(Default_ImgWrpr(paths.ICON_RFM_LAYERS, self.view))   

## ========================================================= ## RFM RENDER ## ========================================================= ##

class Rfm_Render (BaseNode):
    __identifier__ = 'RENDER'
    NODE_NAME = 'Rfm Render'

    def __init__(self):
        super(Rfm_Render, self).__init__()

        self.set_name(name="Render")
        self.set_icon(icon=paths.ICON_MAYA)
        self.add_input('in',multi_input=True)
        self.add_output('out')
        self.set_color(75,118,206) 

        self.create_property("label", "rfm_render", items=None, range=None, widget_type=None, widget_tooltip=None, tab=None)

        self.add_custom_widget(Default_ImgWrpr(paths.ICON_RFM_RENDER, self.view))  

