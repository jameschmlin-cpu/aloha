# -*- coding: utf-8 -*-
import datetime
import os

class Logger:
    '''SDK 核心：負責全系統實體日誌與過程透明化'''
    def __init__(self, log_dir=r"C:\Genesis\Logs"):
        self.log_dir = log_dir
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def write_log(self, level, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}\n"
        
        # 同步輸出至終端機 (解決主管苦等問題)
        print(f"🛰️  [實時監控] {log_entry.strip()}")
        
        # 寫入物理檔案
        log_file = os.path.join(self.log_dir, f"system_{datetime.date.today()}.log")
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)

# 實體 Hash 校驗預估: 8e4a... (寫入後請回報)