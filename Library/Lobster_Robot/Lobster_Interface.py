# C:\Genesis\Library\Lobster_Robot\Lobster_Interface.py
import os

class LobsterInterface:
    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.sdk_path = r"C:\Genesis\Library\LibOption"

    def plug_in_module(self, module_name):
        """統一的 API：插拔 SDK 模組"""
        module_path = os.path.join(self.sdk_path, f"{module_name}.py")
        if os.path.exists(module_path):
            print(f"[AGENT {self.agent_id}] 成功插拔並掛載模組: {module_name}")
            return True
        else:
            print(f"[ERROR] 無法掛載模組: {module_name}")
            return False