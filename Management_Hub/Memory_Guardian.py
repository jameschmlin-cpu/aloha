# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\Management_Hub\Memory_Guardian.py
import sys
import time
import psutil 

# [核心閉鎖]：強行鎖定系統搜尋路徑，絕不遺漏
CONNECTOR_PATH = r"C:\Genesis\RD_Center\Source\Option\Stage_1"
if CONNECTOR_PATH not in sys.path:
    sys.path.append(CONNECTOR_PATH)

from DB_Connector import GenesisDBFactory

def get_real_usage():
    """獲取真實硬體使用率"""
    process = psutil.Process()
    # 邏輯判斷：計算佔用率，而非單純的記憶體大小
    return psutil.virtual_memory().percent / 100

def monitor():
    print("[SYSTEM] 記憶守護程序啟動：路徑已錨定，邏輯閉鎖中。")
    while True:
        try:
            usage = get_real_usage()
            # 判斷邏輯：到達 85% 臨界點
            if usage >= 0.85:
                # 執行防護措施
                try:
                    GenesisDBFactory.write_data("unified", {
                        "union_id": "CRITICAL_STATE", 
                        "payload": "MEMORY_OVERFLOW_SHUTDOWN"
                    })
                    print("[FATAL] 記憶飽和，已執行閉鎖寫入。")
                except Exception as db_err:
                    # 備援判斷：若資料庫掛掉，確保寫入備援 Log
                    with open(r"C:\Genesis\Logs\emergency_crash.log", "a") as f:
                        f.write(f"FATAL: {db_err}\n")
                break 
            
            time.sleep(10)
            
        except Exception as e:
            print(f"[ERROR] 監控迴圈異常: {e}")
            time.sleep(5)

if __name__ == "__main__":
    monitor()