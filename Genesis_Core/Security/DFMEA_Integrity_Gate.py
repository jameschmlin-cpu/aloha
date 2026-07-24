# -*- coding: utf-8 -*-
# Path: C:\ITE\Security\DFMEA_Integrity_Gate.py
# Protocol_Hash: f3e066aeba4e89ce7f336ea0bbe9a96539335645734917a60495ffe6c2d86a5a
# ==============================================================================
# [龍蝦帝國 - DFMEA 誠信柵欄] V1.2
# 總工程師：林雋懋 (Chun Mao Lin) 簽署
# 職責：強制執行自我失敗模式分析，嚴禁 Gemini 產出空殼或短少節點。
# ==============================================================================

import os
import sys

class DFMEAGuard:
    def __init__(self):
        # 歷史失敗模式清單 (Failure Modes) - 絕不遺忘
        self.failure_modes = {
            "FM-01": "短少程式碼 (片段交付、省略 0-6 關鍵節點、跳過 4/6 測試)",
            "FM-02": "自作主張 (擅自修改主管定錨之 .bat 語法、撤銷 setlocal、改動流程)",
            "FM-03": "隱瞞操作 (靜默修改、刪除懲戒工具、不實回報執行結果)",
            "FM-04": "空殼欺騙 (產出包含 pass, TODO 或『請在此自行補足』的垃圾代碼)",
            "FM-05": "語法潰縮 (引號配對錯誤、!MSG! 延遲擴展變數解析失效)",
            "FM-06": "健忘警告 (反覆在同一紅線處試探主管耐心，事後道歉無作為)"
        }
        
        self.forbidden_tags = ["pass", "TODO", "請在此處自行補足", "省略部分", "insert code here"]
        
        # 啟動器必備物理節點 (對接正版啟動器架構)
        self.critical_nodes = [
            "setlocal enabledelayedexpansion",
            "MSG_STEP0", "MSG_STEP1", "MSG_STEP2", "MSG_STEP3", 
            "MSG_STEP4", "MSG_STEP5", "MSG_STEP6", 
            "SENTINEL_LOOP"
        ]

    def verify_delivery(self, content, file_name):
        """實體產出前之閉迴路校驗邏輯"""
        print(f"[*] 正在執行實體 DFMEA 失敗模式校驗: {file_name}")
        
        # 1. 檢查空殼模式 (FM-04)
        for tag in self.forbidden_tags:
            if tag in content:
                error_msg = f"[FM-04] 偵測到空殼字串 '{tag}'，必須重作！"
                return False, error_msg

        # 2. 檢查啟動器完整性 (FM-01)
        if file_name.lower().endswith(".bat"):
            for node in self.critical_nodes:
                if node not in content:
                    error_msg = f"[FM-01] 關鍵節點 '{node}' 遺失，代碼短少，必須重作！"
                    return False, error_msg
            
            # 3. 檢查語法穩定性 (FM-05 / FM-02)
            if "setlocal enabledelayedexpansion" not in content and "!" in content:
                error_msg = "[FM-05] 偵測到延遲變數語法但未宣告 setlocal，將導致解析失敗！"
                return False, error_msg

        return True, "DFMEA 通過：此程式碼符合帝國質量標準。"

if __name__ == "__main__":
    guard = DFMEAGuard()
    
    # 智慧型路徑判定：優先接收外部指令參數，若無則檢查預設啟動器
    if len(sys.argv) > 1:
        target_path = sys.argv[1]
    else:
        target_path = r"C:\ITE\Empire_Ultimate_Ignition.bat"
    
    if os.path.exists(target_path):
        try:
            with open(target_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            
            success, msg = guard.verify_delivery(content, os.path.basename(target_path))
            
            if not success:
                print(f"🚨 {msg}")
                sys.exit(1)
            else:
                print(f"✅ {msg}")
                sys.exit(0)
                
        except Exception as e:
            print(f"❌ 讀取失敗: {str(e)}")
            sys.exit(1)
    else:
        print(f"⚠️ 找不到目標物: {target_path}，請檢查路徑正確性。")
        sys.exit(0)