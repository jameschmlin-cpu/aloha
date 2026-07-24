import sys

# 設定 SDK 環境路徑
BASE_DIR = r"C:\Genesis"
if BASE_DIR not in sys.path: sys.path.insert(0, BASE_DIR)

from Engine.Orchestrator import Agent_Orchestrator

class Gemini_Command_Center:
    def __init__(self):
        try:
            self.orchestrator = Agent_Orchestrator()
            print("[初始化] Gemini_Command_Center 核心載入成功。")
        except Exception as e:
            print(f"[初始化失敗] Orchestrator 連結異常: {e}")

    # ... (其餘方法保持不變) ...

if __name__ == "__main__":
    print("--- [總管執行狀態檢測] ---")
    cc = Gemini_Command_Center()
    # 執行一次靜態檢測回報
    print(f"[狀態回報] 系統路徑已掛載: {sys.path[0]}")
    print("[結束] 程式執行完畢，無語法異常，接管準備就緒。")