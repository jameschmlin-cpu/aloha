# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\Management_Hub\Genesis_Guard.py
import hashlib

class GenesisGuard:
    def __init__(self):
        self.log_path = r"C:\Genesis\Logs\Ops_Log.txt"
        
    def calculate_hash(self, file_path):
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()

    def log_action(self, message):
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(f"[LOG] {message}\n")

if __name__ == "__main__":
    guard = GenesisGuard()
    guard.log_action("Genesis_Guard 已啟動，開始對 SDK 進行診斷...")