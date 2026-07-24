import json
import os
import sqlite3
from datetime import datetime

# ==========================================
# 核心實體路徑定錨
# ==========================================
BASE_PATH = r"C:\Genesis"
DB_PATH = os.path.join(BASE_PATH, "Database", "Lobster_Connectivity.db")
REGISTRY_FILE = os.path.join(BASE_PATH, "SDK", "Registry.json")

class LobsterTaskScheduler:
    """
    龍蝦系統中層核心第 8 號 Class
    專職負責 103 模組的本地虛擬掛載與定時排程調度，嚴禁外部 Tasks API，全在地端閉迴路運行。
    """
    def __init__(self):
        self.db_path = DB_PATH
        self.registry_path = REGISTRY_FILE

    def write_scheduler_telemetry(self, task_id: str, status: str, detail: str):
        """標準化排程日誌落地，永久鎖定於 SQLite 行車記錄器"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO connectivity_logs (timestamp, task_name, status, detail)
                VALUES (?, ?, ?, ?)
            ''', (timestamp, f"[Task_Scheduler] {task_id}", status, detail))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[SCHEDULER_DB_FATAL] {e}")

    def mount_local_virtual_task(self, task_name: str, scheduled_time: str, target_module: str) -> dict:
        """
        中層剛性核心邏輯：
        將 103 模組的排程任務『虛擬掛載』於本地端，驗證目標模組狀態並排入執行鏈。
        """
        task_id = "TSK_" + datetime.now().strftime("%Y%m%d%H%M%S")
        self.write_scheduler_telemetry(task_id, "MOUNT_INIT", f"開始本地虛擬掛載任務: {task_name}")

        # 1. 物理安全查驗：Registry 存在性
        if not os.path.exists(self.registry_path):
            self.write_scheduler_telemetry(task_id, "MOUNT_FAIL", "找不到 Registry 檔案")
            return {"status": "TECHNICAL_RESTRAINT", "reason": "系統設定未定錨"}

        with open(self.registry_path, 'r', encoding='utf-8') as f:
            registry = json.load(f)

        # 2. 閉迴路校驗：確認目標模組是否已登記在名冊中
        if target_module not in registry.get("components", {}):
            fail_msg = f"技術瓶頸：排程調度失敗，目標模組 {target_module} 尚未與中層 SDK 完成實體咬合。"
            self.write_scheduler_telemetry(task_id, "MOUNT_REJECTED", fail_msg)
            return {
                "status": "TECHNICAL_RESTRAINT",
                "task_id": task_id,
                "message": fail_msg
            }

        # 3. 虛擬掛載成功，封裝排程合約
        task_contract = {
            "task_id": task_id,
            "task_name": task_name,
            "target_module": target_module,
            "execution_policy": "LOCAL_VIRTUAL_MOUNT", # 剛性定錨本地
            "scheduled_at": scheduled_time,
            "mounted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        success_detail = f"排程任務 {task_name} 成功虛擬掛載於 C:\\ITE。預計執行時間: {scheduled_time}"
        self.write_scheduler_telemetry(task_id, "MOUNT_PASS", success_detail)
        
        return {
            "status": "TASK_MOUNTED",
            "task_id": task_id,
            "contract": task_contract
        }

if __name__ == "__main__":
    scheduler = LobsterTaskScheduler()
    
    print("\n" + "="*60)
    print(" 龍蝦帝國：中層第 8 號 Class Task_Scheduler 本地掛載測試 ")
    print("="*60)
    
    # 實體模擬：虛擬掛載每日 15:00 的『誠信掃描任務』到行政模組上
    result = scheduler.mount_local_virtual_task(
        task_name="DAILY_INTEGRITY_SCAN_1500",
        scheduled_time="15:00:00",
        target_module="ACT_001_ADMIN_SALARY"
    )
    
    print(f"本地排程掛載狀態: {result['status']}")
    if "task_id" in result:
        print(f"生成本地排程識別碼: {result['task_id']}")
    print(f"實體掛載合約內容:\n{json.dumps(result.get('contract', {}), indent=4, ensure_ascii=False)}")
    print("="*60 + "\n")