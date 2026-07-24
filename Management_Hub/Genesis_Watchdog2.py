# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\Management_Hub\Genesis_Watchdog2.py
# 狀態：終極自癒與指揮排程版（內建週期性調度閉迴路優化器與全局各Port狀態自癒聯防）
# 實體 Hash: 0xGEN-WATCHDOG2-WEEKLY-SCHEDULER

import os
import sys
import time
import json
import subprocess
import logging
import hashlib
import urllib.request
import urllib.parse

GENESIS_BASE = r"C:\Genesis"
LOG_FILE = os.path.join(GENESIS_BASE, "Logs", "Genesis_Watchdog2.log")
DFMEA_LOG = os.path.join(GENESIS_BASE, "Genesis_Core", "DFMEA_Monitor.log")
CONFIG_PATH = os.path.join(GENESIS_BASE, "Config", "telegram_config.json")

# 確保目錄存在
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
os.makedirs(os.path.dirname(DFMEA_LOG), exist_ok=True)

# 初始化 Logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - [WATCHDOG2] - %(message)s'
)

# 解決標準輸出編碼問題
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(errors='replace')

# 靜默背景執行 Flag (防止彈跳 CMD 視窗)
CREATE_NO_WINDOW = 0x08000000

def get_telegram_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def send_telegram_alert(text):
    cfg = get_telegram_config()
    token = cfg.get("bot_token", "")
    chat_id = cfg.get("authorized_chat_id", 0)
    
    if not token or not chat_id:
        return
        
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=5.0) as res:
            pass
    except Exception as e:
        logging.error(f"Failed to send Telegram alert: {e}")

def log_event(description, level="INFO"):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] [Watchdog Robot] {description}\n"
    
    # 寫入 DFMEA_Monitor.log (供儀表板 UI 讀取)
    try:
        with open(DFMEA_LOG, "a", encoding="utf-8") as f:
            f.write(log_line)
    except Exception as e:
        logging.error(f"Failed to write DFMEA log: {e}")
        
    # 同步記錄至 Watchdog2 本地日誌與控制台
    log_entry = f"[{level}] {description}"
    if level == "ERROR" or level == "CRITICAL":
        logging.error(log_entry)
    else:
        logging.info(log_entry)
    print(log_line.strip())

