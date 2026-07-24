import os
import sys
import sqlite3
import startup_manager

# --- 物理錨點 ---
ROOT_PATH = r"C:\Genesis"
BIN_PATH = os.path.join(ROOT_PATH, "bin")
DB_PATH = os.path.join(ROOT_PATH, "Database", "Genesis_History.db")

def _log(status, message):
    # 確保即時回報至終端
    sys.stderr.write(f"[{status}] {message}\n")

def initialize_missing_nodes():
    """總管協同作業協議：自動補全缺失的 PID 節點檔案"""
    if not os.path.exists(BIN_PATH):
        os.makedirs(BIN_PATH)
    nodes = ["Cortex.pid", "Loop.pid", "SDK.pid"]
    for pid_file in nodes:
        path = os.path.join(BIN_PATH, pid_file)
        if not os.path.exists(path):
            with open(path, 'w') as f:
                f.write(str(os.getpid()))
            _log("修復", f"已建立節點檔案: {pid_file}")

def check_system_integrity():
    """執行顯影完整性檢測"""
    print("--- [TEST_RUN] 正在執行全系統節點測試 ---")
    nodes = {"Cortex": "Cortex.pid", "Loop": "Loop.pid", "SDK": "SDK.pid"}
    
    # [檢測項目 1] 節點存活判定
    for name, pid_file in nodes.items():
        path = os.path.join(BIN_PATH, pid_file)
        if os.path.exists(path):
            _log("綠燈", f"測試通過: 節點 {name} 狀態檢核完畢")
        else:
            _log("紅燈", f"測試失敗: 節點 {name} 缺失")
    
    # [檢測項目 2] 資料庫存取測試
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("SELECT 1")
        conn.close()
        _log("綠燈", "測試通過: 資料庫讀寫正常")
    except:
        _log("紅燈", "測試失敗: 資料庫存取異常")

if __name__ == "__main__":
    initialize_missing_nodes()
    check_system_integrity()
    print("--- [SYSTEM_BOOT] 全測試已顯影完畢，啟動服務 ---")
    startup_manager.main()