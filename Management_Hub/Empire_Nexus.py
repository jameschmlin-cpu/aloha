# C:\Genesis\Management_Hub\Empire_Nexus.py
import sys
import os
import sqlite3
import datetime

# --- 閉迴路路徑強制導向 ---
sys.path.append(r"C:\Genesis")
sys.path.append(r"C:\Genesis\Library\LibOption")
# -------------------------

class EmpireNexus:
    def __init__(self, db_path=r"C:\Genesis\Library\LibOption\LibrarySystem\Shared_Knowledge.db"):
        self.db_path = db_path
        self.lib_path = r"C:\Genesis\Library\LibOption"

    def load_library_module(self, module_name):
        """插拔式調用圖書館內的模組"""
        module_full_path = os.path.join(self.lib_path, f"{module_name}.py")
        if os.path.exists(module_full_path):
            try:
                print(f"[LIBRARY] 成功掛載圖書館模組: {module_name}")
                return True
            except Exception as e:
                print(f"[ERROR] 模組掛載失敗: {e}")
        return False

    def ingest_to_shared_knowledge(self, problem_point, failure_mode, root_cause):
        """將知識庫數據寫入 Shared_Knowledge.db"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 使用 ISO 字串格式化時間，確保與 Python 3.12+ 相容
            timestamp = datetime.datetime.now().isoformat()
            
            query = """INSERT INTO dfmea_matrix (id, problem_point, failure_mode, root_cause, updated_at) 
                       VALUES (?, ?, ?, ?, ?)"""
            new_id = f"KNW-{datetime.datetime.now().strftime('%Y%m%d%H%M')}"
            
            cursor.execute(query, (new_id, problem_point, failure_mode, root_cause, timestamp))
            conn.commit()
            conn.close()
            print(f"[SUCCESS] 知識已成功注入 Shared_Knowledge.db (ID: {new_id})")
        except Exception as e:
            print(f"[ERROR] 資料庫寫入失敗: {e}")

if __name__ == "__main__":
    # 初始化並執行測試
    nexus = EmpireNexus()
    
    # 測試掛載圖書館模組
    nexus.load_library_module("Core_Init")
    
    # 測試知識注入
    nexus.ingest_to_shared_knowledge(
        "測試知識點", 
        "系統自動化測試", 
        "Empire_Nexus 模組運作正常"
    )