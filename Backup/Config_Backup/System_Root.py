# C:\Genesis\Config\System_Root.py
import os
# 強制固定路徑，嚴禁任何動態路徑推論
BASE_DIR = r"C:\Genesis"
MANAGEMENT_HUB = os.path.join(BASE_DIR, "Management_Hub")
SDK_LIB = os.path.join(BASE_DIR, "Library", "SDK")
BRICK_LIB = os.path.join(BASE_DIR, "Library", "SDK_Bricks")
LOG_PATH = os.path.join(BASE_DIR, "Logs", "empire_execution.log")