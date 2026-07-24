# -*- coding: utf-8 -*-

# 檔案：C:\Genesis\Genesis_Core\System_Bootloader.py

import sys

import subprocess




def boot():

    print("[帝國啟動] 正在掛載安全衛士與核心調度器...")

    # 1. 啟動保全監控 (Guardian_Bot 駐留)

    subprocess.Popen([sys.executable, r"C:\Genesis\Genesis_Core\Security\Guardian_Bot.py"])

    

    # 2. 初始化 DFMEA 邏輯閘

    from DFMEA_Unified_Gate import DFMEAUnifiedGate

    gate = DFMEAUnifiedGate()

    

    # 3. 啟動總管核心

    print("✅ [啟動完成] 帝國系統進入自主防禦狀態。")



if __name__ == "__main__":

    boot()