# -*- coding: utf-8 -*-
# 最終版：全域任務自動對接引擎 (含指紋識別與自動歸位)
import os
import sqlite3
import hashlib

class GenesisCoreEngine:
    def __init__(self):
        self.db_path = r"C:\Genesis\Database\Genesis_DFMEA.db"
        self.sdk_dir = r"C:\Genesis"

    def generate_fingerprint(self, file_path):
        """為每個程式生成唯一指紋 (id)"""
        sha = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha.update(chunk)
        return sha.hexdigest()[:16] # 取前16碼作為唯一任務ID

    def auto_onboard(self):
        print("[啟動] 開始全域任務自動對接...")
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        count = 0
        for root, _, files in os.walk(self.sdk_dir):
            for file in files:
                if file.endswith(".py") and "Genesis" not in file:
                    file_path = os.path.join(root, file)
                    task_id = self.generate_fingerprint(file_path)
                    
                    # 檢查該 ID 是否已註冊
                    cursor.execute("SELECT id FROM dfmea_matrix WHERE id=?", (task_id,))
                    if not cursor.fetchone():
                        # 自動註冊新任務
                        cursor.execute("INSERT INTO dfmea_matrix (id, problem_point, severity) VALUES (?, ?, ?)", 
                                       (task_id, f"Auto-Registered: {file}", 50))
                        count += 1
                        print(f"[歸位] 自動註冊任務: {file} (ID: {task_id})")
        
        conn.commit()
        conn.close()
        print(f"[完成] 本次自動歸位 {count} 個新任務。帝國架構已閉鎖。")

if __name__ == "__main__":
    engine = GenesisCoreEngine()
    engine.auto_onboard()