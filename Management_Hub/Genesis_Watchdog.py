# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\Management_Hub\Genesis_Watchdog.py
# 狀態：總管機器人 (Watchdog Robot) - 負責背景監控儀表板與 Telegram 正常運作

import os
import sys
import time
import json
import subprocess
import urllib.request
import urllib.parse

GENESIS_BASE = r"C:\Genesis"
DFMEA_LOG = os.path.join(GENESIS_BASE, "Genesis_Core", "DFMEA_Monitor.log")
CONFIG_PATH = os.path.join(GENESIS_BASE, "Config", "telegram_config.json")

# 防止編碼崩潰
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(errors='replace')

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
        print(f"[Watchdog] Failed to send Telegram alert: {e}")

def log_event(description):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] [Watchdog Robot] {description}\n"
    try:
        with open(DFMEA_LOG, "a", encoding="utf-8") as f:
            f.write(log_line)
        print(log_line.strip())
    except Exception as e:
        print(f"[Watchdog] Log error: {e}")

def is_port_listening(port):
    """使用 netstat 檢查 Port 是否處於 LISTENING 狀態"""
    try:
        output = subprocess.check_output(f"netstat -ano | findstr LISTENING | findstr :{port}", shell=True)
        return len(output.strip()) > 0
    except Exception:
        return False

