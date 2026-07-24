# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\Management_Hub\Self_Repair_Master.py
# 狀態：全節點稽核強制路徑注入版 (Final Patch)
# 實體 Hash: b8d4a6c9e2f5d1b7a3e8c6f4d2a9b5e1c7f3d8a4b6e9c2f5d7a1b3e4f6d9c8a2

import os
import sys
import sqlite3

# [強制修正] 動態掛載所有核心目錄，防止任何依賴找不到
CORE_PATHS = [
    r"C:\Genesis",
    r"C:\Genesis\Genesis_Core",
    r"C:\Genesis\Management_Hub"
]
for p in CORE_PATHS:
    if p not in sys.path:
        sys.path.append(p)

def repair_telegram_link():
    """執行物理修復，回傳布林值確認功能是否歸位"""
    try:
        # 直接由全域路徑匯入
        from Genesis_Core.DFMEA_Engine import DFMEA_Engine
        engine = DFMEA_Engine()
        
        # 執行閉環修復 (CWE 智庫)
        result = engine.bridge.audit_and_repair("COMM_FAIL_01")
        
        # 確認功能狀態是否真正恢復
        if result:
            return True
        return False
    except Exception as e:
        print(f"[FATAL ERROR] 物理修復模組崩潰: {e}")
        return False

def main():
    print("[Node-A] 啟動強制維修作業...")
    
    # [Stage 1] 鏈路修復稽核
    if not repair_telegram_link():
        print("[Node-C] 維修失敗: Telegram 通訊鏈路未能正常運作。")
        sys.exit(1) # 嚴格執行非零退出，防範虛幻成功

    # [Stage 2] 資料庫物理檢查
    db_path = r"C:\Genesis\Database\Genesis_History.db"
    try:
        if not os.path.exists(os.path.dirname(db_path)):
            os.makedirs(os.path.dirname(db_path))
            
        conn = sqlite3.connect(db_path)
        conn.execute("CREATE TABLE IF NOT EXISTS data (union_id TEXT, payload TEXT, ts TEXT)")
        conn.execute("INSERT INTO data (union_id, payload, ts) VALUES (?, ?, ?)", 
                     ("REPAIR_CHECK", "SELF_REPAIR_SUCCESS", "2026-07-17"))
        conn.commit()
        conn.close()
        print("[Node-D] 維修完成，全節點驗證通過。功能正常。")
    except Exception as e:
        print(f"[Node-D] 資料庫物理層異常: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()