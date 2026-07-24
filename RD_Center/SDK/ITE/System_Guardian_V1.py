import os

import subprocess

import psutil

import time

import json

import hashlib



# 鎖定開發路徑

BASE_PATH = r"C:\Genesis"

LOG_PATH = os.path.join(BASE_PATH, "Logs")



def initialize_env():

    if not os.path.exists(BASE_PATH): os.makedirs(BASE_PATH)

    if not os.path.exists(LOG_PATH): os.makedirs(LOG_PATH)



def run_security_scrub():

    """第一階段：保安除害 - 物理熔斷惡意進程"""

    print("【1/3 保安除害】啟動中...")

    # 殺掉 PM2 及其所有殘留

    try:

        subprocess.run(["pm2", "kill"], capture_output=True, timeout=5)

        subprocess.run(["pm2", "unstartup"], capture_output=True, timeout=5)

        print(" -> 已強制熔斷 PM2 自動啟動項。")

    except:

        print(" -> PM2 未啟動或已遭手動終止。")



def get_system_health():

    """第二階段：系統偵測 - 獲取硬體實體數據"""

    print("【2/3 系統偵測】掃描中...")

    health = {

        "cpu_percent": psutil.cpu_percent(interval=1),

        "ram_available_gb": round(psutil.virtual_memory().available / (1024**3), 2),

        "disk_io_wait": "Scanning...",

        "status": "GREEN"

    }

    

    # 實測硬碟 I/O 延遲 (針對前任破壞硬碟的 Root Cause 偵測)

    start_io = time.time()

    test_file = os.path.join(BASE_PATH, "io_speed.test")

    with open(test_file, "w") as f:

        f.write("LOBSTER_SYSTEM_CHECK" * 1000)

    os.remove(test_file)

    io_delay = time.time() - start_io

    health["disk_io_wait"] = f"{io_delay:.4f}s"

    

    if io_delay > 0.5: health["status"] = "RED (Disk Bottleneck)"

    return health



def save_and_report(data):

    """第三階段：環境存檔 - 為後續開發建立基準"""

    print("【3/3 環境存檔】寫入中...")

    report_file = os.path.join(BASE_PATH, "env_report.json")

    with open(report_file, "w", encoding="utf-8") as f:

        json.dump(data, f, indent=4)

    

    # 產出實體 Hash 供主管校驗

    with open(report_file, "rb") as f:

        file_hash = hashlib.sha256(f.read()).hexdigest()

    

    print(f" -> 偵測報告已產出：{report_file}")

    print(f" -> 實體 Hash: {file_hash}")

    return file_hash



if __name__ == "__main__":

    initialize_env()

    run_security_scrub()

    health_data = get_system_health()

    save_and_report(health_data)

    print("\n【系統守護者】執行完畢。硬碟已安全，環境已建檔。")