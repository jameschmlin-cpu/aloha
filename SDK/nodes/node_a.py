# C:\Genesis\SDK\nodes\node_a.py
import json

class NodeA_Brain:
    def __init__(self):
        self.queue_path = r"C:\Genesis\SDK\task_queue.json"

    def dispatch(self, command_payload):
        """將指令封裝並推入 Goose 執行隊列"""
        task = {
            "node_origin": "NODE_A",
            "command": command_payload,
            "status": "QUEUED"
        }
        with open(self.queue_path, 'w', encoding='utf-8') as f:
            json.dump(task, f)
        return True