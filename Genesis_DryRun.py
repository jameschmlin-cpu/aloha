import sqlite3
import yaml
import os

# 設定路徑
DB_PATH = r"C:\Genesis\Database\Genesis_Tasks.db"
YAML_PATH = r"C:\Genesis\Database\tasks_mapping.yaml"

def run_dry_run():
    print("--- [Node D: 模擬運行程序啟動] ---")
    
    if not os.path.exists(YAML_PATH):
        print("錯誤: 找不到 tasks_mapping.yaml")
        return

    with open(YAML_PATH, "r", encoding="utf-8") as f:
        mapping = yaml.safe_load(f)["tasks_mapping"]
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, task_name FROM tasks WHERE status = 'PENDING'")
    tasks = cursor.fetchall()
    
    print(f"掃描到 {len(tasks)} 項待執行任務，正在核對指令對接...")
    
    for task_id, task_name in tasks:
        # 匹配邏輯
        cmd = next((cmd for kw, cmd in mapping.items() if kw in task_name), None)
        
        if cmd:
            print(f"[模擬成功] 任務 [{task_id}] '{task_name}' -> 預計執行: {cmd}")
        else:
            print(f"[模擬失敗] 任務 [{task_id}] '{task_name}' -> 無對應指令，將被跳過。")
            
    conn.close()
    print("--- [Node D: 模擬運行程序結束，請確認上述指令流是否正確] ---")

if __name__ == "__main__":
    run_dry_run()