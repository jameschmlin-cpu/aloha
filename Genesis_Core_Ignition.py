import os
import sys
import subprocess

# --- [Stage 1] 全環境自檢與依賴部署 ---
def check_environment():
    required_packages = ['pyautogui']
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"[系統] 偵測到缺少依賴: {package}，正在安裝...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            except Exception as e:
                print(f"[致命錯誤] 無法安裝套件 {package}: {e}")
                return False
    return True

if check_environment():
    import sqlite3
    import pyautogui
    from datetime import datetime

    # --- [Stage 2] 帝國核心架構定義 ---
    BASE_DIR = r"C:\Genesis"
    DB_PATH = os.path.join(BASE_DIR, "Database", "Genesis_History.db")
    TEST_DIR = os.path.join(BASE_DIR, "Test_Deployment")
    LOG_FILE = os.path.join(TEST_DIR, "Full_Ignition.log")

    class GenesisCore:
        def __init__(self):
            pyautogui.FAILSAFE = True
            os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
            os.makedirs(TEST_DIR, exist_ok=True)

        def ignite(self):
            try:
                # 記憶層同步
                conn = sqlite3.connect(DB_PATH)
                conn.execute('CREATE TABLE IF NOT EXISTS memory_core (key TEXT PRIMARY KEY, value TEXT, timestamp TEXT)')
                conn.execute("REPLACE INTO memory_core VALUES (?, ?, ?)", 
                             ("Ignition_Status", "Full_Capacity_Active", datetime.now().isoformat()))
                conn.commit()
                conn.close()
                print("[記憶層] 記憶庫已同步。")

                # 工匠手腳與視覺驗證
                pyautogui.moveTo(400, 400, duration=0.5)
                pyautogui.click()
                print("[工匠層] 視覺手腳測試：滑鼠已移動並點擊。")

                # 檔案寫入測試
                with open(LOG_FILE, "w", encoding="utf-8") as f:
                    f.write(f"Full_Ignition_Success: {datetime.now().isoformat()}")
                print(f"[檔案層] 測試檔案已寫入至: {LOG_FILE}")
                
                return True
            except Exception as e:
                print(f"[執行異常] 帝國點火失敗: {e}")
                return False

    # --- [Stage 3] 主執行流程 ---
    if __name__ == "__main__":
        core = GenesisCore()
        if core.ignite():
            print("====================================")
            print("帝國總控核心：點火成功，全功能連動完成。")
            print("====================================")
        else:
            print("點火過程出現異常，請檢查上述錯誤訊息。")
else:
    print("[系統] 環境檢查未通過，點火中止。")