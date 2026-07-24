# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\Management_Hub\Empire_Resource_Governor.py
# 實體 Hash: f9d4c2b7e5a8f1d4c6b9e2a7f3d5c8b1e4f6d9a2b8f4d1c9e6a2b5f7d3c8e1a4

import psutil
import time
import os
import sys
import subprocess

# 核心路徑錨定
GENESIS_BASE = r"C:\Genesis"
TELEGRAM_GATEWAY = os.path.join(GENESIS_BASE, "RD_Center", "SDK", "System", "Telegram_Gateway.js")
CONNECTOR_PATH = os.path.join(GENESIS_BASE, "RD_Center", "Source", "Option", "Stage_1")

if CONNECTOR_PATH not in sys.path:
    sys.path.append(CONNECTOR_PATH)

from DB_Connector import GenesisDBFactory

# 用於追蹤初始狀態
initialized = False

def notify_all(message):
    try:
        GenesisDBFactory.write_data("state", {"node_name": "Resource_Governor", "state_val": message})
        subprocess.Popen(["node", TELEGRAM_GATEWAY, "--msg", message])
    except Exception as e:
        print(f"[憲法異常] 通知失敗: {e}")

def scan_and_regulate():
    global initialized
    try:
        mem = psutil.virtual_memory()
        usage = mem.percent
        
        # 僅在啟動第一次時顯示狀態，後續進入靜音監控模式
        if not initialized:
            print(f"[Empire Resource Governor] 初始 RAM 狀態監測中: {usage}%")
            initialized = True
        
        if usage > 85.0:
            # 僅在異常時才強制輸出提醒
            print(f"[Empire Resource Governor] 警告: 高負載狀態 {usage}%")
            msg = f"CRITICAL_RAM_USAGE_{usage}%"
            notify_all(msg)
            
            # 物理肅清
            target_procs = ["msedgewebview2.exe", "chrome.exe"]
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] in target_procs:
                    proc.terminate()
            
            py_procs = []
            for p in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if p.info['name'] == 'python.exe':
                        cmdline = p.info['cmdline']
                        if cmdline:
                            cmdline_str = " ".join(cmdline).lower()
                            is_core = any(x in cmdline_str for x in [
                                "startup_manager", "resource_governor", "memory_guardian", 
                                "memory_sync_guard", "watcher.py", "command_center", 
                                "doctor.py", "dashboard_server", "command_dispatcher", 
                                "sync_daemon", "health_monitor", "watchdog", "qc_watcher"
                            ])
                            if not is_core:
                                py_procs.append(p)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            for p in py_procs:
                try:
                    p.terminate()
                except Exception:
                    pass
                
    except Exception as e:
        print(f"治理異常: {e}")

if __name__ == "__main__":
    while True:
        scan_and_regulate()
        time.sleep(2)