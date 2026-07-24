# C:\Genesis\Engine\Database_Init.py (執行一次即可建立 Path_Database.db)
import sqlite3

def init_db():
    db_path = r"C:\Genesis\Management_Hub\Path_Database.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 建立核心路徑對照表
    cursor.execute('''CREATE TABLE IF NOT EXISTS path_map 
                      (module_name TEXT PRIMARY KEY, physical_path TEXT)''')
    
    # 寫入預設路徑對照
    paths = [
        ('Base_Template', r'C:\Genesis\Base_Template.py'),
        ('Orchestrator', r'C:\Genesis\Engine\Orchestrator.py')
    ]
    cursor.executemany('INSERT OR REPLACE INTO path_map VALUES (?, ?)', paths)
    
    conn.commit()
    conn.close()
    print(f"[資料庫] Path_Database.db 已部署於 {db_path}")

if __name__ == "__main__":
    init_db()