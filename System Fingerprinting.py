import platform
import psutil
import os
import json

def get_system_fingerprint():
    """執行主機環境特徵掃描 ( Fingerprinting )"""
    data = {
        "os": platform.platform(),
        "cpu_cores": psutil.cpu_count(),
        "ram_total": psutil.virtual_memory().total,
        "disk_info": [{"device": p.device, "mountpoint": p.mountpoint} for p in psutil.disk_partitions()],
        "env_vars": dict(os.environ), # 獲取所有系統參數
        "python_path": sys.path
    }
    # 物理抽樣並儲存，這是模擬器的基礎參數
    with open(r"C:\Genesis\System_Fingerprint.json", "w") as f:
        json.dump(data, f, indent=4)
    print("🟢 [PHYSICAL_SCAN] 物理環境特徵已抽樣並落檔 (System_Fingerprint.json)")

get_system_fingerprint()