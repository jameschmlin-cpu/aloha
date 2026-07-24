import json
import hashlib
import os

class MemorySentinel:
    def __init__(self, base_path=r"C:\Genesis\SDK\memory"):
        self.base_path = base_path

    def save_snapshot(self, category, topic, data):
        """將決策與重要對話存入實體檔案"""
        content = json.dumps({"topic": topic, "data": data}, indent=4)
        h = hashlib.sha256(content.encode()).hexdigest()[:8]
        file_name = f"{category}_{topic}_{h}.json"
        file_path = os.path.join(self.base_path, category, file_name)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return file_path

    def load_all_snapshots(self):
        """用於啟動時回溯記憶"""
        # 這裡未來會實現全掃描注入 context 的邏輯
        return "記憶庫讀取就緒"