# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\Management_Hub\Gemini_Command_Center_3.py
# 狀態：全量環境修正版
import sys
import os
import hashlib
import py_compile

# 強制將根目錄與模組父目錄插入搜尋路徑首位，確保載入正確
BASE_DIR = r"C:\Genesis"
CORE_DIR = os.path.join(BASE_DIR, "Genesis_Core")
if BASE_DIR not in sys.path: sys.path.insert(0, BASE_DIR)
if CORE_DIR not in sys.path: sys.path.insert(0, BASE_DIR) # 確保模組可被尋獲

from Genesis_Core.Base_Temple import Base_Temple
from Genesis_Core.Core_Gateway import Core_Gateway

class Gemini_Command_Center_3(Base_Temple, Core_Gateway):
    def __init__(self):
        Base_Temple.__init__(self)
        Core_Gateway.__init__(self)
        self._run_sandbox_check()

    def _run_sandbox_check(self):
        try:
            py_compile.compile(__file__, doraise=True)
        except Exception:
            sys.exit(1)

    def generate_hash(self):
        sha256 = hashlib.sha256()
        with open(__file__, 'rb') as f:
            sha256.update(f.read())
        return sha256.hexdigest()

    def run_task(self, task_id, cmd):
        return self.dispatch(task_id, cmd)

    def update_engine_logic(self, new_config):
        self.set_config(new_config)

    def execute_and_modify(self, task_id, logic_hook):
        return self.dispatch_with_override(task_id, logic_hook)

if __name__ == "__main__":
    try:
        cc = Gemini_Command_Center_3()
        print(f"[實體 Hash 證書] {cc.generate_hash()}")
        cc.update_engine_logic({"security_mode": "STRICT", "debug": True})
        status = cc.execute_and_modify("SYS_CORE_002", "RUN_QC_CHECK")
        print(f"[最終執行狀態] 狀態: {status}")
    except Exception as e:
        print(f"[致命錯誤] {e}")
        sys.exit(1)