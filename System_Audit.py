# Category: Security
import os

target_path = r"C:\Genesis\Library\SDK\Webmcp_Core.py"
os.makedirs(os.path.dirname(target_path), exist_ok=True)

# 強制物理內容落地
content = """import os
print("[Webmcp] Core Initialized. Channel Ready.")
# 核心監聽邏輯
"""
with open(target_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"[VERIFY] 檔案落位確認: {os.path.exists(target_path)}")