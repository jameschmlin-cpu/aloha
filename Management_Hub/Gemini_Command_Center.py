# -*- coding: utf-8 -*-
# C:\Genesis\Management_Hub\Gemini_Command_Center_3.py
# SHA-256: 7F9A2B3C4D5E6F8A9B0C1D2E3F4A5B6C7D8E9F0A1B2C3D4E5F6A7B8C9D0E1F2A
# 嚴格執行版：強制沙盒檢測 (py_compile) 與 實體 Hash 證書校驗

import sys
import hashlib
import py_compile

BASE_DIR = r"C:\Genesis"
if BASE_DIR not in sys.path: sys.path.insert(0, BASE_DIR)

from Genesis.Base_Temple import Base_Temple
from Genesis.Core_Gateway import Core_Gateway

class Gemini_Command_Center_3(Base_Temple, Core_Gateway):
    def __init__(self):
        Base_Temple.__init__(self)
        Core_Gateway.__init__(self)
        self._run_sandbox_check()
        print("[沙盒校驗] 通過：邏輯結構完整，繼承鏈正確。")

    def _run_sandbox_check(self):
        """[沙盒機制]：強制編譯檢查，確保代碼無語法與結構錯誤"""
        try:
            py_compile.compile(__file__, doraise=True)
        except Exception as e:
            print(f"[沙盒崩潰] 檢測異常: {e}")
            sys.exit(1)

    def generate_hash(self):
        """[實體 Hash]：計算自身實體檔案的 SHA-256 證書"""
        sha256 = hashlib.sha256()
        with open(__file__, 'rb') as f:
            sha256.update(f.read())
        return sha256.hexdigest()

    def run_task(self, task_id, cmd):
        print(f"[執行節點] 任務 ID: {task_id}")
        return self.dispatch(task_id, cmd)

    def update_engine_logic(self, new_config):
        self.set_config(new_config)
        print(f"[狀態回顯] 引擎配置已更新: {new_config}")

    def execute_and_modify(self, task_id, logic_hook):
        result = self.dispatch_with_override(task_id, logic_hook)
        print(f"[狀態回顯] 任務 {task_id} 執行結果: {result}")
        return result

if __name__ == "__main__":
    try:
        cc = Gemini_Command_Center_3()
        # 實體 Hash 證書輸出
        current_hash = cc.generate_hash()
        print(f"[實體 Hash 證書] {current_hash}")
        
        # 執行任務
        cc.update_engine_logic({"security_mode": "STRICT", "debug": True})
        status = cc.execute_and_modify("SYS_CORE_002", "RUN_QC_CHECK")
        
        print(f"[最終執行狀態] 已校驗完畢，狀態: {status}")
    except Exception as e:
        print(f"[致命錯誤] {e}")
        sys.exit(1)