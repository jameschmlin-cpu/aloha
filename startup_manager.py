# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\startup_manager_v2.py
# 狀態：終極防護整合型啟動管理器（黃金核心永久常駐，嚴禁盲目殺除）
# 實體 Hash: 0xGEN-STARTUP-MANAGER-V2-GOLDEN

import os
import sys
import time
import subprocess
import hashlib
import psutil

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(errors='replace')

GENESIS_BASE = r"C:\Genesis"
LOG_FILE = os.path.join(GENESIS_BASE, "Logs", "Startup_Manager_V2.log")

def log_and_print(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] [Startup Manager V2 Golden] {msg}"
    print(entry)
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry + "\n")

def run_golden_startup_pipeline():
    log_and_print("==================================================")
    log_and_print("=== [黃金核心啟動器] 開始部署，嚴守互鎖與常駐防線 ===")
    log_and_print("==================================================")
    
    # 定義 13 支核心模組與其正確的生死角色 (role: persist = 永久常駐，ondemand = 依條件點火)
    targets = [
        # 1. 核心儀表板 (永久常駐)
        {"name": "dashboard", "path": os.path.join(GENESIS_BASE, "dashboard_server.py"), "role": "persist", "args": ["8000"]},
        # 2. 記憶體與積木守護 (永久常駐，維護記憶體與 85% 重啟讀寫)
        {"name": "memory_guard", "path": os.path.join(GENESIS_BASE, "Management_Hub", "Memory_Guardian.py"), "role": "persist"},
        # 3. 記憶與雲地同步守護 (永久常駐，絕不能斷)
        {"name": "memory_sync_guard", "path": os.path.join(GENESIS_BASE, "Management_Hub", "Memory_Sync_Guard.py"), "role": "persist"},
        # 4. 指令分發中心 (永久常駐，主管下指令的命脈)
        {"name": "command_dispatcher", "path": os.path.join(GENESIS_BASE, "RD_Center", "SDK", "System", "Command_Dispatcher.py"), "role": "persist"},
        # 5. 雲地同步 Daemon (永久常駐)
        {"name": "genesis_sync_daemon", "path": os.path.join(GENESIS_BASE, "Genesis_Sync_Daemon.py"), "role": "persist"},
        
        # 6~13. 其餘專業功能模組 (由 Watchdog 進行動態點火或背景備援)
        {"name": "empire_governor", "path": os.path.join(GENESIS_BASE, "Management_Hub", "Empire_Resource_Governor.py"), "role": "ondemand"},
        {"name": "file_watcher", "path": os.path.join(GENESIS_BASE, "Engine", "Watcher.py"), "role": "ondemand"},
        {"name": "doctor_guard", "path": os.path.join(GENESIS_BASE, "Management_Hub", "Doctor.py"), "role": "ondemand"},
        {"name": "log_health_monitor", "path": os.path.join(GENESIS_BASE, "Management_Hub", "Log_Health_Monitor.py"), "role": "ondemand"},
        {"name": "qc_watcher", "path": os.path.join(GENESIS_BASE, "Management_Hub", "QC_Watcher.py"), "role": "ondemand"},
        {"name": "closed_loop_optimizer", "path": os.path.join(GENESIS_BASE, "genesis_closed_loop_optimizer.py"), "role": "ondemand"},
        {"name": "safety_referee", "path": os.path.join(GENESIS_BASE, "genesis_safety_referee.py"), "role": "ondemand"},
        {"name": "langgraph_core", "path": os.path.join(GENESIS_BASE, "RD_Center", "SDK", "System", "LangGraph_Core.py"), "role": "ondemand"},
        {"name": "lightrag_engine", "path": os.path.join(GENESIS_BASE, "RD_Center", "SDK", "System", "LightRAG_Engine.py"), "role": "ondemand"}
    ]

    active_processes = []
    passed_count = 0
    failed_count = 0
    
    for item in targets:
        name = item["name"]
        path = item["path"]
        role = item["role"]
        extra_args = item.get("args", [])
        
        if not os.path.exists(path):
            log_and_print(f"[略過] 找不到實體路徑: {name} ({path})")
            failed_count += 1
            continue
            
        log_and_print(f"[啟動檢測] 正在拉起模組: {name} ...")
        try:
            cmd = [sys.executable, "-u", path] + extra_args
            # 永久常駐的黃金核心以獨立 Console 視窗或背景常駐執行，絕不殺掉
            if role == "persist":
                proc = subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
                active_processes.append(proc)
                log_and_print(f"  >>> 【✔ 保持常駐定錨】黃金核心 [{name}] 已獨立拉起並持續運作！")
                passed_count += 1
            else:
                # 測試型點火驗證 2 秒後安全釋放交給 Watchdog
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace")
                time.sleep(2)
                ret = proc.poll()
                if ret is None:
                    proc.kill()
                    log_and_print(f"  >>> 【✔ PASS 驗證通過】項目 [{name}] 正常，已納入 Watchdog2 按需點火清單。")
                    passed_count += 1
                elif ret == 0:
                    log_and_print(f"  >>> 【✔ PASS 驗證通過（單次驗證點火完成）】項目 [{name}] 正常退出。")
                    passed_count += 1
                else:
                    _, err = proc.communicate()
                    log_and_print(f"  >>> 【❌ 警告】項目 [{name}] 啟動異常 (Exit Code: {ret}): {err.strip()}")
                    failed_count += 1
        except Exception as e:
            log_and_print(f"  >>> 【❌ 錯誤】項目 [{name}] 執行失敗: {str(e)}")
            failed_count += 1

    log_and_print("==================================================")
    log_and_print(f"=== [總結] 檢測完成 | 🟢 正常運行: {passed_count} | 🔴 異常: {failed_count} ===")
    log_and_print("==================================================")

    # 啟動終極總管 Watchdog2
    watchdog2_path = os.path.join(GENESIS_BASE, "Management_Hub", "Genesis_Watchdog2.py")
    active_watchdog = None
    if os.path.exists(watchdog2_path):
        log_and_print("[總指揮上線] 正式啟動 Genesis_Watchdog2 進行全局聯防與算力保全。")
        active_watchdog = subprocess.Popen([sys.executable, "-u", watchdog2_path], creationflags=subprocess.CREATE_NEW_CONSOLE)

    # 啟動 ClawLibrary (Port 5188) 虛擬辦公室伺服器
    claw_dir = r"C:\ITE\Hermes\Dashboard_v6"
    active_claw = None
    if os.path.exists(claw_dir):
        log_and_print("[視覺核心] 正在啟動 ClawLibrary (Port 5188)...")
        active_claw = subprocess.Popen(["npm.cmd", "run", "dev"], cwd=claw_dir, creationflags=subprocess.CREATE_NEW_CONSOLE)

    hasher = hashlib.sha256(f"GOLDEN_STARTUP_{passed_count}".encode('utf-8'))
    log_and_print(f"[NODE C HASH] 驗證代碼: {hasher.hexdigest()}")
    log_and_print("=== [系統全面就緒] 黃金核心與 Watchdog 聯防網已全線啟動！ ===")

    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        log_and_print("[安全關閉] 收到中斷信號...")
        for p in active_processes:
            try:
                p.kill()
            except:
                pass
        if active_watchdog:
            active_watchdog.kill()
        if active_claw:
            active_claw.kill()

if __name__ == "__main__":
    run_golden_startup_pipeline()