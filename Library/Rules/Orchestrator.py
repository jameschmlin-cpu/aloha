# -*- coding: utf-8 -*-
import sys
import types
import os

# 強制路徑導通（優先級高）
GENESIS_BASE = r"C:\Genesis"
if GENESIS_BASE not in sys.path:
    sys.path.insert(0, GENESIS_BASE)
# 確保 LibrarySystem 與 RD_Center 可被正常搜尋
sys.path.insert(0, os.path.join(GENESIS_BASE, "RD_Center"))
sys.path.insert(0, os.path.join(GENESIS_BASE, "Library", "LibOption", "LibrarySystem"))

# 解決 [FATAL] 錯誤：模擬 Genesis_Core 模組並將 Path_Validator_Engine 掛載進去
genesis_core = types.ModuleType("Genesis_Core")
import Path_Validator_Engine
sys.modules["Genesis_Core"] = genesis_core
sys.modules["Genesis_Core.Path_Validator_Engine"] = Path_Validator_Engine

# 現在可以正常匯入
from Path_Validator_Engine import PathValidator
from Base_Template import Base_Template
from Library.SDK.Agent_Library_Bridge import Agent_Library_Bridge
from Library.Lobster_Robot.Skill_Deployment_Agent import Skill_Deployment_Agent

class Swarm_Orchestrator(Base_Template):
    """
    【總指揮中心】
    修正：正確對接 PathValidator 類別。
    """
    def __init__(self, brick_id="ORCHESTRATOR_01"):
        # 使用實體名稱 PathValidator 進行物理路徑檢查
        validator = PathValidator()
        if not validator.check_path(r"C:\Genesis"):
            raise Exception("路徑檢測失敗")
            
        Base_Template.__init__(self, brick_id=brick_id)
        self.bridge = Agent_Library_Bridge(brick_id=f"{brick_id}_bridge")
        self.deployer = Skill_Deployment_Agent(brick_id=f"{brick_id}_deployer")

    def run_scenario(self, fm_code, download_url=None):
        """執行狀況模擬"""
        def task():
            advice = self.bridge.get_intelligent_advice(fm_code)
            if not advice and download_url:
                self.deployer.deploy_skill(fm_code, download_url)
                return "已自動更新職能大腦"
            return advice
        return self.run_protected(stage_id="SCENARIO_RUN", task=task)