# C:\Genesis\SDK\orchestrator.py
import subprocess
import json

class Orchestrator:
    def call_brick(self, brick_path, params):
        """呼叫一支積木，並回傳結果"""
        # 這裡模擬把參數丟進去，並執行副程式
        cmd = ["python", brick_path, json.dumps(params)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return json.loads(result.stdout) # 接收回傳的結果

# 使用範例：
# orchestrator = Orchestrator()
# result = orchestrator.call_brick(rrrrrrr"C:\Genesis\Library\SDK\Data_Process_Brick.py", {"data": 100})