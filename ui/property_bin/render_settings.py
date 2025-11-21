from PySide6 import QtWidgets, QtGui, QtCore
import core.config as paths
from ui.custom_widgets.custom_widget import Cstm_Widgets

# =========================================================
# Class : Render_Settings
# =========================================================

class Render_Settings (QtWidgets.QWidget) :

    def __init__(self, soft ):
        super().__init__()

        self.soft = soft
        self.define_soft()
        self.ui_render_settings()

    def define_soft (self) :

        if self.soft == "maya" :

            self.color = "#4a78d3"
            self.dark_color = "#162064"
            self.hover_color = "#698dd4"
            self.soft_path = paths.ICON_RFM_RENDER

        else :

            self.color = "#d6582a"
            self.dark_color = "#3F170A"
            self.hover_color = "#ee6736"
            self.soft_path = paths.ICON_RFH_RENDER

    # ---------------------------------------------------------------- CUSTOM ----------------------------------------------------------------

    def default_line_edit (self) :
        """
            Default QEdit style for sample category
        """

        self.edit_default_sample = QtWidgets.QLineEdit()
        self.edit_default_sample.setStyleSheet(f"""
            QLineEdit {{
                background-color : #d8d8d8; 
                border-radius : 2px;
                border : 1px solid #000000;
            }}
            QLineEdit::hover {{
                background-color : #e8e8e8;  
                border-radius : 2px;  
                border : 1px solid {self.color}; 
            }}                    
        """)

        return self.edit_default_sample

    def default_slider (self, name) : 

        name.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                height: 2px;
                margin: 9px 0;
                background: #303030;
                border-radius: 2px;
            }}
            QSlider::groove:horizontal:hover{{
                border: 1px solid #ffffff;         
            }}
            QSlider::sub-page:horizontal {{
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 {self.dark_color},
                    stop:1 {self.color}
                );      
                border-radius: 2px;
            }}
            QSlider::add-page:horizontal {{
                background: #303030;
                border-radius: 2px;
            }}
            QSlider::handle:horizontal {{
                width: 20px;
                height: 30px;
                margin : -10px;
                border-radius : 8px;
            }}
        """)

    # ---------------------------------------------------------------- UI ----------------------------------------------------------------

    def ui_render_settings (self) :

        lyt_main = QtWidgets.QVBoxLayout(self)
        lyt_main.setContentsMargins(0, 0, 0, 0)  

        # ============================================================================ Title
        
        if self.soft == "maya" :
            node_title = "RFM Render Settings"
        else :
            node_title = "RFH Render Settings"

        Cstm_Widgets.default_node_title(lyt_main, node_title, self.soft_path, self.soft)

        # ============================================================================ Size

        #- Title size
        Cstm_Widgets.default_node_subtitle(lyt_main, "Size", self.soft)

        lyt_size_combo = QtWidgets.QHBoxLayout()
        lyt_size_combo.setContentsMargins(10,10,5,10)
        lyt_main.addLayout(lyt_size_combo)

        #-----# QEdit Width #-----#

        self.edit_width = self.default_line_edit()
        self.edit_width.setText("960")
        self.edit_width.setMinimumHeight(22)
        self.edit_width.setStyleSheet(f"""
            QLineEdit {{
                background-color : #d8d8d8; 
                border-radius : 2px;
                border : 1px solid #000000;
            }}
            QLineEdit::hover {{
                background-color : #e8e8e8;  
                border-radius : 2px;  
                border : 1px solid {self.color}; 
            }}                   
        """)

        lyt_size_combo.addWidget(self.edit_width)
        
        #-----# ComboBox Height #-----#

        self.combo_img_size = QtWidgets.QComboBox()
        self.combo_img_size.setObjectName("self.combo_img_size")
        self.combo_img_size.setMinimumHeight(20)
        self.combo_img_size.setMinimumWidth(95)
        self.combo_img_size.setEditable(True)
        self.combo_img_size.setStyleSheet(f"""
            QComboBox {{
                background-color : #d8d8d8; 
                border-radius : 2px;
            }}
            QComboBox::hover {{
                background-color : #e8e8e8;  
                border-radius : 2px;  
                border : 1px solid {self.color}; 
            }}       
            QComboBox::drop-down {{
                background : transparent;
                border : none;
            }}
            QComboBox::down-arrow{{
                image : url({paths.ICON_DROP_DOWN_ARROW});    
                width: 25px;
                height: 25px;  
                margin-right : 2px;                        
            }}   
        """)

        self.combo_img_size.addItem("HD 540", userData="540")
        self.combo_img_size.addItem("HD 720",userData="720")
        self.combo_img_size.addItem("HD 1080", userData="1080")
        self.combo_img_size.addItem("Scope", userData="817")
        self.combo_img_size.addItem("Custom", userData="100")

        self.combo_img_size.currentIndexChanged.connect(self.update_combobox)
        self.update_combobox(self.combo_img_size.currentIndex())

        lyt_size_combo.addWidget(self.combo_img_size)


        # ============================================================================ Frame Range 

        Cstm_Widgets.default_node_subtitle(lyt_main, "Frame Range", self.soft)

        # ----- # Scroll Frame Range # ----- #

        lyt_scroll_frame = QtWidgets.QHBoxLayout()
        lyt_scroll_frame.setContentsMargins(10,10,5,1)
        lyt_main.addLayout(lyt_scroll_frame)

        #- Btn Previous
        btn_frame_previous = QtWidgets.QPushButton()
        btn_frame_previous.setFixedSize(40,20)
        btn_frame_previous.setStyleSheet(f"""
            QPushButton {{ 
                background : {self.color};
                border-top-left-radius : 3px; 
                border-bottom-left-radius:3px;
                icon : url({paths.ICON_ARROW_PREVIOUS});
                icon-size : 10px;  
            }}
            QPushButton::hover {{
                background : {self.hover_color};
            }} 
            QPushButton::pressed{{
                margin : 1px;
            }}
            """)
        btn_frame_previous.clicked.connect(self.previous_frame)

        lyt_scroll_frame.addWidget(btn_frame_previous)

        # ----- # Stacked Widget # ----- #

        self.pg_frame_range = QtWidgets.QStackedWidget()
        self.pg_frame_range.setMaximumHeight(20)
        self.pg_frame_range.setStyleSheet("""
            QWidget { 
                background-color : #d8d8d8;
                margin : 0px;
                font:12px;
                color:#000000;
            }""")

        #- Page Single
        self.pg_single = QtWidgets.QWidget()
        
        self.lyt_single = QtWidgets.QVBoxLayout(self.pg_single)
        self.lyt_single.setContentsMargins(0,0,0,0)

        lbl_single = QtWidgets.QLabel("Single")
        self.lyt_single.addWidget(lbl_single, alignment=QtCore.Qt.AlignCenter) 

        #- Page Range
        self.pg_range = QtWidgets.QWidget()
        
        self.lyt_range = QtWidgets.QHBoxLayout(self.pg_range)
        self.lyt_range.setContentsMargins(0,0,0,0)

        lbl_range = QtWidgets.QLabel("Range")
        self.lyt_range.addWidget(lbl_range, alignment=QtCore.Qt.AlignCenter)

        #- Page Custom
        self.pg_custom = QtWidgets.QWidget()
        
        self.lyt_custom = QtWidgets.QVBoxLayout(self.pg_custom)
        self.lyt_custom.setContentsMargins(0,0,0,0)

        lbl_custom = QtWidgets.QLabel("Custom")
        self.lyt_custom.addWidget(lbl_custom, alignment=QtCore.Qt.AlignCenter)

        #- Add Page
        self.pg_frame_range.addWidget(self.pg_single)    # Index 0
        self.pg_frame_range.addWidget(self.pg_range)   # Index 1
        self.pg_frame_range.addWidget(self.pg_custom)   # Index 2

        lyt_scroll_frame.addWidget(self.pg_frame_range)

        #- Button Next
        btn_frame_next = QtWidgets.QPushButton()
        btn_frame_next.setFixedSize(40,20)
        btn_frame_next.setStyleSheet(f"""
            QPushButton {{
                background : {self.color};
                border-top-right-radius : 3px;
                border-bottom-right-radius:3px;
                icon : url({paths.ICON_ARROW_NEXT});
                icon-size : 10px;  
            }}
            QPushButton::hover {{
                background : {self.hover_color};
            }} 
            QPushButton::pressed{{
                margin : 1px;
            }}            
            """)
        btn_frame_next.clicked.connect(self.next_frame)
        lyt_scroll_frame.addWidget(btn_frame_next)       

        #-----# Layout Enter Range #-----#

        self.lyt_range_edit = QtWidgets.QHBoxLayout()
        self.lyt_range_edit.setContentsMargins(10,1,5,10)
        lyt_main.addLayout(self.lyt_range_edit) 

        #- Enter Range 

        self.edit_range = QtWidgets.QLineEdit (placeholderText="1001")
        self.edit_range.setStyleSheet(f"""
            QLineEdit {{
                background-color : #d8d8d8; 
                border-radius : 2px;
                border : 1px solid #000000;
            }}
            QLineEdit::hover {{
                background-color : #e8e8e8;   
                border : 1px solid {self.color}; 
            }}                      
        """)

        self.lyt_range_edit.addWidget(self.edit_range)
        
        # ============================================================================ Sample

        Cstm_Widgets.default_node_subtitle(lyt_main, "Sample", self.soft)

        # ----- # Min Samples # ----- #

        self.lyt_min_sample = QtWidgets.QHBoxLayout()
        self.lyt_min_sample.setContentsMargins(10,10,5,1)
        lyt_main.addLayout(self.lyt_min_sample)

        #- Label

        self.lbl_min_sample = QtWidgets.QLabel("Min")
        self.lbl_min_sample.setStyleSheet("""QLabel {color : #d8d8d8;}""")
        self.lyt_min_sample.addWidget(self.lbl_min_sample, alignment= QtCore.Qt.AlignRight)

        #- Edit

        self.edit_min_sample = self.default_line_edit()
        self.edit_min_sample.setMaximumSize(50,22)
        self.edit_min_sample.setText("32")

        self.edit_min_sample.returnPressed.connect(self.update_slider_min_sample)
        self.edit_min_sample.editingFinished.connect(self.update_slider_min_sample)
        
        self.lyt_min_sample.addWidget(self.edit_min_sample,alignment= QtCore.Qt.AlignCenter)

        #- Silder

        self.list_sample = [0,16,32,64,128,254,512,1024]

        self.slider_min_sample = QtWidgets.QSlider(orientation=QtCore.Qt.Orientation.Horizontal)
        self.slider_min_sample.setTickPosition(QtWidgets.QSlider.TickPosition.TicksBelow)
        self.slider_min_sample.setMinimum(0)
        self.slider_min_sample.setMaximum(len(self.list_sample) - 1)
        self.slider_min_sample.setTickInterval(1)
        self.slider_min_sample.setSingleStep(1)
        self.slider_min_sample.setValue(2)
        self.slider_min_sample.setFixedSize(100,30)
        self.slider_min_sample.valueChanged.connect(self.update_min_sample)
        self.default_slider(self.slider_min_sample)

        self.lyt_min_sample.addWidget(self.slider_min_sample, alignment= QtCore.Qt.AlignLeft)

        # ----- # Max Samples # ----- #

        self.lyt_max_sample = QtWidgets.QHBoxLayout()
        self.lyt_max_sample.setContentsMargins(10,1,5,1)
        lyt_main.addLayout(self.lyt_max_sample) 

        #- Label

        self.lbl_max_sample = QtWidgets.QLabel("Max")
        self.lbl_max_sample.setStyleSheet("""QLabel {color : #d8d8d8;}""")
        self.lyt_max_sample.addWidget(self.lbl_max_sample, alignment= QtCore.Qt.AlignRight)

        #- Edit

        self.edit_max_sample = self.default_line_edit()
        self.edit_max_sample.setMaximumSize(50,22)
        self.edit_max_sample.setText("128")

        self.edit_max_sample.editingFinished.connect(self.update_slider_max_sample)
        self.edit_max_sample.returnPressed.connect(self.update_slider_max_sample)
        
        self.lyt_max_sample.addWidget(self.edit_max_sample, alignment= QtCore.Qt.AlignCenter)

        #- Silder

        self.slider_max_sample = QtWidgets.QSlider(orientation=QtCore.Qt.Orientation.Horizontal)
        self.slider_max_sample.setTickPosition(QtWidgets.QSlider.TickPosition.TicksBelow)
        self.slider_max_sample.setMinimum(0)
        self.slider_max_sample.setMaximum(len(self.list_sample) - 1)
        self.slider_max_sample.setTickInterval(1)
        self.slider_max_sample.setSingleStep(1)
        self.slider_max_sample.setValue(4)
        self.slider_max_sample.setFixedSize(100,30)
        self.slider_max_sample.valueChanged.connect(self.update_max_sample)
        self.default_slider(self.slider_max_sample)

        self.lyt_max_sample.addWidget(self.slider_max_sample, alignment= QtCore.Qt.AlignLeft)

        #-----# Layout Pixel Variance #-----#

        self.lyt_pix_var = QtWidgets.QHBoxLayout()
        self.lyt_pix_var.setContentsMargins(10,1,5,10)
        lyt_main.addLayout(self.lyt_pix_var) 

        #- Label 

        self.lbl_pix_var = QtWidgets.QLabel("Variance")
        self.lbl_pix_var.setStyleSheet("""QLabel {color : #d8d8d8;}""")
        self.lyt_pix_var.addWidget(self.lbl_pix_var, alignment= QtCore.Qt.AlignRight)

        #- Edit 

        self.edit_pix_var = self.default_line_edit()
        self.edit_pix_var.setMaximumSize(50,22)
        self.edit_pix_var.setText("0.05")

        self.edit_pix_var.returnPressed.connect(self.update_slider_pixel_var)
        self.edit_pix_var.editingFinished.connect(self.update_slider_pixel_var)
        
        self.lyt_pix_var.addWidget(self.edit_pix_var, alignment= QtCore.Qt.AlignCenter)

        #- Silder 

        self.list_pix_var = [0.001,0.01,0.025,0.05,0.075,0.1,0.15,0.3]

        self.slider_pix_var = QtWidgets.QSlider(orientation=QtCore.Qt.Orientation.Horizontal)
        self.slider_pix_var.setTickPosition(QtWidgets.QSlider.TickPosition.TicksBelow)
        self.slider_pix_var.setMinimum(0)
        self.slider_pix_var.setMaximum(len(self.list_sample) - 1)
        self.slider_pix_var.setTickInterval(1)
        self.slider_pix_var.setSingleStep(1)
        self.slider_pix_var.setValue(4)
        self.slider_pix_var.setFixedSize(100,30)
        self.slider_pix_var.valueChanged.connect(self.update_pix_var)

        self.default_slider(self.slider_pix_var)

        self.lyt_pix_var.addWidget(self.slider_pix_var, alignment= QtCore.Qt.AlignLeft)

        # ============================================================================ Ver

        Cstm_Widgets.default_node_subtitle(lyt_main, "Version", self.soft)

        #-----# Ver #-----#

        self.lyt_ver = QtWidgets.QHBoxLayout()
        self.lyt_ver.setContentsMargins(10,10,5,10)
        lyt_main.addLayout(self.lyt_ver) 

        #- Button Remove Ver

        self.btn_ver_remove = QtWidgets.QPushButton()
        self.btn_ver_remove.setIcon(QtGui.QIcon(paths.ICON_MINUS))
        self.btn_ver_remove.setFixedSize(22,22)
        self.btn_ver_remove.setStyleSheet(f"""
            QPushButton {{
                background-color : {self.color}; 
                border-radius : 2px;
            }}
            QPushButton::hover {{
                background-color : {self.hover_color};  
            }}
            QPushButton::pressed {{
                margin : 1px;
            }}                 
        """)

        self.btn_ver_remove.clicked.connect(self.remove_ver)

        self.lyt_ver.addWidget(self.btn_ver_remove)

        #- Edit Ver 

        self.edit_ver = self.default_line_edit()
        self.edit_ver.setMinimumHeight(22)
        self.edit_ver.setAlignment(QtCore.Qt.AlignCenter)
        self.edit_ver.setText("1")
        self.lyt_ver.addWidget(self.edit_ver)

        #-----# Button Add Ver #-----#

        self.btn_ver_add = QtWidgets.QPushButton()
        self.btn_ver_add.setIcon(QtGui.QIcon(paths.ICON_PLUS))
        self.btn_ver_add.setFixedSize(22,22)
        self.btn_ver_add.setStyleSheet(f"""
            QPushButton {{
                background-color : {self.color}; 
                border-radius : 2px;
            }}
            QPushButton::hover {{
                background-color : {self.hover_color};  
            }}  
            QPushButton::pressed {{
                margin : 1px;
            }}                        
        """)

        self.btn_ver_add.clicked.connect(self.add_ver)

        self.lyt_ver.addWidget(self.btn_ver_add)

        # ============================================================================ Save Button

        #- Layout button
        
        self.lyt_btn_save = QtWidgets.QHBoxLayout()
        self.lyt_btn_save.setAlignment(QtGui.Qt.AlignCenter)
        lyt_main.addLayout(self.lyt_btn_save)

        self.btn_save = Cstm_Widgets.title_sidebar_style("Save",self.lyt_btn_save, paths.ICON_HOME, "#646464")
        self.btn_save.setMinimumSize(100,30)

        lyt_main.addStretch()

    # ---------------------------------------------------------------- EVENT ----------------------------------------------------------------

    #- Update ComboBox Size 

    def update_combobox(self, index):
        value = self.combo_img_size.itemData(index)
        if value:
            self.combo_img_size.setEditText(value) 
        if value == "540" :
            self.edit_width.setText("960")
        if value == "720" :
            self.edit_width.setText("1280")
        if value == "1080" :
            self.edit_width.setText("1920")
        if value == "817" :
            self.edit_width.setText("1920")
        if value == "100" :
            self.edit_width.setText("100")

    #- Previous & Next frame range page 

    def previous_frame (self) :

        current = self.pg_frame_range.currentIndex()

        if current == 0 :
            previous = 2
            self.edit_range.setPlaceholderText("1001/1005/1050")
        if current == 1:
            previous = 0
            self.edit_range.setPlaceholderText("1001")  
        if current == 2:
            previous = 1
            self.edit_range.setPlaceholderText("1001-1100")
            
        self.pg_frame_range.setCurrentIndex(previous)

    def next_frame (self) :

        current = self.pg_frame_range.currentIndex()

        if current == 2 :
            next = 0
            self.edit_range.setPlaceholderText("1001")
        if current == 1 :
            next = 2
            self.edit_range.setPlaceholderText("1001/1005/1050")
        if current == 0 :
            next = 1
            self.edit_range.setPlaceholderText("1001-1100")

        self.pg_frame_range.setCurrentIndex(next)

    #- Update des sliders 

    def update_slider_min_sample (self) :

        #- searching clotest value of user text 
        value = self.edit_min_sample.text()

        if not value :
            closest = 2
        else :
            closest = self.list_sample[0]
            min_diff = abs(int(value) - closest)

            for num in self.list_sample:
                diff = abs(int(value) - num)
                if diff < min_diff:
                    min_diff = diff
                    closest = self.list_sample.index(num)

        self.slider_min_sample.setValue(closest)

    def update_slider_max_sample (self) :

        #- searching clotest value of user text 
        value = self.edit_max_sample.text()

        if not value :
            closest = 4
        else :
            closest = self.list_sample[0]
            min_diff = abs(int(value) - closest)

            for num in self.list_sample:
                diff = abs(int(value) - num)
                if diff < min_diff:
                    min_diff = diff
                    closest = self.list_sample.index(num)

        self.slider_max_sample.setValue(closest)

    def update_slider_pixel_var (self) :

        #- searching clotest value of user text 
        value = self.edit_pix_var.text()

        if not value :
            closest = 4
        else :
            closest = self.list_pix_var[0]
            min_diff = abs(float(value) - closest)
            
            for num in self.list_pix_var:
                diff = abs(float(value) - num)
                
                if diff < min_diff:
                    min_diff = diff
                    closest = self.list_pix_var.index(num)

        self.slider_pix_var.setValue(closest)

    def update_min_sample (self, index) : 

        value = self.list_sample[index]
        self.edit_min_sample.setText(str(value))

    def update_max_sample (self, index) : 

        value = self.list_sample[index]
        self.edit_max_sample.setText(str(value))

    def update_pix_var (self, index) : 

        value = self.list_pix_var[index]
        self.edit_pix_var.setText(str(value))

    #- Add & Remove Version

    def add_ver (self) :

        actual_value = self.edit_ver.text()
        new_value = int(actual_value) + 1
        self.edit_ver.setText(str(new_value))

    def remove_ver (self) :
        
        actual_value = self.edit_ver.text()
        new_value = int(actual_value) - 1

        if new_value == 0 :
            new_value = 1

        self.edit_ver.setText(str(new_value))