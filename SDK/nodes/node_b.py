# C:\Genesis\SDK\nodes\node_b.py
# -*- coding: utf-8 -*-
import subprocess
import json
import os

class NodeB_Executor:
    def run_cycle(self):
        queue_path = r"C:\Genesis\SDK\task_queue.json"
        if not os.path.exists(queue_path): return
        
        try:
            with open(queue_path, "r", encoding="utf-8") as f: 
                task = json.load(f)
            
            # 直接執行該檔案，不透過 goose 解析參數字串
            # cmd 預期是一個 Python 檔案路徑
            cmd_path = task["command"]
            print(f"[Exec] 正在運行模組: {cmd_path}")
            
            subprocess.run(["python", cmd_path], check=True)
            
            if os.path.exists(queue_path): os.remove(queue_path)
        except Exception as e:
            print(f"[Error] 任務執行失敗: {e}")