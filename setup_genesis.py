import os
import hashlib

# 目標路徑
root = r"C:\Genesis"
os.makedirs(root, exist_ok=True)

# 定義檔案與內容
data = {
    "AGENTS.md": "# AI 工作守則\n參考: [[ARCHITECTURE.md]]",
    "PLAN.md": "# Roadmap\n參考: [[ARCHITECTURE.md]]",
    "PROGRESS.md": "# 進度\n參考: [[ARCHITECTURE.md]]",
    "DECISIONS.md": "# 決策\n參考: [[ARCHITECTURE.md]]",
    "TASKS.md": "# 任務\n參考: [[ARCHITECTURE.md]]",
    "MEMORY.md": "# 記憶\n參考: [[ARCHITECTURE.md]]",
    "CHANGELOG.md": "# 變更紀錄\n參考: [[ARCHITECTURE.md]]",
    "ARCHITECTURE.md": "# 系統架構\n核心節點: Node A-D"
}

for name, content in data.items():
    h = hashlib.sha256(content.encode()).hexdigest()
    with open(os.path.join(root, name), 'w', encoding='utf-8') as f:
        f.write(f"{content}\n\n---\nHash: {h}")
    print(f"File {name} synced.")