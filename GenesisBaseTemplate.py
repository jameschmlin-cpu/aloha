# -*- coding: utf-8 -*-
import os
import json
from Event_Bus import global_bus  # 整合事件匯流排
from Causal_Tracer import CausalTracer
from SDK.Quality_Control import DFMEA_Module
from SDK.Core import Doctor_Prime

class GenesisBaseTemplate:
    def __init__(self, brick_id):
        self.dfmea = DFMEA_Module()
        self.doctor = Doctor_Prime()
        self.tracer = CausalTracer()
        self.brick_id = brick_id
        self._load_config_and_verify()
        
    def _load_config_and_verify(self):
        # [Stage 2] 配置驅動架構：強制讀取 JSON 並執行實體 Hash 校驗
        with open(r"C:\Genesis\Config\Genesis_Config.json", 'r') as f:
            self.config = json.load(f)
        if not self.dfmea.check_path_integrity(os.getcwd()):
            self.doctor.log_critical("Stage 2 完整性失敗，熔斷啟動。")
            exit(1)

    def run_protected(self, stage_id, task, *args, **kwargs):
        """[Stage 1-4 總閉合執行器]"""
        # [Stage 1] 指紋鎖定 (CPU/硬體指紋驗證)
        if not self.dfmea.verify_fingerprint(): exit(1)
        
        # [Stage 3] 執行前因果鏈結綁定
        trace_id = self.tracer.generate_trace_id(f"S{stage_id}", {"brick": self.brick_id})
        
        # [Stage 3] 合規分析 (預防性阻斷)
        if self.doctor.is_dangerous_action(args): exit(1)
        
        # 執行任務並發布事件
        result = task(*args, **kwargs)
        global_bus.publish(f"S{stage_id}_COMPLETED", {"brick": self.brick_id, "trace_id": trace_id})
        return result