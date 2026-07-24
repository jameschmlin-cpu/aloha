# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\Management_Hub\dashboard_ai_monitor.py
# 狀態：AI 儀表板狀況監控與自癒引擎 - 對接 Genesis_DFMEA.db

import os
import sys
import json
import sqlite3
import socket
import subprocess
import time
from datetime import datetime
import urllib.request

# Setup paths
GENESIS_BASE = r"C:\Genesis"
sys.path.insert(0, os.path.join(GENESIS_BASE, "RD_Center", "SDK", "AI_Core"))
sys.path.insert(0, os.path.join(GENESIS_BASE, "RD_Center"))

# Import GeminiAgent
try:
    from Gemini_Agent import GeminiAgent
    agent = GeminiAgent()
except Exception as e:
    agent = None
    print(f"[Warning] Failed to import GeminiAgent in AI Monitor: {e}")

DB_PATH = os.path.join(GENESIS_BASE, "Database", "Genesis_DFMEA.db")
LOG_PATH = os.path.join(GENESIS_BASE, "Genesis_Core", "DFMEA_Monitor.log")
TG_CONFIG = os.path.join(GENESIS_BASE, "Config", "telegram_config.json")

def write_dfmea_log(message):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"[INFO] [{timestamp}] [AI DFMEA Monitor] {message}\n")
    except Exception as e:
        print(f"Failed to write log: {e}")

def send_telegram_push(text):
    if not os.path.exists(TG_CONFIG):
        return
    try:
        with open(TG_CONFIG, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        token = cfg.get("gemini_api_key", "")
        bot_token = cfg.get("bot_token", token)
        chat_id = cfg.get("authorized_chat_id", 0)
        
        if bot_token and chat_id:
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            payload = {"chat_id": chat_id, "text": text}
            req = urllib.request.Request(
                url, data=json.dumps(payload).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            with urllib.request.urlopen(req, timeout=5.0) as resp:
                pass
    except Exception as e:
        print(f"Failed to push Telegram alert: {e}")

def check_port(port):
    """Check if local port is active/listening."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1.0)
    try:
        s.connect(("127.0.0.1", port))
        s.close()
        return True
    except Exception:
        return False

def check_process_running(keyword):
    """Check if process matching keyword is running via wmic or tasklist."""
    try:
        output = subprocess.check_output('wmic process get CommandLine', shell=True).decode('utf-8', errors='ignore')
        if keyword in output:
            return True
    except Exception:
        pass
    try:
        output = subprocess.check_output('tasklist', shell=True).decode('utf-8', errors='ignore')
        if keyword.lower() in output.lower():
            return True
    except Exception:
        pass
    return False

def query_dfmea_rule(failure_id):
    if not os.path.exists(DB_PATH):
        return None
    try:
        conn = sqlite3.connect(DB_PATH, timeout=5.0)
        cur = conn.cursor()
        cur.execute("""
            SELECT id, problem_point, failure_mode, severity, occurrence, detection, root_cause, prevention, corrective 
            FROM dfmea_matrix WHERE id = ?
        """, (failure_id,))
        row = cur.fetchone()
        conn.close()
        if row:
            return {
                "id": row[0],
                "problem_point": row[1],
                "failure_mode": row[2],
                "severity": row[3],
                "occurrence": row[4],
                "detection": row[5],
                "root_cause": row[6],
                "prevention": row[7],
                "corrective": row[8]
            }
    except Exception as e:
        print(f"Error querying DFMEA rule: {e}")
    return None

def save_dfmea_rule(rule):
    try:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conn = sqlite3.connect(DB_PATH, timeout=5.0)
        conn.execute("PRAGMA journal_mode=WAL;")
        cur = conn.cursor()
        cur.execute("""
            INSERT OR REPLACE INTO dfmea_matrix 
            (id, problem_point, failure_mode, severity, occurrence, detection, root_cause, prevention, corrective)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            rule["id"], rule["problem_point"], rule["failure_mode"],
            int(rule.get("severity", 8)), int(rule.get("occurrence", 5)), int(rule.get("detection", 4)),
            rule["root_cause"], rule["prevention"], rule["corrective"]
        ))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving DFMEA rule: {e}")
        return False

