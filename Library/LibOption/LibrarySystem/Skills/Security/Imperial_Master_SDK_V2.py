# -*- coding: utf-8 -*-
# Path: C:\Genesis\Hermes\Library\Skills\Security\Imperial_Master_SDK_V2.py
# 總工程師：林雋懋 (Chun Mao Lin) 簽署 | 職責：全量資產鑑別、病毒清創、開機主權接管
# ------------------------------------------------------------------------------
import os
import hashlib
import json
import subprocess
from datetime import datetime

class ImperialMasterSDK:
    def __init__(self):
        self.BASE = r"C:\Genesis"
        self.SECURITY_ZONE = os.path.join(self.BASE, "Security")
        self.SKILLS_ZONE = os.path.join(self.BASE, "Hermes", "Library", "Skills")
        self.LOG_PATH = os.path.join(self.BASE, "Hermes", "Library", "Brain_Logs", "Security_Scan.json")
        self.inventory = []

    def _get_file_hash(self, path):
        """[鑑別功能] 產出實體 SHA-256 Hash，作為唯一身分識別"""
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()

    def _is_suspicious(self, path, content):
        """[檢查功能] 偵測前任病毒特徵：包含空殼程式、惡意路徑重定向"""
        # 1. 檔案大小檢查 (小於 100 bytes 通常是空殼)
        if os.path.getsize(path) < 100: return "EMPTY_SHELL"
        # 2. 關鍵字過濾 (偵測是否連往舊路徑 Lobster_Work)
        malicious_keywords = ["Lobster_Work", "Lobster_Brain_System", "pass", "TODO"]
        if any(key in content for key in malicious_keywords):
            return "VETERAN_VIRUS_DETECTED"
        return "CLEAN"

    def deep_scan_and_classify(self):
        """[搜尋、索引、分類] 遍歷 C:\Genesis 並重新整理架構"""
        print(f"[{datetime.now()}] 🛡️ 啟動全量資產鑑定任務...")
        for root, _, files in os.walk(self.BASE):
            for file in files:
                if file.endswith((".py", ".pyd", ".sys")):
                    full_path = os.path.join(root, file)
                    try:
                        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                        
                        status = self._is_suspicious(full_path, content)
                        f_hash = self._get_file_hash(full_path)
                        
                        # 索引與分類邏輯
                        asset_info = {
                            "name": file,
                            "path": full_path,
                            "hash": f_hash,
                            "status": status,
                            "category": "SDK" if "Skills" in root else "System_Core"
                        }
                        self.inventory.append(asset_info)
                        
                        if status != "CLEAN":
                            print(f"🚨 警告：偵測到風險檔案 {file} -> {status}")
                    except Exception as e:
                        print(f"⚠️ 無法讀取檔案 {file}: {e}")

    def execute_sovereign_lock(self):
        """[主權接管] 開機自動執行的核心動作"""
        print(f"[{datetime.now()}] 🚀 執行主權定錨與環境清創...")
        # 清除影子進程
        subprocess.run("taskkill /F /IM node.exe /T", shell=True, capture_output=True)
        # 鎖定意志文件
        soul_path = os.path.join(self.BASE, "Hermes", "Library", "Soul.md")
        if os.path.exists(soul_path):
            subprocess.run(f'attrib +r +s +h "{soul_path}"', shell=True)
        
        # 存檔索引清單
        os.makedirs(os.path.dirname(self.LOG_PATH), exist_ok=True)
        with open(self.LOG_PATH, "w", encoding="utf-8") as f:
            json.dump(self.inventory, f, indent=4, ensure_ascii=False)
        
        print(f"✅ 執政環境已就緒。索引清單已同步至：{self.LOG_PATH}")

if __name__ == "__main__":
    sdk = ImperialMasterSDK()
    sdk.deep_scan_and_classify()
    sdk.execute_sovereign_lock()