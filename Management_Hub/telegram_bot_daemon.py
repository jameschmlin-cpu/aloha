# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\Management_Hub\telegram_bot_daemon.py
# 狀態：手機版 Telegram 雙向控制自癒與警報推播守護進程 (零依賴版)

import os
import json
import time
import sys
import urllib.request
import urllib.parse
import subprocess
import sqlite3

GENESIS_BASE = r"C:\Genesis"
CONFIG_FILE = os.path.join(GENESIS_BASE, "Config", "telegram_config.json")
AUDIT_LOG = os.path.join(GENESIS_BASE, "Logs", "patch_audit.log")
DFMEA_LOG = os.path.join(GENESIS_BASE, "Genesis_Core", "DFMEA_Monitor.log")

# 1. 載入設定檔
def load_config():
    if not os.path.exists(CONFIG_FILE):
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        default = {"bot_token": "YOUR_BOT_TOKEN_FROM_BOTFATHER", "authorized_chat_id": 0}
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(default, f, indent=4)
        return default
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"bot_token": "YOUR_BOT_TOKEN_FROM_BOTFATHER", "authorized_chat_id": 0}

def save_config(config):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        print(f"Error saving config: {e}")

config = load_config()
BOT_TOKEN = config.get("bot_token", "")
AUTH_CHAT_ID = config.get("authorized_chat_id", 0)

# Try importing GeminiAgent
try:
    sys.path.insert(0, os.path.join(GENESIS_BASE, "RD_Center"))
    sys.path.insert(0, os.path.join(GENESIS_BASE, "RD_Center", "SDK"))
    sys.path.insert(0, os.path.join(GENESIS_BASE, "RD_Center", "SDK", "AI_Core"))
    from Gemini_Agent import GeminiAgent
    agent_instance = GeminiAgent()
except Exception as e:
    agent_instance = None
    print(f"[Warning] Failed to import GeminiAgent in daemon: {e}")

# Telegram Bot API 封裝
def send_telegram_request(method, payload):
    if not BOT_TOKEN or "YOUR_BOT_TOKEN" in BOT_TOKEN:
        return None
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/{method}"
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=10) as res:
            return json.loads(res.read().decode('utf-8'))
    except Exception as e:
        print(f"Telegram API Error ({method}): {e}")
        return None

def send_message(chat_id, text):
    print(f"[TG Outbox] Sending to {chat_id}: {text[:50]}...")
    return send_telegram_request("sendMessage", {"chat_id": chat_id, "text": text})

# 獲取硬體與自癒狀態 (對接 nvidia-smi 與 psutil)
def get_system_status():
    status = "🟢 GENESIS SYSTEM HEALTHY\n\n"
    
    # 1. GPU Real Telemetry
    gpu_info = "GPU: NVIDIA RTX 3060 (Simulated)"
    try:
        proc = subprocess.run(
            ["nvidia-smi", "--query-gpu=temperature.gpu,utilization.gpu,memory.used,fan.speed", "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=1.5
        )
        if proc.returncode == 0:
            parts = [p.strip() for p in proc.stdout.strip().split(',')]
            if len(parts) >= 4:
                gpu_info = f"🖥️ GPU: RTX 3060\n  - Temp: {parts[0]}°C\n  - Load: {parts[1]}%\n  - VRAM: {round(float(parts[2])/1024, 1)}GB/12GB\n  - Fan: {parts[3]}%"
    except Exception:
        pass
    
    # 2. CPU / RAM load
    cpu_info = "CPU Load: Unknown"
    ram_info = "RAM Usage: Unknown"
    try:
        import psutil
        cpu_info = f"⚙️ CPU Load: {psutil.cpu_percent()}%"
        ram_info = f"💾 RAM Usage: {psutil.virtual_memory().percent}%"
    except ImportError:
        pass
        
    # 3. SQLite Connection Health
    db_info = "📁 SQLite DB: UNKNOWN"
    db_path = os.path.join(GENESIS_BASE, "Database", "Genesis_DFMEA.db")
    if os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path, timeout=2.0)
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM dfmea_matrix")
            count = cur.fetchone()[0]
            db_info = f"📁 SQLite DB: ONLINE ({count} rules registered)"
            conn.close()
        except Exception as e:
            db_info = f"📁 SQLite DB: ERROR ({e})"
    else:
        db_info = "📁 SQLite DB: MISSING"

    return f"{status}{gpu_info}\n{cpu_info}\n{ram_info}\n{db_info}\n\nType /list_bricks to see executable tasks."