def generate_ai_dfmea_rule(service_name, port_info):
    """Use GeminiAgent to dynamically generate a DFMEA matrix card."""
    if not agent:
        # Static fallback rule if agent is unavailable
        return {
            "id": f"ERR_{service_name.upper()}",
            "problem_point": f"{service_name} Offline",
            "failure_mode": f"Service port {port_info} is closed",
            "severity": 8,
            "occurrence": 5,
            "detection": 4,
            "root_cause": "Process crashed or port was bound by other programs",
            "prevention": "Verify watchdog loop active",
            "corrective": f"Restart {service_name} service script"
        }
    
    prompt = (
        f"A system failure has occurred: The service '{service_name}' on port/process '{port_info}' is OFFLINE.\n"
        f"Generate a DFMEA rule JSON strictly matching this schema:\n"
        f"{{\n"
        f"  \"id\": \"ERR_{service_name.upper()}\",\n"
        f"  \"problem_point\": \"{service_name} Port Offline\",\n"
        f"  \"failure_mode\": \"Brief failure description\",\n"
        f"  \"severity\": 8,\n"
        f"  \"occurrence\": 5,\n"
        f"  \"detection\": 4,\n"
        f"  \"root_cause\": \"Likely root cause details\",\n"
        f"  \"prevention\": \"Proposed preventive actions\",\n"
        f"  \"corrective\": \"Restart the service\"\n"
        f"}}\n"
        f"Note: severity, occurrence, and detection must be integers from 1 to 10."
    )
    
    try:
        res = agent.execute_free_instruction(prompt, {"service": service_name, "port": port_info})
        # If response has conversational_answer, check if we got JSON in patch_code or response_type
        # GeminiAgent schema contains parameters or patch_code. Let's try parsing raw text if it is structured JSON.
        if isinstance(res, dict):
            # Parse from conversational_answer or custom fields
            text = res.get("conversational_answer", "")
            if "{" in text and "}" in text:
                import re
                match = re.search(r"(\{.*\})", text, re.DOTALL)
                if match:
                    return json.loads(match.group(1))
            # Fallback to structured parameter check
            params = res.get("parameters", {})
            if params and "corrective" in params:
                return params
    except Exception as ex:
        print(f"Failed parsing AI generated DFMEA card: {ex}")
        
    return {
        "id": f"ERR_{service_name.upper()}",
        "problem_point": f"{service_name} Offline",
        "failure_mode": f"Service port {port_info} is closed",
        "severity": 8,
        "occurrence": 5,
        "detection": 4,
        "root_cause": "Process crashed or port was bound by other programs",
        "prevention": "Verify watchdog loop active",
        "corrective": f"Restart {service_name} service script"
    }

def execute_self_healing_action(service_name, corrective_action):
    write_dfmea_log(f"自癒引擎啟動: 執行 [ {corrective_action} ] 以修復 {service_name}")
    try:
        if service_name == "Dashboard":
            script = os.path.join(GENESIS_BASE, "dashboard_server.py")
            subprocess.Popen([sys.executable, script, "8000"], creationflags=0x08000000)
        elif service_name == "Node-RED":
            flow_file = os.path.join(GENESIS_BASE, "Bin", "node_red_flow_template.json")
            subprocess.Popen(f"node-red.cmd {flow_file}", shell=True, creationflags=0x08000000)
        elif service_name == "ClawLibrary":
            app_dir = r"C:\ITE\Hermes\Dashboard_v6"
            subprocess.Popen("npm run dev", shell=True, cwd=app_dir, creationflags=0x08000000)
        elif service_name == "Ollama":
            subprocess.Popen("ollama serve", shell=True, creationflags=0x08000000)
        elif service_name == "TelegramGateway":
            gateway_script = os.path.join(GENESIS_BASE, "RD_Center", "SDK", "System", "Telegram_Gateway.js")
            subprocess.Popen(f"node {gateway_script}", shell=True, creationflags=0x08000000)
        return True
    except Exception as e:
        write_dfmea_log(f"自癒執行異常: {e}")
        return False

def run_telemetry_scan():
    services_to_check = [
        {"name": "Dashboard", "port": 8000, "desc": "Port 8000"},
        {"name": "Node-RED", "port": 1880, "desc": "Port 1880"},
        {"name": "ClawLibrary", "port": 5188, "desc": "Port 5188"},
        {"name": "Ollama", "port": 11434, "desc": "Port 11434"},
        {"name": "TelegramGateway", "port": None, "keyword": "Telegram_Gateway.js", "desc": "Process Node"}
    ]
    
    for srv in services_to_check:
        is_alive = False
        if srv["port"] is not None:
            is_alive = check_port(srv["port"])
        else:
            is_alive = check_process_running(srv["keyword"])
            
        if not is_alive:
            failure_id = f"ERR_{srv['name'].upper()}"
            write_dfmea_log(f"⚠️ 偵測到服務異常: {srv['name']} 斷線/無回應！")
            
            # Query DFMEA matrix for matching rule
            rule = query_dfmea_rule(failure_id)
            is_new = False
            
            if not rule:
                is_new = True
                write_dfmea_log(f"🔍 查無資料庫防禦規則 {failure_id}，啟動 AI 智能推導分析中...")
                rule = generate_ai_dfmea_rule(srv["name"], srv["desc"])
                save_dfmea_rule(rule)
                write_dfmea_log(f"💾 AI 已成功註冊新 DFMEA 規則至 Genesis_DFMEA.db")
            
            rpn = int(rule.get("severity", 8)) * int(rule.get("occurrence", 5)) * int(rule.get("detection", 4))
            
            # Send Telegram Alert
            alert_text = (
                f"🌸 親愛的雋懋主管您好！志玲系統告警：\n\n"
                f"🚨 偵測到 [{srv['name']}] 服務心跳中斷！\n"
                f"📋 DFMEA 比對防禦結果：\n"
                f"- 代碼：{rule['id']}\n"
                f"- 失效模式：{rule['failure_mode']}\n"
                f"- 風險指標 (RPN)：{rpn} (S:{rule['severity']} O:{rule['occurrence']} D:{rule['detection']})\n"
                f"- 潛在失效原因：{rule['root_cause']}\n"
                f"- 預防控制方案：{rule['prevention']}\n"
                f"- 建議自癒措施：{rule['corrective']}\n\n"
                f"🤖 守護機器人已啟動自動修復與進程重啟機制，我們一起加油！🌸"
            )
            send_telegram_push(alert_text)
            
            # Execute physical self-healing repair action
            execute_self_healing_action(srv["name"], rule["corrective"])

if __name__ == "__main__":
    run_telemetry_scan()
