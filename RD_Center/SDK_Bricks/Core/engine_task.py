# -*- coding: utf-8 -*-
# Compiled Brick from: engine_task.py
# Category: Core

class EngineTaskBrick:
    def run(self, ctx=None):
        try:
            # -*- coding: utf-8 -*-
            import requests
            import hashlib

            class Stage4Engine:
                def __init__(self, model="qwen2.5:7b"):
                    self.model = model
                    self.url = "http://127.0.0.1:11434/api/generate"

                def execute(self, prompt):
                    """Node C 節點推論：與本地 Ollama 握手"""
                    payload = {"model": self.model, "prompt": prompt, "stream": False}
                    try:
                        response = requests.post(self.url, json=payload, timeout=30)
                        if response.status_code == 200:
                            return response.json().get("response", "無內容回傳")
                        else:
                            return f"執行錯誤: {response.status_code}"
                    except Exception as e:
                        return f"連線異常: {str(e)}"

                def verify_and_log(self, task_name, content):
                    """實體 Hash 產生器 (SDK Stage 4 義務)"""
                    content_bytes = content.encode('utf-8')
                    hash_val = hashlib.sha256(content_bytes).hexdigest()
                    return hash_val
        except Exception as e:
            print(f"[EngineTaskBrick] 運行失敗: {e}")
            return False
        return True
