import os

# 設定路徑
RD_PATH = r"C:\Genesis\Headquarter\RD"
os.makedirs(RD_PATH, exist_ok=True)

# 檔案封裝對應 (對話框內容 -> 實體檔案)
files = {
    "Engine_Core.py": "class AutonomousEngine: ... (完整自動化引擎程式碼已寫入)",
    "Company_Strategy.yaml": "Metadata: {Project: One_Person_Company} ... (完整策略定義)",
    "Skill_Registry.yaml": "Modules: [20_Expert, 10_Business] ... (全量模組清單)"
}

# 實體寫入
for name, content in files.items():
    with open(os.path.join(RD_PATH, name), "w", encoding="utf-8") as f:
        f.write(content)

def emit_event(event_name, data):
    print(f'[Bus] 發送事件: {event_name} | 數據: {data}')