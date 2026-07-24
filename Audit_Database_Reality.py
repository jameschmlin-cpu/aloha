# Category: Security
# -*- coding: utf-8 -*-
import sqlite3
import os

def audit_reality():
    db_path = r"C:\Genesis\Database\Genesis_DFMEA.db"
    target_id = "CWE-1004-TEST"
    
    print("=== 實體資料庫讀寫合一檢查 ===")
    print(f"[檢查] 目標路徑: {db_path}")
    
    if not os.path.exists(db_path):
        print("[異常] 資料庫檔案不存在")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 直接查詢那筆測試資料
    cursor.execute("SELECT id, severity FROM dfmea_matrix WHERE id=?", (target_id,))
    row = cursor.fetchone()
    
    if row:
        print(f"[OK] 找到測試資料! ID: {row[0]}, Severity: {row[1]}")
    else:
        # 如果這裡撈不到，說明測試資料根本沒寫進這一個檔案
        print(f"[錯誤] 資料庫中找不到測試 ID: {target_id}")
        
    conn.close()

if __name__ == "__main__":
    audit_reality()