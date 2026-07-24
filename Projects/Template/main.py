# C:\Genesis\Projects\Template\main.py
import sys

# 強制將 C:\Genesis 加入系統搜尋路徑，確保 SDK 被識別
sys.path.append(r"C:\Genesis")

from SDK.memory.sentinel import MemorySentinel

# 執行第一次決策快照
sentinel = MemorySentinel()
history_data = {
    "project": "Empire_Construction",
    "status": "Initialized",
    "core_strategy": "Closed-Loop_Memory_and_SDK",
    "commitment": "Long-term_Collaboration"
}

path = sentinel.save_snapshot("projects", "Empire_Basics", history_data)
print(f"帝國基石已完成物理存檔: {path}")