# 列出 SDK_Bricks
def list_bricks():
    bricks_dir = os.path.join(GENESIS_BASE, "RD_Center", "SDK_Bricks")
    if not os.path.exists(bricks_dir):
        return "❌ Bricks directory not found."
    
    found = []
    for root, _, files in os.walk(bricks_dir):
        for f in files:
            if f.endswith(".py"):
                rel_path = os.path.relpath(os.path.join(root, f), bricks_dir)
                found.append(rel_path)
    if not found:
        return "📁 No logic bricks found in SDK_Bricks."
    
    res = "📦 Executable Logic Bricks:\n"
    for idx, name in enumerate(found, 1):
        res += f"{idx}. {name}\n"
    res += "\nUse /run_brick <name> to execute."
    return res

# 執行積木
def run_brick(brick_name):
    brick_name = brick_name.strip()
    if not brick_name:
        return "❌ Usage: /run_brick <brick_name_or_file.py>"
        
    bricks_dir = os.path.join(GENESIS_BASE, "RD_Center", "SDK_Bricks")
    found_path = None
    
    # 搜尋積木檔案
    for root, _, files in os.walk(bricks_dir):
        for f in files:
            if f.lower() == brick_name.lower() or f.lower().replace(".py", "") == brick_name.lower().replace(".py", ""):
                found_path = os.path.join(root, f)
                break
        if found_path:
            break
            
    if not found_path:
        return f"❌ Brick '{brick_name}' not found."
        
    send_message(AUTH_CHAT_ID, f"🚀 Executing logic brick: {os.path.basename(found_path)}...")
    
    try:
        proc = subprocess.run([sys.executable, found_path], capture_output=True, text=True, timeout=15.0)
        output = f"📥 [Execution Exit Code: {proc.returncode}]\n\n"
        if proc.stdout:
            output += f"Stdout:\n{proc.stdout}\n"
        if proc.stderr:
            output += f"Stderr:\n{proc.stderr}\n"
        return output
    except Exception as e:
        return f"❌ Subprocess crash: {e}"

# 處理收到的訊息
def handle_message(msg):
    global AUTH_CHAT_ID
    chat = msg.get("chat", {})
    chat_id = chat.get("id")
    text = msg.get("text", "").strip()
    
    if not text:
        return

    # 初次註冊機制
    if AUTH_CHAT_ID == 0:
        AUTH_CHAT_ID = chat_id
        config["authorized_chat_id"] = chat_id
        save_config(config)
        send_message(chat_id, "🔐 Welcome to Genesis! Your Chat ID has been successfully registered as Owner.")
        
    if chat_id != AUTH_CHAT_ID:
        # 拒絕非管理者的控制
        print(f"[Warning] Unauthorized request from Chat ID {chat_id}: {text}")
        return

    if text.startswith("/start"):
        send_message(chat_id, "🧠 Genesis Mobile AI Coordinator is online.\nCommands:\n/status - Query system health\n/list_bricks - List executable bricks\n/run_brick <name> - Dispatch a logic brick")
    elif text.startswith("/status"):
        send_message(chat_id, get_system_status())
    elif text.startswith("/list_bricks"):
        send_message(chat_id, list_bricks())
    elif text.startswith("/run_brick"):
        parts = text.split(" ", 1)
        if len(parts) < 2:
            send_message(chat_id, "❌ Usage: /run_brick <brick_name>")
        else:
            send_message(chat_id, run_brick(parts[1]))
    else:
        # 自然語言交由 AI 大腦處理
        send_message(chat_id, f"📝 Received query: '{text}'. Routing to AI Coordinator...")
        
        conversational_answer = ""
        success = False
        if agent_instance:
            try:
                # Fetch basic telemetry
                telemetry = {}
                try:
                    import psutil
                    telemetry = {
                        "cpu": f"{psutil.cpu_percent()}%",
                        "ram": f"{psutil.virtual_memory().percent}%"
                    }
                except ImportError:
                    pass
                    
                decision = agent_instance.execute_free_instruction(text, telemetry)
                conversational_answer = decision.get("conversational_answer", "")
                if decision.get("response_type") == "ACTION":
                    brick_name = decision.get("target_brick")
                    if brick_name:
                        run_res = run_brick(brick_name)
                        conversational_answer += f"\n\n[Action Triggered]\n- Target Brick: {brick_name}\n- Execution Result:\n{run_res}"
                success = True
            except Exception as e:
                print(f"Daemon AI execution error: {e}")
                
        if not success:
            # Fallback to simple matching
            matched_brick = None
            if "手臂" in text or "運動" in text or "move" in text:
                matched_brick = "Robot_Movement"
            elif "採樣" in text or "感測" in text or "sensor" in text:
                matched_brick = "Sensor_Sampling"
                
            if matched_brick:
                send_message(chat_id, f"🎯 Matched Brick: {matched_brick}. Triggering run...")
                send_message(chat_id, run_brick(matched_brick))
            else:
                send_message(chat_id, "❓ Unknown query. Type /status to query system or /list_bricks to see all tasks.")
        else:
            send_message(chat_id, conversational_answer)

