import sqlite3

DB_PATH = r"C:\Genesis\Database\Genesis_History.db"

def verify_db():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 1. 自動偵測資料庫內的正確表名
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if not tables:
            print("[VERIFY_FAIL] 資料庫內無任何表格")
            return
        
        target_table = tables[0][0] # 自動對接第一個存在的表
        print(f"[SYSTEM] 自動對接表名: {target_table}")
        
        # 2. 讀取該表的最新紀錄
        cursor.execute(f"SELECT timestamp, content FROM {target_table} ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            print("[VERIFY_SUCCESS]")
            print(f"Timestamp: {row[0]}")
            print(f"Content: {row[1]}")
        else:
            print("[VERIFY_FAIL] 表格內無資料")
            
    except Exception as e:
        print(f"[ERROR] 讀取失敗: {e}")

if __name__ == "__main__":
    verify_db()