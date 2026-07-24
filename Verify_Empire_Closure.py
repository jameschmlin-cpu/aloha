# Category: Security
# -*- coding: utf-8 -*-
import sqlite3

def verify_closure():
    db_path = r"C:\Genesis\Database\Genesis_DFMEA.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 查詢是否有任意積木已註冊，且風險權重正確
    cursor.execute("SELECT COUNT(*) FROM dfmea_matrix WHERE severity = 50")
    count = cursor.fetchone()[0]
    
    print("=== 帝國閉環驗證 ===")
    if count > 1000:
        print(f"[OK] 閉環確認：已偵測到 {count} 個受控模組，系統已完全封裝。")
        print("[指令] 隨時可以啟動 Empire_Command_Center.py 進行實戰。")
    else:
        print(f"[警告] 閉鎖異常：僅偵測到 {count} 個模組，請檢查歸位過程。")
        
    conn.close()

if __name__ == "__main__":
    verify_closure()