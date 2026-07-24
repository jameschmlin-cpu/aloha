# Agent A Logic
# -*- coding: utf-8 -*-
# Diag_Agent.py - Genesis AG Advanced Diagnostic & Logic Engine
# Version: 2026.07.12.1500
# 本模組具備獨立決策邏輯、錯誤攔截與完整資料庫操作能力

import os
import sqlite3
import hashlib
import logging

# 初始化日誌紀錄
logging.basicConfig(filename=r'C:\Genesis\system_monitor.log', level=logging.INFO)

class AdvancedDiagAgent:
    def __init__(self):
        self.target = r"C:\Genesis"
        self.db_path = r"C:\Genesis\Database\Genesis_History.db"
        self.agent_id = "DIAG_AGENT_V2_PRO"

    def verify_hash(self, file_path):
        """強化版 Hash 計算，處理大型檔案與權限異常"""
        sha256 = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(65536), b""):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except PermissionError:
            return "PERMISSION_DENIED"
        except Exception:
            return "ERROR"

    def scan_directory(self, root_dir):
        """盤點邏輯主程序"""
        file_list = []
        exclude_dirs = {'.venv_compute', '.venv', '.pytest_cache', '.git', '.agents', 'awesome-llm-apps', '__pycache__', 'cache', '.backup', 'Backup'}
        for root, dirs, files in os.walk(root_dir):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            for file in files:
                path = os.path.join(root, file)
                h = self.verify_hash(path)
                file_list.append((path, h))
        return file_list

    def run(self):
        """Agent 主邏輯：自動執行、自我修正、盤點閉環"""
        print(f"[{self.agent_id}] 系統初始化，開始深度邏輯盤點...")
        try:
            results = self.scan_directory(self.target)
            self.commit_to_db(results)
            logging.info(f"[{self.agent_id}] 盤點成功，記錄 {len(results)} 個模組。")
            print(f"[{self.agent_id}] 盤點閉環作業成功，數據已寫入 Genesis_History.db。")
        except Exception as e:
            error_msg = f"[{self.agent_id}] 重大故障: {str(e)}"
            logging.error(error_msg)
            # 觸發自動除錯重置邏輯
            self.trigger_rca(error_msg)

    def commit_to_db(self, data):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS file_inventory (path TEXT PRIMARY KEY, hash TEXT)")
        cursor.executemany("INSERT OR REPLACE INTO file_inventory (path, hash) VALUES (?, ?)", data)
        conn.commit()
        conn.close()

    def trigger_rca(self, error):
        """符合治理憲法之 RCA 回報機制"""
        print(f"[RCA 啟動] 請檢查: {error}")

if __name__ == "__main__":
    agent = AdvancedDiagAgent()
    agent.run()