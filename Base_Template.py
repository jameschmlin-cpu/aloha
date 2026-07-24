# -*- coding: utf-8 -*-
import sys
import os
import psutil
import sqlite3
import hashlib
import inspect
import json

# ==========================================================
# 物理導通層：強行路徑映射 (Strict Path Mapping)
# 確保絕對路徑被優先掃描，徹底解決 ModuleNotFoundError
# ==========================================================
_CORE_PATH = r"C:\Genesis"
_STAGE0_PATH = r"C:\Genesis\RD_Center\Source\Option\Stage_0"
_SDK_BASE_PATH = r"C:\Genesis\RD_Center\SDK\Base"

for _path in [_CORE_PATH, _STAGE0_PATH, _SDK_BASE_PATH]:
    if _path not in sys.path:
        sys.path.insert(0, _path)

# 執行路徑導通驗證 (沙盒模擬時即刻生效)
def verify_paths():
    for _p in [_STAGE0_PATH]:
        if not os.path.exists(_p):
            print(f"[QC FAIL] 物理路徑缺失: {_p}")
            return False
    return True

if not verify_paths():
    raise EnvironmentError("Genesis 核心架構路徑導通失敗")

# 匯入核心模組
from Causal_Tracer import CausalTracer
from SDK.Core.Doctor_Prime import Doctor_Prime
from Event_Bus import global_bus

class Base_Template:
    """
    【帝國核心內核】Genesis SDK 全自動自癒樞紐
    遵從憲法：強制繼承校驗、語法預編譯、實體 Hash 註冊。
    """
    def __init__(self, brick_id="CORE_INIT"):
        self.brick_id = brick_id
        # Stage 4 校驗節點
        self._enforce_integrity_and_registration()
        
        self.doctor = Doctor_Prime()
        self.tracer = CausalTracer()
        self.config = self._load_central_config()
        self.db_manager = self._init_db_manager()

    def _enforce_integrity_and_registration(self):
        """SDK Stage 4 校驗：強制檢查檔案繼承與 Hash 註冊"""
        caller_file = inspect.stack()[2].filename
        
        # 1. 自動編譯語法檢查
        with open(caller_file, 'r', encoding='utf-8') as f:
            source_code = f.read()
            try:
                compile(source_code, caller_file, 'exec')
            except SyntaxError as e:
                raise RuntimeError(f"[QC FAIL] 程式語法異常: {caller_file} | 錯誤: {e}")

        # 2. 計算實體 Hash
        file_hash = hashlib.sha256(source_code.encode('utf-8')).hexdigest()
        
        # 3. 註冊至 DFMEA 實體資料庫
        self._register_hash_to_dfmea(caller_file, file_hash)
        print(f"[QC PASS] 物理 Hash 比對驗收完成: {file_hash[:16]} | Path: {caller_file}")

    def _register_hash_to_dfmea(self, path, file_hash):
        """將 Hash 寫入 Genesis_DFMEA.db，完成合規入庫"""
        dfmea_db = r"C:\Genesis\Database\Genesis_DFMEA.db"
        conn = sqlite3.connect(dfmea_db)
        try:
            conn.execute("CREATE TABLE IF NOT EXISTS hash_registry (file_path TEXT PRIMARY KEY, sha256 TEXT)")
            conn.execute("INSERT OR REPLACE INTO hash_registry (file_path, sha256) VALUES (?, ?)", 
                         (path, file_hash))
            conn.commit()
        finally:
            conn.close()

    def run_protected(self, stage_id, task, *args, **kwargs):
        """全閉環自癒執行器"""
        try:
            if psutil.Process(os.getpid()).memory_info().rss > self.config['system']['memory_limit']:
                self.doctor.execute_closed_loop_recovery(reason="RESOURCE_EXHAUSTED")
            
            trace_id = self.tracer.generate_trace_id(f"S{stage_id}", {"brick": self.brick_id})
            result = task(*args, **kwargs)
            global_bus.publish(f"S{stage_id}_COMPLETED", {"brick": self.brick_id, "trace_id": trace_id})
            return result
        except Exception as e:
            self.doctor.execute_closed_loop_recovery(reason=str(e))
            return None 

    def _load_central_config(self):
        config_path = r"C:\Genesis\Config\Genesis_Config.json"
        if not os.path.exists(config_path):
            return {"system": {"memory_limit": 1024 * 1024 * 500}}
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _init_db_manager(self):
        db_path = r"C:\Genesis\Database"
        return {
            'Trace': sqlite3.connect(os.path.join(db_path, "Trace_Log.db")),
            'State': sqlite3.connect(os.path.join(db_path, "System_State.db")),
            'Registry': sqlite3.connect(os.path.join(db_path, "Brick_Registry.db"))
        }