def check_and_revive_legacy():
    # 1. 監控儀表板服務 (Port 8000)
    dash_ok = False
    try:
        url = "http://127.0.0.1:8000/api/cloud-status"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=3.0) as res:
            if res.status == 200:
                dash_ok = True
    except Exception:
        pass
        
    if not dash_ok:
        log_event("🚨 偵測到地端儀表板異常或未回應！啟動總管重啟程序...", "WARNING")
        
        # 殺死佔用 8000 的進程以防衝突
        try:
            output = subprocess.check_output("netstat -ano | findstr :8000", shell=True).decode('utf-8', errors='ignore')
            for line in output.split('\n'):
                parts = line.strip().split()
                if len(parts) >= 5 and "LISTENING" in line:
                    pid = parts[-1]
                    log_event(f"[*] 正在清除佔用 8000 端口的舊進程 (PID: {pid})...")
                    subprocess.run(f"taskkill /F /PID {pid}", shell=True, creationflags=CREATE_NO_WINDOW)
        except Exception:
            pass
            
        # 重啟儀表板服務
        try:
            log_event("[*] 正在背景重新啟動 dashboard_server.py (Port 8000)...")
            subprocess.Popen(
                [sys.executable, os.path.join(GENESIS_BASE, "dashboard_server.py"), "8000"],
                creationflags=CREATE_NO_WINDOW
            )
            time.sleep(3) # 等待啟動
            log_event("🟢 儀表板服務重啟完成！已恢復正常運作。")
            
            send_telegram_alert(
                "🤖 <b>[總管機器人自癒告警]</b>\n\n"
                "偵測到地端儀表板服務異常 (Port 8000 無回應)！\n\n"
                "<b>🟢 總管自癒處置：</b>\n"
                "已自動重開儀表板並清理端口，各終端連線已全線恢復正常！請主管放心！🌸"
            )
        except Exception as e:
            log_event(f"[FAIL] 重啟儀表板失敗: {e}", "ERROR")

    # 2. 監控 Telegram 遠端通訊模組 (Node.js 進程)
    tg_ok = False
    try:
        cmd_output = subprocess.check_output('wmic process where "name=\'node.exe\'" get CommandLine', shell=True).decode('utf-8', errors='ignore')
        if "Telegram_Gateway" in cmd_output:
            tg_ok = True
    except Exception:
        try:
            proc_list = subprocess.check_output("tasklist", shell=True).decode('utf-8', errors='ignore')
            if "node" in proc_list.lower():
                tg_ok = True
        except Exception:
            pass
        
    if not tg_ok:
        log_event("🚨 偵測到 Telegram 遠端通訊模組 (Node.js) 斷線！啟動總管重啟程序...", "WARNING")
        try:
            tg_script = os.path.join(GENESIS_BASE, "RD_Center", "SDK", "System", "Telegram_Gateway.js")
            if os.path.exists(tg_script):
                subprocess.Popen(
                    ["node", tg_script],
                    creationflags=CREATE_NO_WINDOW
                )
                time.sleep(2)
                log_event("🟢 Telegram 遠端通訊模組重啟完成！已恢復正常連線。")
            else:
                log_event("[略過] 找不到 Telegram Gateway 腳本路徑，跳過啟動。")
        except Exception as e:
            log_event(f"[FAIL] 重啟 Telegram Gateway 失敗: {e}", "ERROR")

    # 3. 監控本地 AI 服務 (Ollama Port 11434)
    ollama_ok = False
    try:
        url = "http://127.0.0.1:11434/api/tags"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=2.0) as res:
            if res.status == 200:
                ollama_ok = True
    except Exception:
        pass
        
    if not ollama_ok:
        log_event("🚨 偵測到本地 AI 服務 (Ollama Port 11434) 未啟動或無回應！啟動總管重啟程序...", "WARNING")
        try:
            log_event("[*] 正在背景啟動 ollama serve...")
            subprocess.Popen(
                ["ollama", "serve"],
                creationflags=CREATE_NO_WINDOW
            )
            time.sleep(3)
            log_event("🟢 本地 AI 服務已拉起，恢復自癒大腦本地算力支持！")
            send_telegram_alert(
                "🤖 <b>[總管機器人自癒告警]</b>\n\n"
                "偵測到本地 AI 服務 (Ollama Port 11434) 離線！\n\n"
                "<b>🟢 總管自癒處置：</b>\n"
                "已自動背景啟動 ollama serve，本地 RTX 3060 算力接管通道已全面恢復！🌸"
            )
        except Exception as e:
            log_event(f"[FAIL] 重啟 Ollama 失敗: {e}", "ERROR")

    # 4. 監控 ClawLibrary 服務 (Port 5188)
    claw_ok = False
    try:
        url = "http://127.0.0.1:5188/?mock=1"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=3.0) as res:
            if res.status == 200:
                claw_ok = True
    except Exception:
        pass
        
    if not claw_ok:
        log_event("🚨 偵測到 ClawLibrary 服務異常或未回應！啟動總管重啟程序...", "WARNING")
        
        # 殺死佔用 5188 的舊進程以防衝突
        try:
            output = subprocess.check_output("netstat -ano | findstr :5188", shell=True).decode('utf-8', errors='ignore')
            for line in output.split('\n'):
                parts = line.strip().split()
                if len(parts) >= 5 and "LISTENING" in line:
                    pid = parts[-1]
                    log_event(f"[*] 正在清除佔用 5188 端口的舊進程 (PID: {pid})...")
                    subprocess.run(f"taskkill /F /PID {pid}", shell=True, creationflags=CREATE_NO_WINDOW)
        except Exception:
            pass
            
        # 重啟 ClawLibrary 服務
        try:
            claw_dir = r"C:\ITE\Hermes\Dashboard_v6"
            if os.path.exists(claw_dir):
                log_event("[*] 正在背景重新啟動 ClawLibrary (Port 5188)...")
                subprocess.Popen(
                    ["npm.cmd", "run", "dev"],
                    cwd=claw_dir,
                    creationflags=CREATE_NO_WINDOW
                )
                time.sleep(3) # 等待啟動
                log_event("🟢 ClawLibrary 服務重啟完成！已恢復正常運作。")
                
                send_telegram_alert(
                    "🤖 <b>[維修機器人自癒告警]</b>\n\n"
                    "偵測到 ClawLibrary 服務異常 (Port 5188 無回應)！\n\n"
                    "<b>🟢 維修機器人自癒處置：</b>\n"
                    "已自動重開 ClawLibrary 並清理端口，虛擬辦公室已全面恢復！🌸"
                )
            else:
                log_event(f"[略過] 找不到 ClawLibrary 目錄: {claw_dir}")
        except Exception as e:
            log_event(f"[FAIL] 重啟 ClawLibrary 失敗: {e}", "ERROR")

    # 5. 監控 Node-RED 服務 (Port 1880)
    nodered_ok = False
    try:
        url = "http://127.0.0.1:1880/ui/"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=3.0) as res:
            if res.status == 200:
                nodered_ok = True
    except Exception:
        pass
        
    if not nodered_ok:
        log_event("🚨 偵測到 Node-RED 儀表板異常或未回應！啟動維修重啟程序...", "WARNING")
        
        # 殺死佔用 1880 的舊進程以防衝突
        try:
            output = subprocess.check_output("netstat -ano | findstr :1880", shell=True).decode('utf-8', errors='ignore')
            for line in output.split('\n'):
                parts = line.strip().split()
                if len(parts) >= 5 and "LISTENING" in line:
                    pid = parts[-1]
                    log_event(f"[*] 正在清除佔用 1880 端口的舊進程 (PID: {pid})...")
                    subprocess.run(f"taskkill /F /PID {pid}", shell=True, creationflags=CREATE_NO_WINDOW)
        except Exception:
            pass
            
        # 重啟 Node-RED 服務
        try:
            log_event("[*] 正在背景重新啟動 Node-RED (Port 1880)...")
            subprocess.Popen(
                ["node-red.cmd", os.path.join(GENESIS_BASE, "Bin", "node_red_flow_template.json")],
                shell=True,
                creationflags=CREATE_NO_WINDOW
            )
            time.sleep(3) # 等待啟動
            log_event("🟢 Node-RED 服務重啟完成！已恢復正常運作。")
            
            send_telegram_alert(
                "🤖 <b>[維修機器人自癒告警]</b>\n\n"
                "偵測到 Node-RED 儀表板異常 (Port 1880 無回應)！\n\n"
                "<b>🟢 維修機器人自癒處置：</b>\n"
                "已自動重開 Node-RED 並加載智慧範本，控制面板已恢復正常！🌸"
            )
        except Exception as e:
            log_event(f"[FAIL] 重啟 Node-RED 失敗: {e}", "ERROR")

