# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\RD_Center\SDK\System\Command_Dispatcher.py
# 狀態：已開發完成，負責地端網路感知、自動啟閉本地Telegram網關與雙向同步

import os
import sys
import time
import subprocess
import urllib.request

GENESIS_BASE = r"C:\Genesis"
SYNC_SCRIPT = os.path.join(GENESIS_BASE, "RD_Center", "SDK", "System", "Cloud_Bridge_Sync.py")
TG_GATEWAY = os.path.join(GENESIS_BASE, "RD_Center", "SDK", "System", "Telegram_Gateway.js")

class CommandDispatcher:
    def __init__(self):
        self.gateway_process = None
        self.is_running = True
        self.was_online = None

    def check_connectivity(self):
        """檢查地端網際網路與雲端磁碟連接狀態"""
        # 1. 檢查 Google Drive 雲端路徑
        cloud_dir = r"G:\我的雲端硬碟\ITE GEMINI Pro雲端指揮中心"
        if not os.path.exists(cloud_dir):
            return False

        # 2. 檢查網際網路
        try:
            urllib.request.urlopen("https://www.google.com", timeout=3.0)
            return True
        except Exception:
            return False

    def is_gateway_running_globally(self):
        """用 cmd 檢索是否有執行中的 Telegram_Gateway.js 進程"""
        try:
            # 檢索執行命令列中帶有 Telegram_Gateway 的 node 程式
            out = subprocess.run(
                ['wmic', 'process', 'where', "name='node.exe'", 'get', 'CommandLine', '/format:list'],
                capture_output=True, text=True, errors='ignore'
            )
            return "Telegram_Gateway" in out.stdout
        except Exception:
            return False

    def kill_local_gateway(self):
        """終止本地 Telegram 網關進程，防止長輪詢衝突 (409 Conflict)"""
        # A. 終止 Python 管理的 Process
        if self.gateway_process:
            try:
                self.gateway_process.terminate()
                self.gateway_process.wait(timeout=2.0)
                print("[Dispatcher] 本地 Telegram 網關進程已被成功終止。")
            except Exception:
                pass
            self.gateway_process = None

        # B. 保險起見，利用 taskkill 強制終止任何執行中的 Telegram_Gateway.js node 進程
        try:
            # 尋找 CommandLine 中有 Telegram_Gateway 的進程 ID 並強制結束
            proc_query = subprocess.run(
                ['wmic', 'process', 'where', "name='node.exe'", 'get', 'processid,commandline'],
                capture_output=True, text=True, errors='ignore'
            )
            for line in proc_query.stdout.splitlines():
                if "Telegram_Gateway" in line:
                    parts = line.strip().split()
                    if parts:
                        pid = parts[-1]
                        subprocess.run(['taskkill', '/F', '/PID', pid], capture_output=True)
                        print(f"[Dispatcher] 已強制結束殘留的網關進程 (PID: {pid})")
        except Exception:
            pass

    def start_local_gateway(self):
        """啟動本地 Telegram 網關"""
        if self.is_gateway_running_globally():
            print("[Dispatcher] 本地 Telegram 網關已經在背景運行中。")
            return
        
        try:
            print("[Dispatcher] 正在啟動本地 Telegram 網關...")
            self.gateway_process = subprocess.Popen(
                ["node", TG_GATEWAY],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print("[Dispatcher] 本地 Telegram 網關啟動成功。")
        except Exception as e:
            print(f"[❌] 啟動本地 Telegram 網關失敗: {e}")

    def trigger_sync(self):
        """調用 Cloud_Bridge_Sync.py 進行資料庫雙向對齊與發送心跳"""
        try:
            subprocess.run([sys.executable, SYNC_SCRIPT], check=True)
        except Exception as e:
            print(f"[警告] 調度資料庫同步失敗: {e}")

    def run(self):
        print("==========================================================")
        print("      Genesis Cloud-Ground Command Dispatcher Online      ")
        print("      Active-Passive Failover Coordination: ACTIVE        ")
        print("==========================================================")

        while self.is_running:
            is_online = self.check_connectivity()

            if is_online:
                if self.was_online is False or self.was_online is None:
                    print("[+] 系統檢測：網際網路與雲端指揮部連線已建立！(ONLINE)")
                    
                    # 1. 優先進行一次資料庫同步，將雲端離線時寫入的指令同步回來
                    self.trigger_sync()
                    
                    # 2. 頂真緩衝：等待 5 秒，讓雲端 Agent 看到 heartbeat 已更新並主動關閉其 polling，避免 409 衝突
                    print("[Dispatcher] 等待 5 秒讓雲端大腦釋放長輪詢權限...")
                    time.sleep(5)
                    
                    # 3. 啟動本地 Telegram 網關
                    self.start_local_gateway()
                else:
                    # 常規運作：定時同步並確保本地網關正常
                    self.trigger_sync()
                    if not self.is_gateway_running_globally():
                        self.start_local_gateway()

                self.was_online = True
            else:
                if self.was_online is True or self.was_online is None:
                    print("[!] 系統檢測：地端網路已中斷或無法連接雲端指揮部！(OFFLINE)")
                    # 立即終止地端 Telegram 網關，讓雲端安全接管
                    self.kill_local_gateway()

                self.was_online = False

            # 每 10 秒檢查一次
            time.sleep(10)

if __name__ == "__main__":
    dispatcher = CommandDispatcher()
    try:
        dispatcher.run()
    except KeyboardInterrupt:
        print("\nDispatcher shutdown.")
        dispatcher.kill_local_gateway()
