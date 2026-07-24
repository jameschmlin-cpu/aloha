# C:\Genesis\Engine\Database_Migrator.py
import os
import shutil

def migrate_database():
    old_path = r"C:\Genesis\Management_Hub\Path_Database.db"
    new_dir = r"C:\Genesis\Database"
    new_path = os.path.join(new_dir, "Path_Database.db")
    
    # 確保資料庫目錄存在
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
        print(f"[系統] 建立資料庫統一目錄: {new_dir}")
        
    # 執行遷移
    if os.path.exists(old_path):
        shutil.move(old_path, new_path)
        print(f"[系統] 資料庫已遷移至: {new_path}")
    else:
        print(f"[警告] 原始位置無資料庫檔案，直接初始化新檔於: {new_path}")
        
    return new_path

if __name__ == "__main__":
    migrate_database()