# -*- coding: utf-8 -*-
import os
import sqlite3
import argparse
from engine_task import Stage4Engine

class Empire_Command_Center:
    def __init__(self):
        self.config = {"dfmea_db": r"C:\Genesis\Database\Genesis_DFMEA.db"}
        self.ai_engine = Stage4Engine()
        self.verify_integrity()

    def verify_integrity(self):
        if not os.path.exists(self.config["dfmea_db"]):
            raise FileNotFoundError(f"[嚴重告警] 資料庫缺失: {self.config['dfmea_db']}")
        print("[成功] 指揮中心已成功與 SDK 閉鎖核心對接。")

    def execute_task(self, task_id):
        conn = sqlite3.connect(self.config["dfmea_db"])
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT severity FROM dfmea_matrix WHERE id=? LIMIT 1", (task_id,))
            row = cursor.fetchone()
            if row and row[0] > 100:
                print(f"[熔斷] 任務 {task_id} 風險過高，執行物理阻斷。")
                return False
            return True
        finally:
            conn.close()

    def execute_ai_task(self, task_id, prompt_text):
        print(f"\n=== [Stage 4] 啟動 AI 橋接任務: {task_id} ===")
        if not self.execute_task(task_id):
            return
        
        result = self.ai_engine.execute(prompt_text)
        hash_val = self.ai_engine.verify_and_log(task_id, result)
        print(f"[AI 回報]:\n{result}\n[閉環歸檔] Hash: {hash_val[:16]}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Genesis Empire Command Center")
    parser.add_argument("--task", required=True, help="任務 ID")
    parser.add_argument("--prompt", help="直接輸入指令內容")
    parser.add_argument("--prompt_file", help="輸入指令內容的檔案路徑")
    
    args = parser.parse_args()
    
    # 邏輯判斷：優先讀取檔案，若無則讀取直接參數
    final_prompt = ""
    if args.prompt_file:
        with open(args.prompt_file, 'r', encoding='utf-8') as f:
            final_prompt = f.read()
    elif args.prompt:
        final_prompt = args.prompt
    else:
        print("[錯誤] 請提供 --prompt 或 --prompt_file")
        exit(1)
        
    center = Empire_Command_Center()
    center.execute_ai_task(args.task, final_prompt)