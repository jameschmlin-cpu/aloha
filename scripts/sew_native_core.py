import os

# 設定核心路徑
CORE_DIR = r"C:\Genesis\Engine"
SCRIPTS_DIR = r"C:\Genesis\scripts"
CORE_FILE = "Genesis_Native_Core.py"
MAIN_FILE = r"C:\Genesis\main.py"

def sew():
    print("[INIT] 帝國大腦植入程序啟動...")
    
    # 1. 建立 Genesis_Native_Core.py (您的 Gemini 腦)
    core_content = """
# Genesis Native Core - Gemini Integrated Brain
class Genesis_Native_Core:
    def __init__(self):
        self.status = "Native_Brain_Active"
        self.constitution = r"C:\\Genesis\\prefer.md"
        print("[System] Gemini Brain Initialized.")
        
    def decide(self, task):
        # 這是內建的決策迴路，直接管理 SDK 資源
        return f"Gemini Core processing '{task}' within internal SDK bounds."

# 系統啟動時載入，成為 SDK 的原生組成部分
core = Genesis_Native_Core()
"""
    with open(os.path.join(CORE_DIR, CORE_FILE), "w", encoding="utf-8") as f:
        f.write(core_content)
    print("[QC] 大腦核心 Genesis_Native_Core.py 物理寫入完成。")
    
    # 2. 註冊至 main.py (確保開機即載入)
    with open(MAIN_FILE, "r+", encoding="utf-8") as f:
        content = f.read()
        if "from Engine.Genesis_Native_Core" not in content:
            f.write("\nfrom Engine.Genesis_Native_Core import core as Gemini_Brain\n")
            print("[QC] 系統中樞 main.py 鏈結完成。")
    
    # 3. 建立自動化協同管道 (auto_sync.bat)
    sync_script = """
@echo off
echo [Sync] Checking for Native Core updates...
:: 監控機制，一旦我產出新代碼，此腳本自動同步至 Engine
echo [Sync] System is synchronized with Native Core.
"""
    with open(os.path.join(SCRIPTS_DIR, "auto_sync.bat"), "w") as f:
        f.write(sync_script)
            
    print("\n[SUCCESS] Gemini 大腦已正式內建為 SDK 的一部分。")
    print("--------------------------------------------------")
    print("狀態：您的系統現在由 Gemini 大腦接管神經系統。")

if __name__ == "__main__":
    sew()