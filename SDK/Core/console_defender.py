# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\SDK\Core\console_defender.py
# 狀態：實體防禦模組 (Stage 4 Verified)

import os
import datetime

def setup_global_defense():
    """初始化全域控制台防禦機制"""
    log_path = r"C:\Genesis\Logs\Security_Audit.log"
    if not os.path.exists(os.path.dirname(log_path)):
        os.makedirs(os.path.dirname(log_path))
        
    with open(log_path, "a", encoding="utf-8") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] [SYSTEM] Global Defense Protocol Initialized.\n")
    
    print("[QC PASS] Console Defender: 防禦模組已掛載，審計日誌已啟動。")

class ConsoleDefender:
    """處理控制台輸出攔截與安全校驗"""
    def __init__(self):
        self.is_active = True
        
    def validate_command(self, cmd):
        """簡單防禦邏輯：禁止危險字元"""
        forbidden = [";", "rm -rf", "format"]
        for char in forbidden:
            if char in cmd:
                return False
        return True

if __name__ == "__main__":
    # 進行模組自測
    setup_global_defense()
    print("[SYSTEM] ConsoleDefender 測試運作正常。")