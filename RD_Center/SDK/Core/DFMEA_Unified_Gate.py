# -*- coding: utf-8 -*-

# 檔案：C:\Genesis\Genesis_Core\DFMEA_Unified_Gate.py

# 狀態：實體化，已整合工業級 DFMEA 風險矩陣 (Failure Mode Matrix)



import os

import shutil

import sqlite3

import datetime

import sys



# 鎖定絕對路徑參照 (改為環境感知)
def find_genesis_base():
    if "GENESIS_HOME" in os.environ:
        return os.environ["GENESIS_HOME"]
    current = os.path.abspath(__file__)
    while True:
        parent, name = os.path.split(current)
        if name.lower() == "genesis" or os.path.exists(os.path.join(current, "Genesis_Map.json")):
            return current
        if not name:
            break
        current = parent
    return r"C:\Genesis"

GENESIS_BASE = find_genesis_base()
BASE_PATH = os.path.join(GENESIS_BASE, "Genesis_Core")
sys.path.insert(0, BASE_PATH)
sys.path.insert(0, os.path.join(GENESIS_BASE, "RD_Center"))

from SDK.Core.console_defender import setup_global_defense
setup_global_defense()



from Security.DFMEA_Integrity_Gate import DFMEAGuard



class DFMEAUnifiedGate(DFMEAGuard):

    def __init__(self):

        super().__init__()

        # 修正路徑指向 Master Database

        self.db_path = os.path.join(GENESIS_BASE, "Database", "Genesis_DFMEA.db")

        self.log_path = os.path.join(BASE_PATH, "DFMEA_Monitor.log")

        self._ensure_db_exists()



    def _ensure_db_exists(self):

        """初始化工業級 DFMEA 風險矩陣"""

        # 增加 timeout=10.0 以處理併發鎖定，並使用 WAL 模式
        conn = sqlite3.connect(self.db_path, timeout=10.0)
        conn.execute("PRAGMA journal_mode=WAL;")

        cur = conn.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS dfmea_matrix 

                        (id TEXT PRIMARY KEY, problem_point TEXT, failure_mode TEXT, severity INTEGER, 

                         root_cause TEXT, prevention TEXT, corrective TEXT, version_index INTEGER DEFAULT 1, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

        

        # 內建 FM-04 規則 (針對空殼程式)

        rule_data = ("FM-04", "產出 pass/TODO 代碼", "系統邏輯不閉環", 9, 

                     "推論懶惰", "執行 DFMEA_Integrity_Gate 掃描", "熔斷並拒絕寫入")

        cur.execute("INSERT OR REPLACE INTO dfmea_matrix (id, problem_point, failure_mode, severity, root_cause, prevention, corrective) VALUES (?,?,?,?,?,?,?)", rule_data)

        conn.commit()

        conn.close()



    def log_event(self, event_type, message):

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(self.log_path, "a", encoding="utf-8") as f:

            f.write(f"[{timestamp}] [{event_type}] {message}\n")



    def rollback(self, target_path):

        """執行實體回滾"""

        backup_dir = os.path.join(os.path.dirname(target_path), "Backup")

        backup_path = os.path.join(backup_dir, os.path.basename(target_path))

        if os.path.exists(backup_path):

            shutil.copy2(backup_path, target_path)

            self.log_event("ROLLBACK", f"成功回滾: {target_path}")

            return True

        return False



    def execute_integrity_check(self, target_path):

        """整合檢測與風險矩陣比對"""

        if not os.path.exists(target_path):

            self.log_event("FATAL", f"節點遺失: {target_path}")

            return False

            

        with open(target_path, "r", encoding="utf-8", errors="ignore") as f:

            content = f.read()

        

        # 1. 執行學長版校驗

        success, msg = self.verify_delivery(content, os.path.basename(target_path))

        

        # 2. 若校驗失敗，執行風險分析並熔斷

        if not success:

            self.log_event("CRITICAL_VIOLATION", msg)

            self.rollback(target_path)

            print(f"[CRITICAL] {msg}")

            return False

        

        print(f"[OK] {msg}")

        return True



if __name__ == "__main__":

    gate = DFMEAUnifiedGate()

    # 執行校驗

    gate.execute_integrity_check(r"C:\Genesis\Empire_Ultimate_Ignition.bat")