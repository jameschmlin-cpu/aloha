# Category: Security
# -*- coding: utf-8 -*-
# 檔案名稱：C:\Genesis\Audit_Database_Schema.py
# 核心功能：探測資料庫內部結構，確認 DFMEA_Table 是否存在

import sqlite3
import os

def audit_database_schema():
    db_path = r"C:\Genesis\Database\Genesis_DFMEA.db"
    
    print(f"=== 正在診斷資料庫: {db_path} ===")
    
    if not os.path.exists(db_path):
        print("[嚴重告警] 資料庫檔案實體不存在！")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 查詢資料庫中所有的表格名稱
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("[結果] 資料庫內含表格：")
        if not tables:
            print("  (資料庫為空，沒有任何表格)")
        for table in tables:
            print(f"  - {table[0]}")
            
        conn.close()
        print("=== 診斷完成 ===")
        
    except Exception as e:
        print(f"[診斷失敗] 讀取資料庫錯誤: {e}")

if __name__ == "__main__":
    audit_database_schema()