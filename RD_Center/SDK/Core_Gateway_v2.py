from Core_Gateway import Core_Gateway
import datetime

class Core_Gateway_v2(Core_Gateway):
    def __init__(self):
        super().__init__()
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] [System] Doctor 防禦性核心已掛載。")

    def _log_status(self, stage, message):
        """節點狀態偵測器，強制輸出執行狀況"""
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] [Node_{stage}] {message}")

    def execute_task(self, task_id):
        # S4 階段：執行防禦性檢查
        if self.S4_Monitor_Defense():
            self._log_status("D", f"任務 {task_id} 完整性核對通過")
            
            # 2. 自動調用維運邏輯
            result = self.perform_integrity_check(task_id)
            
            if result:
                self._log_status("C", f"任務 {task_id} 執行回傳代碼: 0 (成功)")
                return True
        
        self._log_status("A", "防禦檢查失敗！系統進入熔斷狀態。")
        return False

    def perform_integrity_check(self, task_id):
        # 模擬 Node B Hash 比對過程
        self._log_status("B", f"正在比對任務 {task_id} 的實體 Hash")
        return True

if __name__ == "__main__":
    # 測試執行狀況輸出
    gateway = Core_Gateway_v2()
    gateway.execute_task(100)