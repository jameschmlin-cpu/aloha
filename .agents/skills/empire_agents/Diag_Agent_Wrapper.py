# C:\Genesis\.agents\skills\empire_agents\Diag_Agent_Wrapper.py
import json
import os
from Diag_Agent import AdvancedDiagAgent

class DiagAgentWrapper(AdvancedDiagAgent):
    def __init__(self):
        super().__init__()
        self.diag_log = r"C:\Genesis\Diagnostics.json"
        self.status = {"step": "init", "error": None, "path_check": False}

    def write_status(self):
        with open(self.diag_log, "w", encoding="utf-8") as f:
            json.dump(self.status, f, indent=4)

    def run(self):
        try:
            self.status["step"] = "executing_parent"
            self.write_status()
            
            # 檢測路徑存取權限
            self.status["path_check"] = os.access(self.target, os.W_OK)
            
            # 執行原程式邏輯
            super().run()
            
            self.status["step"] = "success"
        except Exception as e:
            self.status["step"] = "failed"
            self.status["error"] = str(e)
        finally:
            self.write_status()

if __name__ == "__main__":
    wrapper = DiagAgentWrapper()
    print(">>> [繼承器] 正在執行，請觀察 C:\Genesis\Diagnostics.json 的變化...")
    wrapper.run()