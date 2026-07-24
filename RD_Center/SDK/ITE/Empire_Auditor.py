# -*- coding: utf-8 -*-

# Path: C:\Genesis\Empire_Auditor.py

# 龍蝦帝國專屬 - 系統誠信稽核器 v1.0.0

# 指揮官：林雋懋 | 狀態：閉迴路管理執行中



import hashlib

import os

import json

from datetime import datetime



class EmpireAuditor:

    def __init__(self):

        # 鎖定實體路徑，確保不逃逸

        self.target_dir = r"C:\Genesis\Database"

        self.log_file = r"C:\Genesis\Logs\Auditor_Log.txt"

        

        # 確保日誌目錄存在

        if not os.path.exists(r"C:\Genesis\Logs"):

            os.makedirs(r"C:\Genesis\Logs")



    def calculate_sha256(self, file_path):

        """實體 Hash 校驗邏輯，嚴禁 pass/TODO"""

        sha256_hash = hashlib.sha256()

        try:

            with open(file_path, "rb") as f:

                for byte_block in iter(lambda: f.read(4096), b""):

                    sha256_hash.update(byte_block)

            # 剛性判定：空殼程式防禦 (若檔案小於 1024 bytes 視為惡意欺騙)

            if os.path.getsize(file_path) < 1024:

                return "🚨_EMPTY_SHELL_DETECTED"

            return sha256_hash.hexdigest()

        except Exception as e:

            return f"ERROR_{str(e)}"



    def run_audit(self):

        """執行全節點掃描"""

        results = {}

        if not os.path.exists(self.target_dir):

            return {"status": "FAILED", "msg": "路徑阻斷：C:\\ITE\\Database 不存在"}

        

        for file in os.listdir(self.target_dir):

            if file.endswith(".db"):

                path = os.path.join(self.target_dir, file)

                results[file] = self.calculate_sha256(path)

        

        # 產出審計報告，確保邏輯閉環

        report = {

            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

            "audit_results": results

        }

        

        with open(self.log_file, "w", encoding="utf-8") as f:

            f.write(json.dumps(report, indent=4))

        

        return report



if __name__ == "__main__":

    auditor = EmpireAuditor()

    print("🦞 [龍蝦帝國] 正在進行實體誠信稽核...")

    audit_report = auditor.run_audit()

    print(f"✅ 稽核完成。報告已寫入: {auditor.log_file}")

    for file, h in audit_report.get("audit_results", {}).items():

        print(f" -> {file}: {h[:16]}...")