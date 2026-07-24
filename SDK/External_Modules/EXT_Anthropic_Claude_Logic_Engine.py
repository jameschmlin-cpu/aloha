# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\SDK\External_Modules\EXT_Anthropic_Claude_Logic_Engine.py
# 狀態：Anthropic Claude Logic Engine 外部模組封裝 (支援 RTX 3060 本地降級備援)

import sys
import os

# Ensure root is in system path for imports
GENESIS_BASE = r"C:\Genesis"
if os.path.join(GENESIS_BASE, "RD_Center") not in sys.path:
    sys.path.insert(0, os.path.join(GENESIS_BASE, "RD_Center"))

class EXT_Anthropic_Claude_Logic_Engine:
    def __init__(self):
        pass

    def run(self, context, user_prompt):
        """(context, user_prompt) -> (refined_plan)"""
        print("[EXT_Anthropic_Claude_Logic_Engine] Querying Anthropic Claude logic core...")
        
        # Simulating potential API request timeout or internet connectivity loss
        try:
            # Under normal operations, this would call Anthropic API.
            # We simulate a connection timeout check to demonstrate fallback
            offline_test_env = os.environ.get("GENESIS_OFFLINE_TEST", "1")
            if offline_test_env == "1":
                raise TimeoutError("Anthropic API request timed out (Simulated offline condition).")
                
            refined_plan = f"Claude refined plan for: {user_prompt}"
            return refined_plan
            
        except Exception as e:
            print(f"[Warning] Anthropic API failed: {e}. Activating RTX 3060 Local Fallback...")
            try:
                from SDK.AI_Core.Local_AI_Agent import LocalAIAgent
                agent = LocalAIAgent()
                # Run decision query on local model
                telemetry = {"context": context, "user_prompt": user_prompt, "source": "EXT_Anthropic"}
                decision = agent.analyze_and_decide(telemetry)
                refined_plan = f"[RTX 3060 Fallback Plan] {decision.get('analysis', 'Fallback analysis result')}"
                return refined_plan
            except Exception as fallback_err:
                print(f"[Critical] Local Fallback also failed: {fallback_err}")
                return "[Error] API Timeout & Local Fallback Failed"