# 4. 主動警報推播監視器
class LogMonitor:
    def __init__(self):
        self.log_files = [AUDIT_LOG, DFMEA_LOG]
        self.last_positions = {}
        for lf in self.log_files:
            if os.path.exists(lf):
                self.last_positions[lf] = os.path.getsize(lf)
            else:
                self.last_positions[lf] = 0

    def check_new_warnings(self):
        if AUTH_CHAT_ID == 0:
            return
            
        for lf in self.log_files:
            if not os.path.exists(lf):
                continue
                
            curr_size = os.path.getsize(lf)
            last_pos = self.last_positions.get(lf, 0)
            
            if curr_size > last_pos:
                try:
                    with open(lf, "r", encoding="utf-8", errors="ignore") as f:
                        f.seek(last_pos)
                        new_lines = f.readlines()
                        
                    for line in new_lines:
                        line_upper = line.upper()
                        # 當偵測到警告或異常字詞，主動推播至手機 Telegram
                        if "WARNING" in line_upper or "ERROR" in line_upper or "CRITICAL" in line_upper or "FATAL" in line_upper:
                            send_message(AUTH_CHAT_ID, f"🚨 [System Alert Push]\n{line.strip()}")
                except Exception as e:
                    print(f"Error checking logs: {e}")
                self.last_positions[lf] = curr_size

# 5. 主程序長輪詢 Loop
def start_polling():
    print("==========================================================")
    print("      Genesis Mobile Telegram Bot Daemon Running          ")
    print("==========================================================")
    
    if not BOT_TOKEN or "YOUR_BOT_TOKEN" in BOT_TOKEN:
        print("[Error] Please configure your real Bot Token in C:\\Genesis\\Config\\telegram_config.json")
        return
        
    last_update_id = 0
    log_monitor = LogMonitor()
    
    while True:
        # 1. 檢查是否有新日誌警報
        log_monitor.check_new_warnings()
        
        # 2. 獲取 Telegram 訊息 (長輪詢 2 秒)
        payload = {"timeout": 2, "allowed_updates": ["message"]}
        if last_update_id > 0:
            payload["offset"] = last_update_id + 1
            
        res = send_telegram_request("getUpdates", payload)
        if res and res.get("ok"):
            updates = res.get("result", [])
            for u in updates:
                update_id = u.get("update_id")
                last_update_id = max(last_update_id, update_id)
                
                message = u.get("message")
                if message:
                    handle_message(message)
                    
        time.sleep(1)

if __name__ == "__main__":
    try:
        start_polling()
    except KeyboardInterrupt:
        print("\nShutdown.")
