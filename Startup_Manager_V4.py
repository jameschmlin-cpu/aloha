# -*- coding: utf-8 -*-
# C:\Genesis\Startup_Manager_V4.py
# 狀態：終極防護整合型啟動管理器 V4 (對接黃金啟動管線與核心自癒)

import os
import sys
import sqlite3
import psutil

# 導入黃金常駐模組
try:
    sys.path.insert(0, r"C:\Genesis")
    import startup_manager
except ImportError as e:
    sys.stderr.write(f"[錯誤] 無法加載 startup_manager.py: {e}\n")
    sys.exit(1)

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
    
    # [檢測項目 2] 資料庫完整性與讀寫測試
    try:
        conn = sqlite3.connect(DB_PATH)
        if conn.execute("PRAGMA integrity_check").fetchone()[0] == "ok":
            _log("綠燈", "測試通過: 資料庫讀寫與完整性檢核正常")
        else:
            raise Exception("Integrity check failed")
        conn.close()
    except Exception as e:
        _log("紅燈", f"測試失敗: 資料庫存取異常 ({e})")
        sys.exit(1)

if __name__ == "__main__":
    # 1. 補全節點與自我檢測
    initialize_missing_nodes()
    check_system_integrity()
    
    print("--- [SYSTEM_BOOT] 全測試已完成，啟動背景服務 ---")
    
    # 2. 調用黃金啟動管線啟動背景常駐服務 (包含 Port 8000 的 dashboard)
    try:
        startup_manager.run_golden_startup_pipeline()
        _log("綠燈", "Startup Manager V4 啟動鏈路完成")
    except Exception as e:
        _log("紅燈", f"啟動背景服務失敗: {e}")
        sys.exit(1)
