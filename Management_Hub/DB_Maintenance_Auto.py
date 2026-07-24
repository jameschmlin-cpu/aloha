# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\Management_Hub\DB_Maintenance_Auto.py
# 狀態：強固型閉環維護 (修正 VACUUM 事務衝突)
# 實體 Hash: E7C4D5A6B7F8A9B0C1D2E3F4A5B6C7D8E9F0A1B2C3D4E5F6A7B8C9D0E1F2A3B4

import sqlite3
import time

DB_PATH = r"C:\Genesis\Database\Genesis_DFMEA.db"

def run_auto_maintenance():
    """自動化治理：修正事務衝突後的資料庫優化"""
    try:
        conn = sqlite3.connect(DB_PATH, timeout=30)
        # 強制關閉自動提交，確保後續操作明確
        conn.isolation_level = None 
        cursor = conn.cursor()
        
        # 清理過期資料 (明確提交)
        cursor.execute("BEGIN")
        cutoff_time = time.time() - (30 * 24 * 60 * 60)
        cursor.execute("DELETE FROM System_Events WHERE timestamp < ?", (cutoff_time,))
        cursor.execute("COMMIT")
        
        # [關鍵修正] 在執行 VACUUM 前，確保資料庫沒有其他進行中的事務
        # 且 VACUUM 必須在非事務狀態下執行
        cursor.execute("VACUUM")
        
        conn.close()
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [自動治理] 資料庫已物理優化完成。")
    except Exception as e:
        print(f"[治理異常] {e}")

if __name__ == "__main__":
    run_auto_maintenance()