# -*- coding: utf-8 -*-
# Genesis_AG_Autonomous_Core.py
# 任務：執行全域自主盤點，無需人工調度

import os
import sqlite3
import hashlib
import logging
import threading

logging.basicConfig(filename=r'C:\Genesis\system_monitor.log', level=logging.INFO)

class Genesis_AG_Core:
    def __init__(self):
        self.db = r"C:\Genesis\Database\Genesis_History.db"
        self.target = r"C:\Genesis"

    def execute_autonomous_scan(self):
        """自主掃描邏輯，由系統觸發，不需人工調度"""
        logging.info("[系統自檢] 自動作業閉環已觸發。")
        for root, _, files in os.walk(self.target):
            for file in files:
                path = os.path.join(root, file)
                try:
                    with open(path, "rb") as f:
                        h = hashlib.sha256(f.read()).hexdigest()
                    # 直接寫入資料庫，完成自動盤點閉環
                    conn = sqlite3.connect(self.db)
                    conn.execute("INSERT OR REPLACE INTO inventory_audit (path, hash) VALUES (?, ?)", (path, h))
                    conn.commit()
                    conn.close()
                except:
                    continue
        logging.info("[系統自檢] 自動盤點完成。")

if __name__ == "__main__":
    core = Genesis_AG_Core()
    # 自動作業執行，不需外部指令
    threading.Thread(target=core.execute_autonomous_scan, daemon=True).start()
    print("[系統狀態] 自動化作業程序已在後台運作，無需人工調度。")