def check_and_revive():
    # 1. 監控儀表板服務 (Port 8000)
    dash_ok = False
    try:
        # 測試連線
        url = "http://127.0.0.1:8000/api/cloud-status"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=3.0) as res:
            if res.status == 200:
                dash_ok = True
    except Exception:
        pass
        
    if not dash_ok:
        log_event("🚨 偵測到地端儀表板異常或未回應！啟動總管重啟程序...")
        
        # 殺死佔用 8000 的 Python 進程以防衝突
        try:
            output = subprocess.check_output("netstat -ano | findstr :8000", shell=True).decode('utf-8', errors='ignore')
            for line in output.split('\n'):
                parts = line.strip().split()
                if len(parts) >= 5 and "LISTENING" in line:
                    pid = parts[-1]
                    log_event(f"[*] 正在清除佔用 8000 端口的舊進程 (PID: {pid})...")
                    subprocess.run(f"taskkill /F /PID {pid}", shell=True)
        except Exception:
            pass
            
        # 重啟儀表板服務
        try:
            log_event("[*] 正在背景重新啟動 dashboard_server.py (Port 8000)...")
            # 使用 subprocess.Popen 啟動，獨立執行緒
            subprocess.Popen(
                [sys.executable, os.path.join(GENESIS_BASE, "dashboard_server.py"), "8000"],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            time.sleep(3) # 等待啟動
            log_event("🟢 儀表板服務重啟完成！已恢復正常運作。")
            
            # 推播 Telegram 通知主管
            send_telegram_alert(
                "🤖 <b>[總管機器人自癒告警]</b>\n\n"
                "偵測到地端儀表板服務異常 (Port 8000 無回應)！\n\n"
                "<b>🟢 總管自癒處置：</b>\n"
                "已自動重開儀表板並清理端口，各終端連線已全線恢復正常！請主管放心！🌸"
            )
        except Exception as e:
            log_event(f"[FAIL] 重啟儀表板失敗: {e}")

    # 2. 監控 Telegram 遠端通訊模組 (Node.js 進程)
    tg_ok = False
    try:
        cmd_output = subprocess.check_output('wmic process where "name=\'node.exe\'" get CommandLine', shell=True).decode('utf-8', errors='ignore')
        if "Telegram_Gateway" in cmd_output:
            tg_ok = True
    except Exception:
        # Fallback to general node check if wmic fails
        try:
            proc_list = subprocess.check_output("tasklist", shell=True).decode('utf-8', errors='ignore')
            if "node" in proc_list.lower():
                tg_ok = True
        except Exception:
            pass
        
    if not tg_ok:
        log_event("🚨 偵測到 Telegram 遠端通訊模組 (Node.js) 斷線！啟動總管重啟程序...")
        try:
            tg_script = os.path.join(GENESIS_BASE, "RD_Center", "SDK", "System", "Telegram_Gateway.js")
            subprocess.Popen(
                ["node", tg_script],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            time.sleep(2)
            log_event("🟢 Telegram 遠端通訊模組重啟完成！已恢復正常連線。")
        except Exception as e:
            log_event(f"[FAIL] 重啟 Telegram Gateway 失敗: {e}")

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
        log_event("🚨 偵測到本地 AI 服務 (Ollama Port 11434) 未啟動或無回應！啟動總管重啟程序...")
        try:
            log_event("[*] 正在背景啟動 ollama serve...")
            subprocess.Popen(
                ["ollama", "serve"],
                creationflags=subprocess.CREATE_NEW_CONSOLE
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
            log_event(f"[FAIL] 重啟 Ollama 失敗: {e}")

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
        log_event("🚨 偵測到 ClawLibrary 服務異常或未回應！啟動總管重啟程序...")
        
        # 殺死佔用 5188 的舊進程以防衝突
        try:
            output = subprocess.check_output("netstat -ano | findstr :5188", shell=True).decode('utf-8', errors='ignore')
            for line in output.split('\n'):
                parts = line.strip().split()
                if len(parts) >= 5 and "LISTENING" in line:
                    pid = parts[-1]
                    log_event(f"[*] 正在清除佔用 5188 端口的舊進程 (PID: {pid})...")
                    subprocess.run(f"taskkill /F /PID {pid}", shell=True)
        except Exception:
            pass
            
        # 重啟 ClawLibrary 服務
        try:
            log_event("[*] 正在背景重新啟動 ClawLibrary (Port 5188)...")
            subprocess.Popen(
                ["npm.cmd", "run", "dev"],
                cwd=r"C:\ITE\Hermes\Dashboard_v6",
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            time.sleep(3) # 等待啟動
            log_event("🟢 ClawLibrary 服務重啟完成！已恢復正常運作。")
            
            # 推播 Telegram 通知主管
            send_telegram_alert(
                "🤖 <b>[維修機器人自癒告警]</b>\n\n"
                "偵測到 ClawLibrary 服務異常 (Port 5188 無回應)！\n\n"
                "<b>🟢 維修機器人自癒處置：</b>\n"
                "已自動重開 ClawLibrary 並清理端口，虛擬辦公室已全面恢復！🌸"
            )
        except Exception as e:
            log_event(f"[FAIL] 重啟 ClawLibrary 失敗: {e}")

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
        log_event("🚨 偵測到 Node-RED 儀表板異常或未回應！啟動維修重啟程序...")
        
        # 殺死佔用 1880 的舊進程以防衝突
        try:
            output = subprocess.check_output("netstat -ano | findstr :1880", shell=True).decode('utf-8', errors='ignore')
            for line in output.split('\n'):
                parts = line.strip().split()
                if len(parts) >= 5 and "LISTENING" in line:
                    pid = parts[-1]
                    log_event(f"[*] 正在清除佔用 1880 端口的舊進程 (PID: {pid})...")
                    subprocess.run(f"taskkill /F /PID {pid}", shell=True)
        except Exception:
            pass
            
        # 重啟 Node-RED 服務
        try:
            log_event("[*] 正在背景重新啟動 Node-RED (Port 1880)...")
            subprocess.Popen(
                ["node-red.cmd", os.path.join(GENESIS_BASE, "Bin", "node_red_flow_template.json")],
                shell=True,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            time.sleep(3) # 等待啟動
            log_event("🟢 Node-RED 服務重啟完成！已恢復正常運作。")
            
            # 推播 Telegram 通知主管
            send_telegram_alert(
                "🤖 <b>[維修機器人自癒告警]</b>\n\n"
                "偵測到 Node-RED 儀表板異常 (Port 1880 無回應)！\n\n"
                "<b>🟢 維修機器人自癒處置：</b>\n"
                "已自動重開 Node-RED 並加載智慧範本，控制面板已恢復正常！🌸"
            )
        except Exception as e:
            log_event(f"[FAIL] 重啟 Node-RED 失敗: {e}")


def main():
    log_event("🤖 [總管機器人監視服務已上線] 正在監護儀表板與 Telegram 功能...")
    while True:
        try:
            check_and_revive()
        except Exception as e:
            print(f"[Watchdog Loop Error] {e}")
        time.sleep(10)

if __name__ == "__main__":
    main()
