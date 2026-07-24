# -*- coding: utf-8 -*-
import sys
import os
import json
import psutil
import sqlite3

# ==========================================================
# 物理導通層：全路徑展平 (Flattened Path)
# 確保 Stage_0 與 Stage_1 模組在任何執行路徑下皆可被識別
# ==========================================================
sys.path.insert(0, r"C:\Genesis")
sys.path.insert(0, r"C:\Genesis\RD_Center")
sys.path.insert(0, r"C:\Genesis\RD_Center\Source\Option\Stage_0")
sys.path.insert(0, r"C:\Genesis\RD_Center\Source\Option\Stage_1")

# 直接從展平後的目錄匯入檔案，無需冗長路徑名稱空間
from Causal_Tracer import CausalTracer
from SDK.Core.Doctor_Prime import Doctor_Prime
from Event_Bus import global_bus

# 處理 connectivity_base 匯入 (針對 SDK/Base 目錄)
sys.path.insert(0, r"C:\Genesis\RD_Center\SDK\Base")

class Base_Template:
    """
    【帝國核心內核】Genesis SDK 全自動自癒樞紐
    徹底移除熔斷機制，改為「偵測-診斷-修復」的閉環自癒
    """
    def __init__(self, brick_id="CORE_INIT"):
        self.brick_id = brick_id
        self.doctor = Doctor_Prime()
        self.tracer = CausalTracer()
        self.config = self._load_central_config()
        self.db_manager = self._init_db_manager()
        self.registry_path = r"C:\Genesis\SDK\Registry.json"

    def run_protected(self, stage_id, task, *args, **kwargs):
        """
        全閉環自癒執行器：
        偵測資源異動 -> 診斷 (DFMEA) -> 執行修復 (Doctor) -> 恢復流程
        """
        try:
            # A. 資源檢查 (偵測)
            if psutil.Process(os.getpid()).memory_info().rss > self.config['system']['memory_limit']:
                self.doctor.execute_closed_loop_recovery(reason="RESOURCE_EXHAUSTED")
            
            # B. 執行業務邏輯
            trace_id = self.tracer.generate_trace_id(f"S{stage_id}", {"brick": self.brick_id})
            result = task(*args, **kwargs)
            
            # C. 閉環訊號發布
            global_bus.publish(f"S{stage_id}_COMPLETED", {"brick": self.brick_id, "trace_id": trace_id})
            return result

        except Exception as e:
            # 發生錯誤直接交給 Doctor 進行即時維修或還原
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
        os.makedirs(db_path, exist_ok=True)
        return {
            'Trace': sqlite3.connect(os.path.join(db_path, "Trace_Log.db")),
            'State': sqlite3.connect(os.path.join(db_path, "System_State.db")),
            'Registry': sqlite3.connect(os.path.join(db_path, "Brick_Registry.db"))
        }