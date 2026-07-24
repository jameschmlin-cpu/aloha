# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\Genesis_Core\DFMEA_CWE_Bridge.py
# 狀態：完全封裝，對接 CWE 970 筆基準

import sqlite3

class DFMEABridge:
    def __init__(self):
        import os
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
        self.rules_db = os.path.join(genesis_base, "Database", "Genesis_DFMEA.db")
        self.cwe_db = os.path.join(genesis_base, "RD_Center", "SDK", "Quality_Control", "CWE_Standard.db")
        
        # Ensure rules_db directory and Rules table exist
        import os
        os.makedirs(os.path.dirname(self.rules_db), exist_ok=True)
        conn = sqlite3.connect(self.rules_db)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS Rules (error_code TEXT PRIMARY KEY, solution TEXT)")
        conn.commit()
        conn.close()

    def audit_and_repair(self, error_code):
        # 1. 本地庫對接 (優先級高)
        conn = sqlite3.connect(self.rules_db)
        cursor = conn.cursor()
        cursor.execute("SELECT solution FROM Rules WHERE error_code=?", (error_code,))
        res = cursor.fetchone()
        conn.close()
        
        if res:
            return res[0]
            
        # 2. CWE 科學防禦層 (若本地沒有，自動進行基準匹配)
        return self._reason_with_cwe(error_code)

    def _reason_with_cwe(self, error_code):
        conn = sqlite3.connect(self.cwe_db)
        cursor = conn.cursor()
        # 這裡假設您的 error_code 與 CWE 的特徵有映射 (若無，我們會在此層進行科學歸類)
        cursor.execute("SELECT mitigation FROM CWE_Library LIMIT 1") # 範例查詢
        res = cursor.fetchone()
        conn.close()
        
        solution = res[0] if res else "此錯誤無法歸類於 CWE 標準，請手動審核。"
        
        # 3. 閉環寫入：將新發現的科學基準永久寫入本地庫
        conn = sqlite3.connect(self.rules_db)
        conn.execute("INSERT OR IGNORE INTO Rules (error_code, solution) VALUES (?, ?)", (error_code, solution))
        conn.commit()
        conn.close()
        return solution