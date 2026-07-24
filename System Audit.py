# Category: Security
import os
import datetime

# 檢查活動日誌，驗證自動化執行結果
log_path = r"C:\Genesis\activity.log"
engine_path = r"C:\Genesis\Management_Hub\Blueprint_Engine.py"

print(f"--- [系統時間: {datetime.datetime.now()}] ---")

# 1. 檢查藍圖引擎是否存在
if os.path.exists(engine_path):
    print(f"[OK] Blueprint_Engine 已實體化: {os.path.getsize(engine_path)} bytes")
else:
    print("[ERROR] 藍圖引擎缺失，自動化煉化未啟動")

# 2. 讀取最後一行日誌紀錄
if os.path.exists(log_path):
    with open(log_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        if lines:
            print(f"[LOG] 最後紀錄: {lines[-1].strip()}")
        else:
            print("[WARN] 日誌為空，程序可能掛起")
else:
    print("[ERROR] activity.log 未產生，部署未完成")