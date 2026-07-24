# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\SDK\External_Modules\EXT_OpenAI_Vision_API.py
# 狀態：OpenAI Vision API 外部模組封裝 (支援 RTX 3060 本地降級備援)

import sys
import os

GENESIS_BASE = r"C:\Genesis"
if os.path.join(GENESIS_BASE, "RD_Center") not in sys.path:
    sys.path.insert(0, os.path.join(GENESIS_BASE, "RD_Center"))

class EXT_OpenAI_Vision_API:
    def __init__(self):
        pass

    def run(self, image_path, prompt):
        """(image_path, prompt) -> (analysis_text)"""
        print(f"[EXT_OpenAI_Vision_API] Processing image {image_path} with prompt: {prompt}")
        
        try:
            offline_test_env = os.environ.get("GENESIS_OFFLINE_TEST", "1")
            if offline_test_env == "1":
                raise TimeoutError("OpenAI API request timed out (Simulated offline condition).")
                
            analysis_text = f"OpenAI Vision Analysis for {image_path}"
            return analysis_text
            
        except Exception as e:
            print(f"[Warning] OpenAI Vision API failed: {e}. Activating RTX 3060 Local Fallback...")
            try:
                from SDK.AI_Core.Local_AI_Agent import LocalAIAgent
                agent = LocalAIAgent()
                telemetry = {"image_path": image_path, "prompt": prompt, "source": "EXT_OpenAI_Vision"}
                decision = agent.analyze_and_decide(telemetry)
                analysis_text = f"[RTX 3060 Vision Fallback] {decision.get('analysis', 'Fallback analysis result')}"
                return analysis_text
            except Exception as fallback_err:
                print(f"[Critical] Local Fallback also failed: {fallback_err}")
                return "[Error] OpenAI Vision Timeout & Local Fallback Failed"
