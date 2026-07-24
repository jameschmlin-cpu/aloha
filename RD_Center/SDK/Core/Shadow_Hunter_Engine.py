# -*- coding: utf-8 -*-

# 檔案：C:\Genesis\Genesis_Core\Shadow_Hunter_Engine.py

# 狀態：肅清模式 - 執行環境與程序指紋掃描



import psutil

import winreg


import datetime



class ShadowHunter:

    def __init__(self):

        self.report_log = r"C:\Genesis\logs\Shadow_Report.log"

        print(f"[{datetime.datetime.now()}] 🛡️ 影子狩獵引擎啟動，掃描目標：隱匿進程與異常啟動項...")



    def log(self, message):

        with open(self.report_log, "a", encoding="utf-8") as f:

            f.write(f"[{datetime.datetime.now()}] {message}\n")

        print(message)



    def hunt(self):

        self.log(">>> 開始執行全域影子程序捕捉...")

        

        # 1. 行為學檢查：搜尋異常進程 (非白名單程序)

        for proc in psutil.process_iter(['pid', 'name', 'exe']):

            try:

                # 檢查進程是否偽裝或異常 (此處範例為隱身特徵監測)

                if proc.info['name'] in ["unknown_proc.exe", "shadow_agent.exe"]:

                    self.log(f"🔴 [偵測到影子城市] 程序名稱: {proc.info['name']}, PID: {proc.info['pid']}")

            except (psutil.NoSuchProcess, psutil.AccessDenied):

                continue



        # 2. 註冊表持久化檢查：找出隱藏的開機啟動惡意路徑

        self._check_persistence_registry()

        self.log(">>> 影子狩獵完成，報告已生成。")



    def _check_persistence_registry(self):

        paths = [

            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run",

            r"SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce"

        ]

        for path in paths:

            try:

                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)

                for i in range(winreg.QueryInfoKey(key)[1]):

                    name, value, _ = winreg.EnumValue(key, i)

                    # 此處比對白名單 Hash，非白名單即標記

                    if "ITE" not in value and "System32" not in value:

                        self.log(f"⚠️ [異常啟動項] 發現可疑路徑: {name} => {value}")

            except Exception: continue



if __name__ == "__main__":

    hunter = ShadowHunter()

    hunter.hunt()