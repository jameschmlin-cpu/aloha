# Category: Core
# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\Force_Write_Verify.py
# 核心：強制注入並驗證，確保資料庫檔案在寫入後同步提交 (Commit)

import sqlite3

def force_write_and_verify():
    db_path = r"C:\Genesis\Database\Genesis_DFMEA.db"
    target_id = "CWE-1004-TEST"
    
    print("=== 強制寫入校驗器 ===")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. 強制寫入
        cursor.execute("""
            INSERT OR REPLACE INTO dfmea_matrix (id, problem_point, severity)
            VALUES (?, ?, ?)
        """, (target_id, "Force-Inject: HttpOnly Missing", 150))
        
        # 2. 關鍵：務必提交 (Commit)
        conn.commit()
        print("[OK] 資料已成功 Commit 至資料庫。")
        
        # 3. 立即查詢驗證
        cursor.execute("SELECT severity FROM dfmea_matrix WHERE id=?", (target_id,))
        result = cursor.fetchone()
        
        if result:
            print(f"[SUCCESS] 驗證成功！讀取到 Severity: {result[0]}")
        else:
            print("[FAILURE] 寫入後仍無法讀取，資料庫路徑可能存在指向錯誤。")
            
        conn.close()
    except Exception as e:
        print(f"[例外] 寫入過程中斷: {e}")

if __name__ == "__main__":
    force_write_and_verify()