import sqlite3
import subprocess
import os
import time
import logging
from RD_Center.SDK.AI_Core.Gemini_Agent_Enhanced import GeminiAgentEnhanced
from RD_Center.SDK.Core_Gateway_v2 import Core_Gateway_v2

# 設定日誌歸檔
logging.basicConfig(
    filename=r"C:\Genesis\Logs\empire_operations.log",
    level=logging.INFO,
    format='%(asctime)s - [Node_D] - %(message)s'
)

class GenesisOrchestrator:
    def __init__(self):
        self.agent = GeminiAgentEnhanced()
        self.gateway = Core_Gateway_v2()
        self.db_path = r"C:\Genesis\Database\Genesis_Tasks.db"

    def apply_patch(self, task_id, code):
        """物理寫入層：使用專屬 Patch 路徑，並執行隔離驗證"""
        patch_path = os.path.join(r"C:\Genesis\Temp", f"patch_{task_id}.py")
        with open(patch_path, "w", encoding="utf-8") as f:
            f.write(code)
        
        # 執行並捕獲結果
        result = subprocess.run(["python", patch_path], capture_output=True, text=True)
        return result.returncode == 0, result.stderr

    def run_autonomous_cycle(self):
        """全自動化閉環維運"""
        print("[System] 帝國自治引擎：無人值守模式啟用...")
        
        while True: # 自動化監控循環
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT id, task_name FROM tasks WHERE status = 'PENDING'")
            tasks = cursor.fetchall()
            
            if not tasks:
                print("[System] 任務隊列清空，進入待機節能模式...")
                time.sleep(30)
                continue

            for task_id, task_name in tasks:
                try:
                    logging.info(f"開始處理任務 [{task_id}]: {task_name}")
                    
                    # 1. 認知與決策
                    decision = self.agent.execute_free_instruction(task_name)
                    
                    # 2. 物理校驗與防禦 (SDK 4 Stages)
                    if self.gateway.execute_task(task_id):
                        # 3. 物理執行與自動補丁
                        success, error = self.apply_patch(task_id, decision['patch_code'])
                        if success:
                            cursor.execute("UPDATE tasks SET status = 'COMPLETED' WHERE id = ?", (task_id,))
                            logging.info(f"任務 [{task_id}] 成功部署")
                        else:
                            logging.error(f"任務 [{task_id}] 執行失敗: {error}")
                            # 觸發自我修復 (Doctor)
                            self.trigger_self_healing(task_id)
                    else:
                        logging.warning(f"任務 [{task_id}] 未通過安全審核 (Node C 熔斷)")
                
                except Exception as e:
                    logging.critical(f"帝國引擎遇到嚴重崩潰: {str(e)}")
            
            conn.commit()
            conn.close()

    def trigger_self_healing(self, task_id):
        """觸發 Root Cause 分析與自動修復"""
        print("-> [Node C] 觸發自動故障排除 (Doctor)...")
        # 這裡可銜接您先前的 Doctor.py 邏輯
        subprocess.run(["python", r"C:\Genesis\Management_Hub\Doctor.py", "--fix", str(task_id)])

if __name__ == "__main__":
    engine = GenesisOrchestrator()
    engine.run_autonomous_cycle()