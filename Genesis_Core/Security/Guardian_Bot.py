# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\RD_Center\Source\Option\Stage_1\Guardian_Bot.py
# 狀態：功能完全還原，嚴格執行原始邏輯

import psutil
import time
import os
from Genesis_Core.Security.Aegis_Sentinel import AegisSentinel

class GuardianEngine:
    def __init__(self):
        self.root_path = r"C:\Genesis"
        self.log_path = os.path.join(self.root_path, "Genesis_Core", "logs")
        if not os.path.exists(self.log_path): 
            os.makedirs(self.log_path)
        
        # 實例化 Aegis 哨兵
        self.aegis = AegisSentinel()
        
        # 帝國白名單
        self.trusted_apps = ["python.exe", "ollama.exe", "telegram", "hermes_kernel"]

    def log_event(self, message):
        # 原始稽核記錄邏輯：無任何變動
        try:
            with open(os.path.join(self.log_path, "Defense.log"), "a") as f:
                f.write(f"{time.ctime()} | {message}\n")
        except: 
            pass

    def scan_and_remediate(self):
        # 原始行為監控邏輯：完全保留原先設定
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            try:
                proc_name = proc.info['name'].lower()
                if any(t in proc_name for t in self.trusted_apps):
                    continue
                
                if proc.cpu_percent(interval=0.1) > 90:
                    msg = f"!!! [行為異常] PID: {proc.pid} ({proc_name}) 佔用過高 CPU"
                    self.log_event(msg)
                    proc.suspend()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

    def start_resident(self):
        """駐留介面，由 SDK 呼叫"""
        print(">>> [保全系統] 已成功駐留記憶體。")

    def run(self):
        print(">>> [系統已啟動] 帝國安全保全已更新，白名單防護已導通...")
        while True:
            self.scan_and_remediate()
            # 原始硬體健康檢查
            self.aegis.check_physical_integrity()
            time.sleep(30) 

def start_resident():
    bot = GuardianEngine()
    bot.start_resident()
    # 執行緒掛鉤邏輯保留
    bot.run()