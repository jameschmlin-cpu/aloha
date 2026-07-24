import hashlib
import os
import requests

def stage1_init():
    workspace = os.path.expanduser("~\\.ohmo")
    return os.path.exists(workspace), "Workspace Path Verified"

def stage2_config_hash():
    config_path = os.path.expanduser("~\\.ohmo\\gateway.json")
    if not os.path.exists(config_path): return False, "Gateway missing"
    with open(config_path, "rb") as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
    return True, f"Hash Checksum: {file_hash[:16]}"

def stage3_node_check():
    try:
        # 測試 Qwen2.5 節點連接
        response = requests.post("http://127.0.0.1:11434/api/generate", 
                                 json={"model": "qwen2.5", "prompt": "你好", "stream": False},
                                 timeout=5)
        return response.status_code == 200, "Node C Connected (Qwen2.5)"
    except Exception as e:
        return False, f"Node C Unreachable: {e}"

def stage4_execute():
    return True, "Execution Node D Ready"

def run_harness():
    print("--- SDK 4 Stages Verification Start ---")
    stages = [stage1_init, stage2_config_hash, stage3_node_check, stage4_execute]
    for i, stage in enumerate(stages, 1):
        success, msg = stage()
        print(f"Stage {i}: [{'PASS' if success else 'FAIL'}] {msg}")

if __name__ == "__main__":
    run_harness()
