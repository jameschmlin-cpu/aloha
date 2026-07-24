# C:\Genesis\Management_Hub\Gemini_Command_Center.py
import sys
import os


# 絕對路徑掛載
BASE_DIR = r"C:\Genesis"
if BASE_DIR not in sys.path: sys.path.insert(0, BASE_DIR)

from Engine.Orchestrator import Agent_Orchestrator

class Gemini_Command_Center:
    def __init__(self):
        self.orchestrator = Agent_Orchestrator()
    
    def run_task(self, task_id, cmd):
        print(f"[總管決策] 收到任務 {task_id}，正在啟動協同作業...")
        # [關鍵修正]：這裡才是真正「呼叫功能」的地方
        # 我現在主動將任務轉發給 Engine 底下的 Orchestrator 進行邏輯運算
        try:
            result = self.orchestrator.dispatch(task_id, cmd)
            print(f"[作業結果] {result}")
        except Exception as e:
            print(f"[作業失敗] 邏輯呼叫異常: {e}")

    def update_engine_logic(self, new_config):
        """[邏輯修改指令]：直接修改 Engine 的底層行為配置"""
        print(f"[指令介入] 正在修改後端邏輯配置...")
        # 這裡直接呼叫繼承的修改方法，而非僅回傳
        self.orchestrator.engine_core.set_config(new_config)
        print(f"[系統確認] 邏輯配置已更新為: {new_config}")

    def execute_and_modify(self, task_id, logic_hook):
        """[呼叫與繼承]：執行任務並在過程中注入自定義邏輯"""
        print(f"[指令下達] 啟動任務 {task_id}，掛載邏輯 Hook...")
        # 繼承自 Orchestrator 的邏輯修改指令
        return self.orchestrator.dispatch_with_override(task_id, logic_hook)

     def register_new_task(file_name, priority):
    """[總管指令] 自動將任務納入啟動清單"""
    config_path = r"C:\Genesis\Database\Startup_Registry.json"
    with open(config_path, 'r+') as f:
        data = json.load(f)
        data[file_name] = {"priority": priority, "path": f"C:\\Genesis\\Engine\\{file_name}", "status": "active"}
        f.seek(0)
        json.dump(data, f, indent=4)
    print(f"[系統] 任務 {file_name} 已成功納入啟動清單 (優先級: {priority})")

if __name__ == "__main__":
    cc = Gemini_Command_Center()
    # 測試：執行一個邏輯修改指令
    cc.update_engine_logic({"security_mode": "STRICT", "debug": False})
    
    # 測試：呼叫任務處理並注入邏輯邏輯
    status = cc.execute_and_modify("SYS_CORE_002", "RUN_QC_CHECK")