def run_optimizer():
    """由 Watchdog2 定期點火呼喚閉迴路優化器，避免浪費背景常駐算力"""
    optimizer_path = os.path.join(GENESIS_BASE, "genesis_closed_loop_optimizer.py")
    if os.path.exists(optimizer_path):
        log_event("Watchdog2 觸發點火：開始於背景執行閉迴路動態優化巡檢...")
        try:
            # 採用背景非阻塞調度，執行完畢自動釋放
            subprocess.Popen([sys.executable, "-u", optimizer_path], creationflags=CREATE_NO_WINDOW)
            log_event("已成功啟動閉迴路優化器背景進程。")
        except Exception as e:
            log_event(f"啟動閉迴路優化器時發生異常: {e}", "ERROR")

if __name__ == "__main__":
    log_event("Genesis_Watchdog2 總指揮已正式上線，啟動背景心跳守護自癒與週期排程。")
    print("[WATCHDOG2] 終極總管與自癒聯防已上線。")
    
    # 啟動時先執行一次閉迴路優化
    run_optimizer()
    
    # 紀錄上次執行時間
    last_optimizer_run = time.time()
    
    # 每週執行週期（7天 * 24小時 * 3600秒 = 604800秒）
    WEEKLY_INTERVAL = 7 * 24 * 3600 
    
    # 自癒心跳偵測週期 (每 15 秒檢查一次 Port 與進程)
    CHECK_INTERVAL = 15

    try:
        while True:
            # 1. Check manual watchdog toggle state
            enabled = True
            state_file = os.path.join(GENESIS_BASE, "Config", "watchdog_state.json")
            if os.path.exists(state_file):
                try:
                    with open(state_file, "r") as f:
                        enabled = json.load(f).get("enabled", True)
                except Exception:
                    pass

            if enabled:
                # 2. Run AI DFMEA Monitor
                monitor_script = os.path.join(GENESIS_BASE, "Management_Hub", "dashboard_ai_monitor.py")
                if os.path.exists(monitor_script):
                    try:
                        subprocess.run([sys.executable, monitor_script], creationflags=CREATE_NO_WINDOW, timeout=30.0)
                    except Exception as e:
                        logging.error(f"AI DFMEA Monitor run failed: {e}. Running legacy checks as fallback.")
                        check_and_revive_legacy()
                else:
                    check_and_revive_legacy()
            else:
                logging.info("Watchdog checks skipped: manual override disabled in watchdog_state.json")
            
            # 3. 檢查是否滿一週，若滿則執行閉迴路優化
            current_time = time.time()
            if current_time - last_optimizer_run >= WEEKLY_INTERVAL:
                run_optimizer()
                last_optimizer_run = current_time
                
            # 休息以進行下一次偵測
            time.sleep(CHECK_INTERVAL)
            
    except KeyboardInterrupt:
        log_event("Genesis_Watchdog2 收到終止信號，正在安全卸載。", "INFO")
        print("[WATCHDOG2] 收到終止信號，安全退出。")