# C:\Genesis\SDK\send_command.py
import json
import sys

# 接收參數作為指令
cmd = sys.argv[1] if len(sys.argv) > 1 else "python --version"

task = {"command": cmd, "status": "QUEUED"}
# 強制以純 UTF-8 (不含 BOM) 寫入
with open(r"C:\Genesis\SDK\task_queue.json", "w", encoding="utf-8") as f:
    json.dump(task, f)

print(f"[Queue] 已指令部署: {cmd}")