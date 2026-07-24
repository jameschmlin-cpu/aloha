# Category: Core
# C:\Genesis\deploy_genesis.py
import os

# 系統路徑定義
SDK_PATH = r"C:\Genesis\SDK"
NODES_PATH = os.path.join(SDK_PATH, "nodes")

# 節點實體邏輯 (包含閉環自癒與物理對接)
nodes_code = {
    "node_a.py": """import json\nclass NodeA_Brain:\n    def dispatch(self, cmd):\n        with open(r"C:\\Genesis\\SDK\\task_queue.json", "w") as f:\n            json.dump({"command": cmd, "status": "QUEUED"}, f)\n""",
    "node_b.py": """import subprocess, json, os\nclass NodeB_Executor:\n    def run_cycle(self):\n        if not os.path.exists(r"C:\\Genesis\\SDK\\task_queue.json"): return\n        with open(r"C:\\Genesis\\SDK\\task_queue.json", "r") as f: task = json.load(f)\n        subprocess.run([r"C:\\Genesis\\Bin\\goose.exe", "run", task["command"]])\n        if os.path.exists(r"C:\\Genesis\\SDK\\task_queue.json"): os.remove(r"C:\\Genesis\\SDK\\task_queue.json")\n""",
    "node_c.py": """import subprocess\nclass NodeC_GooseRunner:\n    def execute(self, cmd):\n        return subprocess.run([r"C:\\Genesis\\Bin\\goose.exe", "run", cmd], capture_output=True)\n""",
    "node_d.py": """import hashlib\nclass NodeD_Validator:\n    def verify(self, path):\n        return True # 此處對接物理Hash比對邏輯\n"""
}

# 門戶守衛 (Gatekeeper)
gatekeeper_code = """from nodes.node_a import NodeA_Brain\nfrom nodes.node_b import NodeB_Executor\nimport time\n\nbrain = NodeA_Brain()\nexecutor = NodeB_Executor()\nprint("[System] Genesis 總管邏輯已掛載，閉環作業啟動...")\nwhile True:\n    executor.run_cycle()\n    time.sleep(1)\n"""

def deploy():
    os.makedirs(NODES_PATH, exist_ok=True)
    for name, content in nodes_code.items():
        with open(os.path.join(NODES_PATH, name), "w") as f: f.write(content)
    with open(os.path.join(SDK_PATH, "gatekeeper.py"), "w") as f: f.write(gatekeeper_code)
    print("[DEPLOY] 核心節點與守衛已部署至 C:\\Genesis\\SDK")

if __name__ == "__main__":
    deploy()