# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\DFMEA_Update_Script.py
# 狀態：風險矩陣完整性強制修復 (Stage 4 Compliance - FM-04 Full Integrity)
# 實體 Hash: 0xGEN-DFMEA-FIX-20260712-Z2

import sqlite3
import os
import sys

def update_dfmea_database_full():
    """強制將 FM-04 工業級風險規則完整寫入核心資料庫"""
    db_path = r"C:\Genesis\Database\Genesis_DFMEA.db"
    if not os.path.exists(db_path):
        return False, "資料庫路徑遺失，系統拒絕寫入。"
    
    try:
        conn = sqlite3.connect(db_path, timeout=10.0)
        conn.execute("PRAGMA journal_mode=WAL;")
        cur = conn.cursor()
        
        # [完整閉環寫入]：定義 FM-04 規則所有七個維度
        # 嚴重度 (severity=9) 觸發最高級熔斷
        full_rule_data = (
            "FM-04",                                   # id
            "Genesis_AG_Core 閉環完整性",               # problem_point
            "邏輯閉環失效 (Logic Gap)",                 # failure_mode
            9,                                         # severity
            "編寫 Doctor_Prime_2.py 時，未將「DFMEA 工業級風險矩陣」之核心閉環邏輯（Failure Mode Matrix Control）實體寫入執行路徑",           # root_cause
            "執行沙盒測試 強制掃描",        # prevention
            "今後所有產出的程式碼，交付前必須先產出系統分析與「邏輯拓撲圖」供主管審核"                # corrective
        )
        
        cur.execute('''INSERT OR REPLACE INTO dfmea_matrix 
                       (id, problem_point, failure_mode, severity, root_cause, prevention, corrective) 
                       VALUES (?,?,?,?,?,?,?)''', full_rule_data)
        
        conn.commit()
        conn.close()
        return True, "規則已完全寫入矩陣。"
    except Exception as e:
        return False, str(e)

if __name__ == "__main__":
    success, msg = update_dfmea_database_full()
    if success:
        print(f"[SUCCESS] {msg}")
        sys.exit(0)
    else:
        print(f"[FATAL] 寫入失敗: {msg}")
        sys.exit(1)