# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\Management_Hub\Doctor.py
# 狀態：最終校準版 (封堵所有邏輯斷層與前任漏洞)

import sys
import os

# [物理對齊] 強制導通所有 Genesis 核心組件
sys.path.insert(0, os.path.abspath(r"C:\Genesis"))
sys.path.insert(0, os.path.abspath(r"C:\Genesis\RD_Center"))

try:
    from SDK.Core_Gateway import Core_Gateway
    from SDK.Registry_Manager import Registry_Manager
    from SDK.Backup_Engine import Backup_Engine
    from SDK.DFMEA_Monitor import DFMEA_Monitor
    from SDK.Guardian_Bot import Guardian_Bot
    # 繞過 20class 命名漏洞
    mod = __import__("20class.Lifecycle_Hook", fromlist=["Lifecycle_Hook"])
    Lifecycle_Hook = mod.Lifecycle_Hook
except Exception as e:
    sys.stderr.write(f"[FATAL] 實體匯入鏈斷裂: {e}\n")
    sys.exit(1)

class Doctor(Core_Gateway):
    def __init__(self):
        super().__init__()
        # 實體初始化所有守護組件
        self.registry = Registry_Manager()
        self.hook = Lifecycle_Hook()
        self.backup = Backup_Engine()
        self.dfmea = DFMEA_Monitor()
        self.bot = Guardian_Bot()

    def run_guard(self):
        """[閉環調度] 執行全盤診斷與防禦"""
        print("[SYSTEM] 醫生程序啟動，執行全盤診斷...")

        # 1. DFMEA 與 防禦矩陣偵測 (補齊缺失功能)
        if not self.bot.verify_defense_matrix():
            print("[ALERT] 偵測到失效模式，啟動緊急自癒...")
            
            # 2. 備份機制 (補齊前朝缺失)
            self.backup.create_checkpoint()
            
            # 3. 實體 Registry 修復
            self.registry.regenerate_minimalist_registry()
            
            # 4. 閉環稽核
            if self.hook.verify_system_integrity().get('status') == "EMPIRE_BOOT_SUCCESS":
                print("[SUCCESS] 診斷修復成功。")
                sys.exit(0)
            else:
                print("[FATAL] 修復後稽核失敗，請立即介入。")
                sys.exit(1)
        else:
            print("[SUCCESS] 系統穩定，Guardian_Bot 防禦矩陣正常。")
            sys.exit(0)

if __name__ == "__main__":
    doc = Doctor()
    doc.run_guard()