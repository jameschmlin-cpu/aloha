# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\Database_Locater.py
import os
import sqlite3

def locate_and_repair_databases():
    # 定義目標路徑與資料庫列表
    target_dir = r"C:\Genesis\Genesis_Core\Data"
    databases = {
        "Unified_Empire_Memory": os.path.join(target_dir, "Unified_Empire_Memory.db"),
        "System_Core": os.path.join(target_dir, "System_Core.db"),
        "path_master": os.path.join(target_dir, "path_master.db")
    }

    if not os.path.exists(target_dir):
        print(f"[系統診斷] 目標目錄不存在，正在建立: {target_dir}")
        os.makedirs(target_dir)

    print("[開始搜尋] 正在定位與驗證資料庫...")

    for name, path in databases.items():
        if os.path.exists(path):
            try:
                # 簡單測試連線，確認檔案未損毀
                conn = sqlite3.connect(path)
                conn.execute("SELECT 1")
                conn.close()
                print(f"[正常] 找到資料庫: {name} | 位置: {path}")
            except Exception as e:
                print(f"[警告] 檔案損毀或無法讀取: {name} - {e}")
                # 若損毀，移除後準備重建
                os.remove(path)
                recreate_db(name, path)
        else:
            print(f"[遺失] 找不到資料庫: {name}，正在強制重建...")
            recreate_db(name, path)

def recreate_db(name, path):
    """根據帝國架構重建資料庫"""
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    
    if name == "Unified_Empire_Memory":
        cursor.execute("CREATE TABLE IF NOT EXISTS State_Table (id INTEGER PRIMARY KEY, service_name TEXT, status TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS Log_Table (id INTEGER PRIMARY KEY, timestamp DATETIME, data TEXT)")
    elif name == "System_Core":
        cursor.execute("CREATE TABLE IF NOT EXISTS paths (key TEXT PRIMARY KEY, path TEXT)")
    elif name == "path_master":
        cursor.execute("CREATE TABLE IF NOT EXISTS PathRegistry (key TEXT PRIMARY KEY, physical_path TEXT)")
        paths = [('BASE', r'C:\Genesis\Genesis_Core'), ('LOGS', r'C:\Genesis\Genesis_Core\logs')]
        cursor.executemany('INSERT OR REPLACE INTO PathRegistry VALUES (?,?)', paths)
        
    conn.commit()
    conn.close()
    print(f"[修復成功] {name} 已在 {path} 重建完畢。")

if __name__ == "__main__":
    locate_and_repair_databases()