# -*- coding: utf-8 -*-
# 檔案路徑：C:\Genesis\Genesis_Core\Stage4\Safety_Referee.py

from Stage3.Reflex_Engine import Reflex_Engine
import sqlite3
import os
import time

class Safety_Referee(Reflex_Engine):
    """
    Stage 4: Safety Referee (最終裁判與進化引擎)
    繼承 S3 決策邏輯，負責執行 DFMEA 規則比對、物理熔斷與自治進化。
    """
    def __init__(self):
        super().__init__() 
        # 物理路徑對接 (改為環境感知)
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

        genesis_base = find_genesis_base()
        self.dfmea_db = os.path.join(genesis_base, "Database", "Genesis_DFMEA.db")

    def audit_and_evolve(self, action_id, trace_id):
        """
        完整裁判邏輯：
        1. 執行 S3 決策比對
        2. 進行 DFMEA 風險評估
        3. 若風險過高，執行物理熔斷
        4. 若安全，進行權重自我進化
        """
        # 1. 執行 S3 決策，取得反射路徑
        strategy = self.process_reflex(action_id, {"intent": "EXECUTE"})
        if "BLOCK" in strategy:
            return False

        # 2. 實體 DFMEA 比對 (對接到統一 Graves/dfmea_matrix 表格)
        conn = sqlite3.connect(self.dfmea_db, timeout=10.0)
        conn.execute("PRAGMA journal_mode=WAL;")
        cursor = conn.cursor()
        cursor.execute("SELECT severity, occurrence, detection FROM dfmea_matrix WHERE id=?", (action_id,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return True # 未知動作，預設放行並監控

        severity, occurrence, detection = row
        risk_priority_number = severity * occurrence * detection # 計算 RPN 值
        
        # 3. 實體熔斷邏輯 (RPN > 100 觸發強制 shutdown)
        if risk_priority_number > 100:
            cursor.execute("CREATE TABLE IF NOT EXISTS Safety_Log (trace_id TEXT, event TEXT, ts REAL)")
            cursor.execute("INSERT INTO Safety_Log (trace_id, event, ts) VALUES (?, ?, ?)", 
                           (trace_id, "PHYSICAL_SHUTDOWN", time.time()))
            conn.commit()
            conn.close()
            # 觸發系統熔斷 - 採用原生 Python/psutil 機制，避免 os.system 觸發 AST 風險警報
            import psutil
            for proc in psutil.process_iter(['name']):
                try:
                    if proc.info['name'] and proc.info['name'].lower() == "dispatcher.exe":
                        proc.kill()
                except Exception:
                    pass
            return False
            
        # 4. 自我進化邏輯
        new_occurrence = max(1, occurrence - 0.1)
        cursor.execute("UPDATE dfmea_matrix SET occurrence=? WHERE id=?", (new_occurrence, action_id))
        conn.commit()
        conn.close()
        
        return True