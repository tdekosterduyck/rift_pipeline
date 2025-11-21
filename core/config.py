import os

# ========================================================= PATHS ========================================================= 

# ----------- # BASE PATH # ---------- #

CORE_PATH = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.dirname(CORE_PATH)
PYTHON_PATH = os.path.join(os.path.join(BASE_PATH, "Python"), "python.exe")

ICON_PATH = os.path.join(os.path.join(BASE_PATH, "ressources"), "icons")
IMAGES_PATH = os.path.join(os.path.join(BASE_PATH, "ressources"), "images")

JSON_PATH = os.path.join(BASE_PATH, "json")

# ----------- # ICON PATH ---------- #

# ---- # Main Ui # ---- #

#- Side bar

ICON_HOME = os.path.join(ICON_PATH, "home.png").replace("\\","/")
ICON_GRAPH = os.path.join(ICON_PATH, "render_graph.svg").replace("\\","/")
ICON_FARM = os.path.join(ICON_PATH, "farm.svg").replace("\\","/")
ICON_SETTINGS = os.path.join(ICON_PATH, "settings.png").replace("\\","/")
ICON_EXIT = os.path.join(ICON_PATH, "exit.png").replace("\\","/")

#- Home page

ICON_LOGO = os.path.join(ICON_PATH, "logo.png").replace("\\","/")
ICON_TITLE = os.path.join(IMAGES_PATH, "title.png").replace("\\","/")
ICON_CREATE_WP = os.path.join(ICON_PATH, "create_workspace.svg").replace("\\","/")

#- Workspace page

ICON_BG = os.path.join(IMAGES_PATH, "bg.png").replace("\\","/")
ICON_RETURN = os.path.join(ICON_PATH, "return.svg").replace("\\","/")

#- Graph page

ICON_LOCK = os.path.join(ICON_PATH, "lock.png").replace("\\","/")
ICON_CLEAR = os.path.join(ICON_PATH, "clear.png").replace("\\","/")

# ---- # Nodes # ---- #

#- Rfm Nodes

ICON_MAYA = os.path.join(ICON_PATH, "maya.png")
ICON_RFM_LOAD = os.path.join(ICON_PATH, "rfm_load.svg")
ICON_RFM_MERGE = os.path.join(ICON_PATH, "rfm_merge.svg")
ICON_RFM_CAMERA = os.path.join(ICON_PATH, "rfm_camera.svg")
ICON_RFM_AOVS = os.path.join(ICON_PATH, "rfm_aovs.svg")
ICON_RFM_CRYPTOS = os.path.join(ICON_PATH, "rfm_cryptos.svg")
ICON_RFM_LAYERS = os.path.join(ICON_PATH, "rfm_layers.svg")
ICON_RFM_RENDER = os.path.join(ICON_PATH, "rfm_render.svg")

#- Rfh Nodes

ICON_HOUDINI = os.path.join(ICON_PATH, "houdini.png")
ICON_RFH_LOAD = os.path.join(ICON_PATH, "rfh_load.svg")
ICON_RFH_MERGE = os.path.join(ICON_PATH, "rfh_merge.svg")
ICON_RFH_CAMERA = os.path.join(ICON_PATH, "rfh_camera.svg")
ICON_RFH_AOVS = os.path.join(ICON_PATH, "rfh_aovs.svg")
ICON_RFH_CRYPTOS = os.path.join(ICON_PATH, "rfh_cryptos.svg")
ICON_RFH_LAYERS = os.path.join(ICON_PATH, "rfh_layers.svg")
ICON_RFH_RENDER = os.path.join(ICON_PATH, "rfh_render.svg")

# ---- # Property Bin # ---- #

#- Maya

RFM_ICON_FOLDER = os.path.join(ICON_PATH, "rfm_folder.svg").replace("\\","/")
RFM_ICON_FOLDER_HOVER = os.path.join(ICON_PATH, "rfm_folder_hover.svg").replace("\\","/")

#- Houdini

RFH_ICON_FOLDER = os.path.join(ICON_PATH, "rfh_folder.svg").replace("\\","/")
RFH_ICON_FOLDER_HOVER = os.path.join(ICON_PATH, "rfh_folder_hover.svg").replace("\\","/")

#- Grobal 

ICON_DROP_DOWN_ARROW = os.path.join(ICON_PATH, "drop_down_arrow.svg").replace("\\","/")
ICON_ARROW_PREVIOUS = os.path.join(ICON_PATH, "arrow_previous.svg").replace("\\","/")
ICON_ARROW_NEXT = os.path.join(ICON_PATH, "arrow_next.svg").replace("\\","/")
ICON_MINUS = os.path.join(ICON_PATH, "minus.svg").replace("\\","/")
ICON_PLUS = os.path.join(ICON_PATH, "plus.svg").replace("\\","/")