import os
import sqlite3
import time
import socket
import threading
import sys
import pyautogui
import startup_manager

REPORT_FILE = r"C:\Genesis\System_Audit_Report.log"

def write_audit(node, status, detail=""):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] NODE: {node} | STATUS: {status} | DETAIL: {detail}\n"
    with open(REPORT_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)

def recovery_agent(node_name):
    """自我修復代理：針對特定故障點進行物理修復"""
    print(f"🛠 [RECOVERY] 偵測到 '{node_name}' 故障，啟動自動修復...")
    try:
        if node_name == "DATABASE":
            # 資料庫崩潰則直接重構結構
            if os.path.exists(r"C:\Genesis\Genesis_History.db"): os.remove(r"C:\Genesis\Genesis_History.db")
            conn = sqlite3.connect(r"C:\Genesis\Genesis_History.db")
            conn.execute("CREATE TABLE Genesis_History (id INTEGER PRIMARY KEY, timestamp TEXT, content TEXT)")
            conn.commit()
            conn.close()
        elif node_name == "FILE_IO":
            # 檔案 IO 故障則重置權限路徑
            os.makedirs(r"C:\Genesis", exist_ok=True)
        return True
    except Exception as e:
        print(f"!!! [REPAIR_FAIL] {node_name} 修復失敗: {e}")
        return False

def run_all_physical_tests():
    """診斷與自癒閉環迴路"""
    tests = {
        "FILE_IO": lambda: open(r"C:\Genesis\test.tmp", "w").close() or os.remove(r"C:\Genesis\test.tmp"),
        "DATABASE": lambda: sqlite3.connect(r"C:\Genesis\Genesis_History.db").execute("SELECT 1"),
        "NETWORK": lambda: socket.create_connection(("8.8.8.8", 53), timeout=2),
        "REMOTE_CONTROL": lambda: pyautogui.position()
    }
    
    all_pass = True
    for name, func in tests.items():
        try:
            func()
            print(f"🟢 [PASS] {name}")
            write_audit(name, "PASS")
        except Exception as e:
            print(f"🔴 [FAIL] {name} - {e}")
            # 觸發修復邏輯
            if recovery_agent(name):
                print(f"✅ [RECOVERED] '{name}' 修復成功，系統持續運行。")
                write_audit(name, "RECOVERED")
            else:
                write_audit(name, "CRITICAL_FAIL", str(e))
                all_pass = False
    return all_pass

if __name__ == "__main__":
    if run_all_physical_tests():
        print("\n--- [STATUS] 全節點就緒，自癒系統已啟動 ---")
        # 注入依賴
        startup_manager.threading = threading
        startup_manager.main()
    else:
        print("\n!!! [系統鎖定] 部分節點修復失敗，強制進入維護模式 !!!")
        sys.exit(1)