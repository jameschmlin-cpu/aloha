import time
import os
import datetime

class Genesis_Engine:
    def __init__(self, log_path):
        self.log_path = log_path
        self.running = True

    def log_event(self, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(log_entry)
            f.flush()
            os.fsync(f.fileno())

    def start_loop(self, task_callback):
        self.log_event(">>> [核心引擎] 引擎啟動，進入監控循環。")
        while self.running:
            # 執行傳入的產品任務
            task_callback()
            
            # DFMEA 檢查 (所有產品共用)
            if not os.path.exists(self.log_path):
                self.log_event("!!! [核心引擎] DFMEA 斷言失敗，觸發熔斷 !!!")
                break
            
            time.sleep(5)