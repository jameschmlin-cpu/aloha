# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\Management_Hub\DB_Maintenance.py
# 狀態：物理清理模組 (符合憲法資源優先級條款)

import sqlite3
import time

DB_PATH = r"C:\Genesis\Database\Genesis_DFMEA.db"

def vacuum_database():
    """執行資料庫空間重組與歷史日誌清理"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 刪除 30 天前的過期診斷日誌
        cutoff_time = time.time() - (30 * 86400)
        cursor.execute("DELETE FROM System_Events WHERE timestamp < ?", (cutoff_time,))
        
        # 重組空間 (Vacuum)
        cursor.execute("VACUUM")
        conn.commit()
        conn.close()
        print("[物理清理] 垃圾數據已清除，資料庫空間已重組。")
    except Exception as e:
        print(f"[清理失敗] {e}")

if __name__ == "__main__":
    vacuum_database()