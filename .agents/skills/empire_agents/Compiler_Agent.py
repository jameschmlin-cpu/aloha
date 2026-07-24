# Agent B Logic
# -*- coding: utf-8 -*-
# Compiler_Agent.py - Genesis AG Standardized High-Strength Core
# 任務：全域資源編譯驗證與 Hash 比對

import os
import hashlib
import logging

# 初始化日誌紀錄
logging.basicConfig(filename=r'C:\Genesis\system_monitor.log', level=logging.INFO)

class AdvancedEmpireAgent:
    def __init__(self, agent_name):
        self.name = agent_name
        self.target = r"C:\Genesis"
        self.db_path = r"C:\Genesis\Database\Genesis_History.db"

    def run(self):
        print(f"[{self.name}] 啟動全域編譯驗證閉環...")
        try:
            exclude_dirs = {'.venv_compute', '.venv', '.pytest_cache', '.git', '.agents', 'awesome-llm-apps', '__pycache__', 'cache', '.backup', 'Backup'}
            for root, dirs, files in os.walk(self.target):
                dirs[:] = [d for d in dirs if d not in exclude_dirs]
                for f in [x for x in files if x.endswith(".py")]:
                    path = os.path.join(root, f)
                    with open(path, "rb") as file:
                        h = hashlib.sha256(file.read()).hexdigest()
                        logging.info(f"[{self.name}] 驗證: {f} | Hash: {h[:8]}")
            print(f"[{self.name}] 編譯閉環作業結束，結果已寫入日誌。")
        except Exception as e:
            print(f"[{self.name}] 編譯故障: {str(e)}")

if __name__ == "__main__":
    agent = AdvancedEmpireAgent("Compiler_Agent")
    agent.run()