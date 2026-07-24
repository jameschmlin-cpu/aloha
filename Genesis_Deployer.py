import sqlite3
import yaml
import subprocess
import os
import sys

# --- 1. 物理路徑鎖定 ---
GENESIS_PATH = r"C:\Genesis"
if os.path.exists(GENESIS_PATH):
    os.chdir(GENESIS_PATH)
    sys.path.append(GENESIS_PATH)
else:
    print(f"致命錯誤：核心路徑 {GENESIS_PATH} 不存在。")
    sys.exit(1)

# 設定參數
DB_PATH = os.path.join(GENESIS_PATH, "Database", "Genesis_Tasks.db")
YAML_PATH = os.path.join(GENESIS_PATH, "Database", "tasks_mapping.yaml")
LOG_DIR = os.path.join(GENESIS_PATH, "logs")

# 嘗試掛載核心邏輯模組
try:
    from Genesis_Local_Brain import get_ai_cmd
except ImportError:
    def get_ai_cmd(task_name): return None

def execute_command(command, timeout=15):
    """診斷型執行器：包含超時中斷機制"""
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, 
            encoding='utf-8', errors='replace', timeout=timeout
        )
        return True, result.stdout
    except subprocess.TimeoutExpired:
        return False, f"任務執行逾時 ({timeout}s, 已自動跳過)"
    except Exception as e:
        return False, str(e)

def run_deployment():
    if not os.path.exists(YAML_PATH):
        print(f"錯誤: 找不到 {YAML_PATH}")
        return

    with open(YAML_PATH, "r", encoding="utf-8") as f:
        mapping = yaml.safe_load(f).get("tasks_mapping", {})
    
    # 使用 WAL 模式開啟連線[cite: 2]
    conn = sqlite3.connect(DB_PATH, timeout=60)
    conn.execute("PRAGMA journal_mode=WAL;")
    cursor = conn.cursor()
    cursor.execute("SELECT id, task_name FROM tasks WHERE status = 'PENDING'")
    tasks = cursor.fetchall()
    
    success_count = 0
    fail_count = 0
    
    for task_id, task_name in tasks:
        # 動態 Timeout 設定：87 與 93 任務給予 60 秒緩衝
        current_timeout = 60 if task_id in [87, 93] else 15
        
        print(f"\n正在處理: [{task_id}] {task_name} (Timeout: {current_timeout}s)")
        cmd = mapping.get(task_name) or mapping.get(str(task_id))
        if not cmd: cmd = get_ai_cmd(task_name)
            
        if not cmd:
            print("-> 跳過: 無對應執行指令")
            fail_count += 1
            continue

        # 執行指令
        success, output = execute_command(cmd, timeout=current_timeout)
        
        if success:
            with sqlite3.connect(DB_PATH, timeout=60) as update_conn:
                update_conn.execute("UPDATE tasks SET status = 'COMPLETED' WHERE id = ?", (task_id,))
            success_count += 1
            print(f"-> 成功: {task_name}")
            
            if not os.path.exists(LOG_DIR): os.makedirs(LOG_DIR)
            with open(os.path.join(LOG_DIR, f"task_{task_id}.log"), "w", encoding="utf-8") as log:
                log.write(output)
        else:
            fail_count += 1
            print(f"-> 失敗: {output.strip()}")

    conn.close()

    # --- Node D 品質報告 ---
    print("\n" + "="*40)
    print("部署執行報告 (Node D QC Audit):")
    print(f"任務完成數: {success_count} | 失敗/跳過: {fail_count}")
    print("執行狀態: [完成] - 已針對特定任務延長執行時限。")
    print("="*40)

if __name__ == "__main__":
    run_deployment()