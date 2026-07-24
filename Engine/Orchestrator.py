# C:\Genesis\Engine\Orchestrator.py
import sqlite3
import os

class Agent_Orchestrator:
    def __init__(self):
        # [路徑修正] 強制指向統一資料庫位置
        self.db_path = r"C:\Genesis\Database\Path_Database.db"
        self.engine_core = Engine_Core()

    def get_path(self, module_name):
        """從統一資料庫獲取模組路徑"""
        if not os.path.exists(self.db_path):
            return None
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT physical_path FROM path_map WHERE module_name = ?", (module_name,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None

    def dispatch(self, task_id, cmd):
        return f"任務 {task_id} 已執行，參數: {cmd}"

    def dispatch_with_override(self, task_id, logic_hook):
        print(f"[Engine] 正在執行任務 {task_id}，掛載 Hook: {logic_hook}")
        return True

class Engine_Core:
    def set_config(self, new_config):
        print(f"[Engine] 配置已更新: {new_config}")