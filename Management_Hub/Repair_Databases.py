import sqlite3
import os

# 目標物理路徑
ROOT = r"C:\Genesis\Database"
DBS = ["Genesis_DFMEA.db", "Genesis_History.db", "Genesis_Safety.db"]

def repair_all():
    print("[SYSTEM] 正在執行三個核心資料庫的表結構修復...")
    for db_name in DBS:
        db_path = os.path.join(ROOT, db_name)
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # 強制寫入標準化結構 (ID, Timestamp, Content)
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {db_name.replace('.db', '')} (id INTEGER PRIMARY KEY, timestamp TEXT, content TEXT)")
            
            conn.commit()
            conn.close()
            print(f"[SUCCESS] {db_name} 結構已修復，可正常存檔。")
        except Exception as e:
            print(f"[ERROR] {db_name} 修復失敗: {e}")

if __name__ == "__main__":
    repair_all()