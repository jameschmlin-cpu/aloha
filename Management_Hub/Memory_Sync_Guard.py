# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\Management_Hub\Memory_Sync_Guard.py
# 狀態：常駐守護模式 (已修正進程結束導致誤觸自癒之缺陷)

import hashlib
import os
import time
import logging
import sys
import threading

# --- 核心路徑設定 ---
# 確保路徑完全對齊 Protocol 規範
sys.path.append(r"C:\Genesis")
LOG_FILE = r'C:\Genesis\Logs\system_monitor.log'
MEMORY_PATH = r"C:\Genesis\SDK\memory"

# 設定日誌
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - [MEMORY_GUARD] - %(message)s'
)

def calculate_file_hash(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest().upper()

def monitor_loop():
    """監控迴圈邏輯"""
    while True:
        try:
            if os.path.exists(MEMORY_PATH):
                for filename in os.listdir(MEMORY_PATH):
                    file_path = os.path.join(MEMORY_PATH, filename)
                    if os.path.isfile(file_path):
                        actual_hash = calculate_file_hash(file_path)
                        logging.info(f"積木完整性核驗: {filename} | Hash: {actual_hash}")
            time.sleep(300)
        except Exception as e:
            logging.error(f"記憶監控發生中斷: {e}")
            time.sleep(10)

if __name__ == "__main__":
    # 啟動監控執行緒
    monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
    monitor_thread.start()
    
    logging.info("記憶中斷監控器已常駐啟動。")
    print("[SUCCESS] Memory Sync Guard initialized.")
    
    # [物理修正] 替換 sys.exit(0)，改以阻塞迴圈常駐，防止管理器誤判進程結束
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        logging.info("記憶監控器收到終止訊號，準備關閉。")
        sys.exit(0)