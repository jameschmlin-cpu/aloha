# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\SDK\adapter_factory.py
# 狀態：積木封裝器 (Wrapper Factory) - 負責將外部工具一鍵封裝成 Python 積木

import os

def generate_brick_wrapper(tool_name, api_spec):
    """
    自動生成對應的外部工具封裝積木腳本，寫入至 C:\Genesis\SDK\External_Modules\
    """
    dest_dir = r"C:\Genesis\SDK\External_Modules"
    os.makedirs(dest_dir, exist_ok=True)
    
    inputs = api_spec.get("inputs", {})
    params_def = []
    for param_name, default_val in inputs.items():
        if isinstance(default_val, str):
            params_def.append(f"{param_name}='{default_val}'")
        else:
            params_def.append(f"{param_name}={default_val}")
            
    params_signature = ", ".join(params_def)
    params_only_names = list(inputs.keys())
    
    code = f"""# -*- coding: utf-8 -*-
# 檔案：C:\\Genesis\\SDK\\External_Modules\\{tool_name}.py
# 狀態：自動生成的外部積木封裝器 (由 Wrapper Factory 生產)

import os
import sys
import json

class {tool_name}:
    def __init__(self):
        pass

    def run(self, {params_signature}):
        \"\"\"{tool_name} 執行方法\"\"\"
        print(f"[*] [{tool_name}] 啟動調用...")
        
        try:
            # 模擬網路超時以展示備援 (透過 GENESIS_OFFLINE_TEST 環境變數)
            offline_test = os.environ.get("GENESIS_OFFLINE_TEST", "1")
            if offline_test == "1":
                raise TimeoutError("Cloud service connection timed out (Simulated offline condition).")
                
            # 雲端運算模擬 (正常連網時)
            result = f"Cloud processed {tool_name} output"
            return result
            
        except Exception as e:
            print(f"[Warning] [{tool_name}] 雲端 API 失敗: {{e}}。啟動 RTX 3060 本地 fallback...")
            try:
                # 載入本地 AI 大腦
                sys.path.insert(0, r"C:\\Genesis\\RD_Center")
                from SDK.AI_Core.Local_AI_Agent import LocalAIAgent
                agent = LocalAIAgent()
                telemetry = {{
                    "tool": "{tool_name}",
                    "params": {{{', '.join([f'"{p}": str({p})' for p in params_only_names])}}},
                    "error": str(e)
                }}
                decision = agent.analyze_and_decide(telemetry)
                fallback_result = f"[Local GPU Fallback Output] {{decision.get('analysis', 'Mock fallback rendering completed.')}}"
                return fallback_result
            except Exception as fe:
                print(f"[Critical] 本地 fallback 異常: {{fe}}")
                return f"[Fallback Failed] {{str(fe)}}"
"""

    filepath = os.path.join(dest_dir, f"{tool_name}.py")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"[Wrapper Factory] Successfully created wrapper: {filepath}")
    return filepath