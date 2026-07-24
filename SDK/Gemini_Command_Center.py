# -*- coding: utf-8 -*-
# C:\Genesis\SDK\Gemini_Command_Center.py
# 工業級控制中心：全通道狀態回顯與 SDK 四階段校驗

import os
import json
import subprocess
import sys
from pre_flight_check import IndustrialPreFlight

class CommandCenter:
    def __init__(self):
        self.manifest_path = r"C:\Genesis\SDK\block_manifest.json"
        self.checker = IndustrialPreFlight()
        print("[初始化] 命令中心已啟動，已掛載預判守門員。")

    def load_manifest(self):
        if not os.path.exists(self.manifest_path):
            print(f"[Fatal] 找不到積木清單: {self.manifest_path}")
            sys.exit(1)
        with open(self.manifest_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def execute_command(self, target_script):
        """執行狀況全顯式調度器"""
        print(f"[Node A] 正在索引積木: {target_script}")
        
        # 1. 查找積木
        manifest = self.load_manifest()
        target_brick = next((item for item in manifest if target_script in item['path']), None)
        
        if not target_brick:
            print(f"[Node B] 錯誤：在 17,490 個積木中找不到 {target_script}")
            return

        # 2. Stage 1-2: 預判執行 (強制輸出風險指標)
        print("[Node B] 正在進行預判校驗...")
        if not self.checker.run_pre_flight(target_brick['path']):
            print("[Node C] 熔斷機制觸發：安全性驗證失敗，任務終止！")
            return

        # 3. Stage 3-4: 物理調用與實時回顯
        print(f"[Node C] 安全性校驗通過，開始執行: {os.path.basename(target_brick['path'])}")
        try:
            # 捕獲並實時顯示子進程輸出
            proc = subprocess.Popen(["python", target_brick['path']], 
                                    stdout=subprocess.PIPE, 
                                    stderr=subprocess.PIPE, 
                                    text=True)
            stdout, stderr = proc.communicate()
            
            if stdout: print(f"[輸出紀錄]\n{stdout}")
            if stderr: print(f"[錯誤紀錄]\n{stderr}")
            
            print(f"[Node D] 任務執行結束，返回碼: {proc.returncode}")
        except Exception as e:
            print(f"[Node D] 執行過程中發生物理異常: {e}")

if __name__ == "__main__":
    center = CommandCenter()
    # 測試執行：請在下方輸入您要測試的積木名稱
    # 範例：center.execute_command("test_job.py")
    print("[待命] 請輸入指令進行組裝測試...")