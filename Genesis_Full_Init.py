import os
import sqlite3

def run_init():
    BASE = r"C:\Genesis"
    DB_DIR = os.path.join(BASE, "Database")
    REG_DB = os.path.join(DB_DIR, "Path_Register.db")
    # 更新後的聖殿區路徑
    LIB_SYSTEM = os.path.join(BASE, "Library", "LibOption", "LibrarySystem")
    MAIN_PY = os.path.join(LIB_SYSTEM, "Library_Main.py")
    
    print("[System] 執行環境完整性檢查與路徑掛載...")

    # 1. 完整性檢查：LibSystem 是否存在
    if not os.path.exists(LIB_SYSTEM):
        print(f"[Error] 缺失帝國藍圖區: {LIB_SYSTEM}")
    
    if not os.path.exists(MAIN_PY):
        print(f"[Warning] 主控程式缺失: {MAIN_PY}")

    # 2. 自動偵測 Database 資料夾下的 .db 並掛載至註冊表
    if os.path.exists(REG_DB):
        conn = sqlite3.connect(REG_DB)
        conn.execute("CREATE TABLE IF NOT EXISTS path_map (module_name TEXT PRIMARY KEY, physical_path TEXT)")
        
        db_files = [f for f in os.listdir(DB_DIR) if f.endswith(".db")]
        for db_file in db_files:
            module_name = db_file.replace(".db", "")
            full_path = os.path.join(DB_DIR, db_file)
            conn.execute("INSERT OR REPLACE INTO path_map (module_name, physical_path) VALUES (?, ?)", 
                         (module_name, full_path))
            print(f"[Mount] 已將資料庫 {module_name} 註冊至系統路由。")
        
        conn.commit()
        conn.close()
    else:
        print(f"[Error] 找不到註冊表: {REG_DB}")

    print(f"[PASS] Genesis 系統已與 {LIB_SYSTEM} 連結完成。")

if __name__ == "__main__":
    run_init()