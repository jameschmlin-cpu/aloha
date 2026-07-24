# C:\Genesis\Headquarter\RD\Audit_Monitor.py
import time
import os

class AuditMonitor:
    def __init__(self):
        self.log_path = r"C:\Genesis\Headquarter\Logs\Empire_Audit.log"
        # 確保日誌目錄與檔案存在
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        if not os.path.exists(self.log_path):
            with open(self.log_path, 'w') as f:
                f.write("[System] Audit Log Initialized.\n")

    def watch(self):
        print(f"[AuditMonitor] 正在監控節點軌跡: {self.log_path}")
        print("--- 帝國審計視窗已開啟 (按 Ctrl+C 退出) ---")
        
        # 移動到檔案末尾，開始監控
        with open(self.log_path, "r", encoding="utf-8") as f:
            f.seek(0, os.SEEK_END)
            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.5) # 降低 CPU 佔用
                    continue
                # 實時輸出審計紀錄
                print(f"[Audit_Node_Event] {line.strip()}")

if __name__ == "__main__":
    monitor = AuditMonitor()
    try:
        monitor.watch()
    except KeyboardInterrupt:
        print("\n[System] 審計視窗已關閉。")