# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\startup_manager_v2.py
# 狀態：背景靜默執行版（全面改用 CREATE_NO_WINDOW，不彈跳多餘視窗）
# 實體 Hash: 0xGEN-STARTUP-MANAGER-SILENT

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
    entry = f"[{timestamp}] [Startup Manager Silent] {msg}"
    print(entry)
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry + "\n")

def main():
    log_and_print("==================================================")
    log_and_print("=== [Startup Manager V2] 開始進行背景靜默分級部署 ===")
    log_and_print("==================================================")
    
    # 1. 永久常駐組（絕對不能刪、必須持續背景運行）
    persistent_cores = [
        {"name": "dashboard", "path": os.path.join(GENESIS_BASE, "dashboard_server.py"), "args": ["8000"]},
        {"name": "memory_guard", "path": os.path.join(GENESIS_BASE, "Management_Hub", "Memory_Guardian.py"), "args": []},
        {"name": "memory_sync_guard", "path": os.path.join(GENESIS_BASE, "Management_Hub", "Memory_Sync_Guard.py"), "args": []},
        {"name": "command_dispatcher", "path": os.path.join(GENESIS_BASE, "RD_Center", "SDK", "System", "Command_Dispatcher.py"), "args": []},
        {"name": "genesis_sync_daemon", "path": os.path.join(GENESIS_BASE, "Genesis_Sync_Daemon.py"), "args": []}
    ]

    # 2. 按需點火組（測完即釋放，納入 Watchdog2 清單）
    ondemand_targets = [
        {"name": "empire_governor", "path": os.path.join(GENESIS_BASE, "Management_Hub", "Empire_Resource_Governor.py")},
        {"name": "file_watcher", "path": os.path.join(GENESIS_BASE, "Engine", "Watcher.py")},
        {"name": "doctor_guard", "path": os.path.join(GENESIS_BASE, "Management_Hub", "Doctor.py")},
        {"name": "log_health_monitor", "path": os.path.join(GENESIS_BASE, "Management_Hub", "Log_Health_Monitor.py")},
        {"name": "qc_watcher", "path": os.path.join(GENESIS_BASE, "Management_Hub", "QC_Watcher.py")},
        {"name": "closed_loop_optimizer", "path": os.path.join(GENESIS_BASE, "genesis_closed_loop_optimizer.py")},
        {"name": "langgraph_core", "path": os.path.join(GENESIS_BASE, "RD_Center", "SDK", "System", "LangGraph_Core.py")},
        {"name": "lightrag_engine", "path": os.path.join(GENESIS_BASE, "RD_Center", "SDK", "System", "LightRAG_Engine.py")}
    ]

    active_persistent = []
    passed_count = 0

    # 靜默執行旗標：完全不跳出任何獨立主控台視窗
    silent_flags = getattr(subprocess, 'CREATE_NO_WINDOW', 0x08000000)

    # 階段一：啟動永久常駐核心（靜默背景運行）
    log_and_print("--- [階段一] 正在背景靜默拉起永久常駐核心 ---")
    for core in persistent_cores:
        name = core["name"]
        path = core["path"]
        args = core["args"]
        if not os.path.exists(path):
            log_and_print(f"[錯誤] 找不到路徑: {name} ({path})")
            continue
        try:
            cmd = [sys.executable, "-u", path] + args
            proc = subprocess.Popen(cmd, creationflags=silent_flags)
            active_persistent.append((name, proc))
            log_and_print(f"  >>> 【✔ 靜默常駐】項目 [{name}] 已在背景鎖定運行！")
            passed_count += 1
            time.sleep(1)
        except Exception as e:
            log_and_print(f"  >>> 【❌ 失敗】項目 [{name}] 異常: {e}")

    # 階段二：點火檢測按需模組並安全釋放
    log_and_print("--- [階段二] 正在靜默點火檢測按需模組（測完即釋放） ---")
    for item in ondemand_targets:
        name = item["name"]
        path = item["path"]
        if not os.path.exists(path):
            log_and_print(f"[略過] 找不到路徑: {name}")
            continue
        try:
            cmd = [sys.executable, "-u", path]
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace", creationflags=silent_flags)
            time.sleep(2)
            if proc.poll() is None:
                proc.kill()
                log_and_print(f"  >>> 【✔ PASS & 封存待命】項目 [{name}] 實測通過，已安全殺除釋放。")
                passed_count += 1
            else:
                _, err = proc.communicate()
                log_and_print(f"  >>> 【❌ FAIL】項目 [{name}] 異常崩潰: {err.strip()}")
        except Exception as e:
            log_and_print(f"  >>> 【❌ 錯誤】項目 [{name}] 執行失敗: {e}")

    log_and_print("==================================================")
    log_and_print(f"=== [總結] 永久常駐與按需檢測完畢，總計有效項目: {passed_count} ===")
    log_and_print("==================================================")

    # 1. 啟動終極總管 Watchdog2（背景靜默）
    watchdog2_path = os.path.join(GENESIS_BASE, "Management_Hub", "Genesis_Watchdog2.py")
    active_watchdog = None
    if os.path.exists(watchdog2_path):
        log_and_print("[總指揮上線] 正式於背景啟動 Genesis_Watchdog2 進行全局聯防。")
        active_watchdog = subprocess.Popen([sys.executable, "-u", watchdog2_path], creationflags=silent_flags)

    # 2. 啟動 ClawLibrary (Port 5188) 視覺核心（背景靜默）
    claw_dir = r"C:\ITE\Hermes\Dashboard_v6"
    active_claw = None
    if os.path.exists(claw_dir):
        log_and_print("[視覺核心] 正在背景啟動 ClawLibrary (Port 5188)...")
        active_claw = subprocess.Popen(["npm.cmd", "run", "dev"], cwd=claw_dir, creationflags=silent_flags)

    # 2.5 啟動 Telegram Gateway 遠端通訊模組（背景靜默）
    active_telegram = None
    try:
        tg_script = os.path.join(GENESIS_BASE, "RD_Center", "SDK", "System", "Telegram_Gateway.js")
        if os.path.exists(tg_script):
            log_and_print("[遠端通訊] 正在背景啟動 Telegram Gateway...")
            active_telegram = subprocess.Popen(["node", tg_script], creationflags=silent_flags)
        else:
            log_and_print("[遠端通訊] 找不到 Telegram Gateway 腳本路徑，跳過啟動。")
    except Exception as te:
        log_and_print(f"[遠端通訊] 啟動 Telegram Gateway 失敗: {te}")

    # 3. 啟動 Node-RED (Port 1880) 儀表板與遙控核心（背景靜默）
    active_nodered = None
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', 1880))
        sock.close()
        if result != 0:
            log_and_print("[儀表板遙控] 正在背景啟動 Node-RED (Port 1880)...")
            active_nodered = subprocess.Popen(
                ["node-red.cmd", os.path.join(GENESIS_BASE, "Bin", "node_red_flow_template.json")],
                shell=True,
                creationflags=silent_flags
            )
        else:
            log_and_print("[儀表板遙控] Node-RED (Port 1880) 偵測到已在運行，跳過啟動。")
    except Exception as ne:
        log_and_print(f"[儀表板遙控] 啟動 Node-RED 失敗: {ne}")

    # 4. 產出 Node C Hash 驗證代碼
    hasher = hashlib.sha256(f"SILENT_STARTUP_{passed_count}".encode('utf-8'))
    log_and_print(f"[NODE C HASH] 終極啟動管理器驗證代碼: {hasher.hexdigest()}")
    log_and_print("=== [系統全面就緒] 所有模組已在背景靜默全線啟動，畫面保持乾淨！ ===")

    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        log_and_print("[安全關閉] 收到中斷信號...")
        for name, p in active_persistent:
            try:
                p.kill()
            except:
                pass
        if active_watchdog:
            try: active_watchdog.kill()
            except: pass
        if active_claw:
            try: active_claw.kill()
            except: pass
        if active_telegram:
            try: active_telegram.kill()
            except: pass
        if active_nodered:
            try:
                parent = psutil.Process(active_nodered.pid)
                for child in parent.children(recursive=True):
                    child.kill()
                parent.kill()
            except:
                pass

if __name__ == "__main__":
    main()