# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\RD_Center\SDK\System\goose_executor.py
# 狀態：已開發完成，負責 Goose AI 地端 Stage 3 & 4 物理執行與防禦

import os
import sys
import json
import sqlite3
import subprocess
from datetime import datetime

GENESIS_BASE = r"C:\Genesis"
LOCAL_DB = os.path.join(GENESIS_BASE, "Database", "Genesis_DFMEA.db")
CLOUD_DB = r"G:\我的雲端硬碟\ITE GEMINI Pro雲端指揮中心\memory_core_sync.db"
LOG_FILE = os.path.join(GENESIS_BASE, "Genesis_Core", "DFMEA_Monitor.log")

# 設定 stdout 與 stderr 保護，防範 Windows CP950 編碼崩潰
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(errors='replace')

def log_dfmea(level, module_name, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] [{level}] [{module_name}] {message}\n"
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_line)
    except Exception as e:
        print(f"Failed to write DFMEA log: {e}")

def update_task_status(task_id, status, error_msg=""):
    for db in [LOCAL_DB, CLOUD_DB]:
        if os.path.exists(db):
            try:
                conn = sqlite3.connect(db, timeout=5.0)
                conn.execute("PRAGMA journal_mode=WAL;")
                cur = conn.cursor()
                cur.execute("""
                    UPDATE Sync_Control_Table 
                    SET status = ? 
                    WHERE task_id = ?
                """, (status, task_id))
                
                # Insert event
                event_type = 'EXECUTION_SUCCESS' if status == 'COMPLETED' else 'EXECUTION_FAILED'
                inst_str = json.dumps({"error": error_msg}) if error_msg else "{}"
                cur.execute("""
                    INSERT INTO System_Events (event_type, instruction, status, timestamp)
                    VALUES (?, ?, ?, ?)
                """, (event_type, inst_str, status, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                
                conn.commit()
                conn.close()
            except Exception as e:
                print(f"Failed to update task status in {db}: {e}")

def run_goose_stages(task_id, brick_name):
    """
    Goose AI Ground Executor Bridge
    - Stage 3: Physical Script / command dispatching
    - Stage 4: Run-time telemetry check, post-execution check & DFMEA logging
    """
    print(f"\n=== [Goose AI Ground Executor: Task {task_id}] ===")
    
    # 搜尋積木路徑
    bricks_dir = os.path.join(GENESIS_BASE, "RD_Center", "SDK_Bricks")
    found_path = None
    for root, _, files in os.walk(bricks_dir):
        for f in files:
            if f.lower() == brick_name.lower() or f.lower().replace(".py", "") == brick_name.lower().replace(".py", ""):
                found_path = os.path.join(root, f)
                break
        if found_path:
            break

    if not found_path:
        err_msg = f"找不到積木實體: {brick_name}"
        print(f"[❌ S3 失敗] {err_msg}")
        log_dfmea("ERROR", "Goose_Stage3", err_msg)
        update_task_status(task_id, "FAILED", err_msg)
        return False

    print(f"[+] S3 (Command): 尋獲積木 {found_path}，準備執行物理調度...")
    log_dfmea("INFO", "Goose_Stage3", f"Dispatching command: python {found_path}")

    # 執行積木
    try:
        proc = subprocess.run(
            [sys.executable, found_path],
            capture_output=True,
            text=True,
            timeout=15.0
        )
        stdout = proc.stdout
        stderr = proc.stderr
        exit_code = proc.returncode
    except subprocess.TimeoutExpired:
        err_msg = "積木執行逾時被強制熔斷 (Timeout: 15s)"
        print(f"[❌ S3 失敗] {err_msg}")
        log_dfmea("CRITICAL", "Goose_Stage3", err_msg)
        update_task_status(task_id, "FAILED", err_msg)
        return False
    except Exception as e:
        err_msg = f"積木啟動失敗: {e}"
        print(f"[❌ S3 失敗] {err_msg}")
        log_dfmea("ERROR", "Goose_Stage3", err_msg)
        update_task_status(task_id, "FAILED", err_msg)
        return False

    # Stage 4: 後端防禦、日誌審計與狀態報告
    print(f"[+] S4 (Monitor & Defense): 執行完畢，結果代碼: {exit_code}")
    
    if exit_code == 0:
        print("[+] S4 檢查成功：積木合規退出！")
        log_dfmea("SUCCESS", "Goose_Stage4", f"Execution successful for {brick_name}. Return code: 0")
        
        # 將 stdout 紀錄回 DFMEA 日誌中以便後續追蹤
        for line in stdout.splitlines():
            if line.strip():
                log_dfmea("STDOUT", brick_name.replace(".py", ""), line.strip())
                
        update_task_status(task_id, "COMPLETED")
        return True
    else:
        print(f"[❌ S4 警告] 積木回傳異常代碼: {exit_code}")
        log_dfmea("ERROR", "Goose_Stage4", f"Execution failed for {brick_name}. Return code: {exit_code}")
        if stderr.strip():
            log_dfmea("STDERR", brick_name.replace(".py", ""), stderr.strip())
            
        update_task_status(task_id, "FAILED", stderr.strip())
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python goose_executor.py <task_id> <brick_name>")
        sys.exit(1)
    
    run_goose_stages(sys.argv[1], sys.argv[2])
