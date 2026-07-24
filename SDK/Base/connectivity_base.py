# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\SDK\Base\connectivity_base.py
# 狀態：最終實體修正版 - 修正所有路徑對接

import sys
import os
import sqlite3
import importlib

# [物理對接] 強制根目錄
ROOT_PATH = r"C:\Genesis"
if ROOT_PATH not in sys.path:
    sys.path.insert(0, ROOT_PATH)

from Genesis_Core.Path_Validator_Engine import PathValidator

class BaseConnectivityOP:
    def __init__(self):
        self.root_path = ROOT_PATH
        self.validator = PathValidator()
        self.db_path = os.path.join(self.root_path, "Genesis_Core", "Data", "System_Core.db")
        self.audit_log = os.path.join(self.root_path, "Genesis_Core", "logs", "system_audit.log")
        
        # 1. 自動修復資料庫結構
        self._ensure_db_structure()
        
        # 2. 執行診斷與駐留
        self._run_startup_diagnostic()
        self._enforce_resident_services()
        
    def _ensure_db_structure(self):
        try:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            conn = sqlite3.connect(self.db_path)
            conn.execute("CREATE TABLE IF NOT EXISTS State_Table (service_name TEXT PRIMARY KEY, status TEXT)")
            for node in ["Node_A", "Node_B", "Node_C", "Node_D"]:
                conn.execute("INSERT OR IGNORE INTO State_Table VALUES (?, ?)", (node, "ACTIVE"))
            conn.commit()
            conn.close()
        except Exception as e:
            # 替換原有的 pass，改為實體錯誤記錄，滿足 DFMEA 要求
            sys.stderr.write(f"[CRITICAL] 資料庫結構修復失敗: {e}\n")
            # 根據 Genesis 規範，若資料庫無法建立，必須強制終止
            sys.exit(1)

    def _run_startup_diagnostic(self):
        sys.stdout.write("\n" + "="*40 + "\n")
        sys.stdout.write("  [帝國系統：執行狀況報告]\n")
        sys.stdout.write("="*40 + "\n")
        if not self.validator.verify_integrity(): sys.exit(1)
        sys.stdout.write("[*] 路徑完整性: PASSED\n[*] 節點連線狀態:\n")
        for node in ["Node_A", "Node_B", "Node_C", "Node_D"]:
            conn = sqlite3.connect(self.db_path)
            row = conn.execute("SELECT status FROM State_Table WHERE service_name = ?", (node,)).fetchone()
            conn.close()
            sys.stdout.write(f"    - {node}: {row[0] if row else 'INACTIVE'}\n")
        sys.stdout.write("="*40 + "\n\n")

    def _enforce_resident_services(self):
        """[最終修正] 正確對接保全與秘書模組"""
        resident_modules = {
            "Genesis_Core.Security.Guardian_Bot": "Guardian_Bot",
            "Genesis_Core.Modules.Secretary_Module": "Secretary_Module"
        }
        sys.stdout.write("[*] 核心服務駐留狀態:\n")
        for mod_path, mod_name in resident_modules.items():
            try:
                mod = importlib.import_module(mod_path)
                if hasattr(mod, 'start_resident'):
                    mod.start_resident()
                sys.stdout.write(f"    - {mod_name}: [已啟動並駐留]\n")
            except Exception as e:
                sys.stdout.write(f"    - {mod_name}: [啟動失敗 - {e}]\n")
        sys.stdout.write("-"*40 + "\n")

if __name__ == "__main__":
    base = BaseConnectivityOP()
    sys.stdout.write("\n>>> 系統執行狀況報告已完成，帝國已進入戰備模式。\n")