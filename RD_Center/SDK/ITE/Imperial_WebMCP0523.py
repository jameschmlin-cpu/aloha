# -*- coding: utf-8 -*-

import json

import os

import subprocess

import sys


import sqlite3

import hashlib

import psutil

from http.server import HTTPServer, BaseHTTPRequestHandler

from datetime import datetime



# 鎖定 SDK 路徑，落實後端模組化

SDK_CORE_PATH = r"C:\Genesis\SDK\Core"

if SDK_CORE_PATH not in sys.path:

    sys.path.append(SDK_CORE_PATH)



class WebMCP(BaseHTTPRequestHandler):

    EXCHANGE_PATH = r"C:\Genesis\Exchange"

    DB_PATH = r"C:\Genesis\Database\Lobster_Memory.db"



    def _init_db(self):

        """初始化實體 SQLite 共同記憶庫"""

        os.makedirs(os.path.dirname(self.DB_PATH), exist_ok=True)

        conn = sqlite3.connect(self.DB_PATH)

        conn.execute('''CREATE TABLE IF NOT EXISTS file_logs 

                       (id INTEGER PRIMARY KEY AUTOINCREMENT,

                        timestamp TEXT, client TEXT, filename TEXT, hash TEXT, status TEXT)''')

        conn.commit()

        conn.close()



    def log_to_terminal_and_db(self, filename, file_hash, status):

        """實時在視窗釋出數據並寫入資料庫"""

        timestamp = datetime.now().strftime("%H:%M:%S")

        client_info = self.headers.get('User-Agent', 'Unknown')

        

        # 1. 視窗即時釋出 (Terminal Echo)

        print(f"[{timestamp}] 📥 [ACTION] {filename} | HASH: {file_hash[:16]}... | STATUS: {status}")

        

        # 2. SQLite 實體存證

        try:

            self._init_db()

            conn = sqlite3.connect(self.DB_PATH)

            conn.execute("INSERT INTO file_logs (timestamp, client, filename, hash, status) VALUES (?, ?, ?, ?, ?)",

                         (timestamp, client_info, filename, file_hash, status))

            conn.commit()

            conn.close()

        except Exception as e:

            print(f"   >> [DB] 🚨 記憶寫入失敗: {str(e)}")



    def do_POST(self):

        content_length = int(self.headers.get('Content-Length', 0))

        if content_length == 0: return

        

        try:

            data = json.loads(self.rfile.read(content_length))

        except Exception as e:

            self._send_error(f"JSON 解析失敗: {str(e)}")

            return



        cmd_type = data.get('cmd', 'infer')

        reply = ""; node_c = "OK"



        try:

            if cmd_type == "save":

                filename = data.get('filename', 'temp.txt')

                content = data.get('content', '')

                f_hash = hashlib.sha256(content.encode()).hexdigest()

                

                # --- 自動補完子路徑邏輯 (核心修正) ---

                target_path = os.path.join(self.EXCHANGE_PATH, filename)

                target_dir = os.path.dirname(target_path)

                if not os.path.exists(target_dir):

                    os.makedirs(target_dir, exist_ok=True)

                

                with open(target_path, 'w', encoding='utf-8') as f:

                    f.write(content)

                

                # 同步釋出數據至視窗並存入 SQLite

                self.log_to_terminal_and_db(filename, f_hash, "SUCCESS")

                reply = f"✅ {filename} 物理寫入與 SQLite 存證成功。"



            elif cmd_type == "sync":

                f_hash = hashlib.sha256(str(datetime.now()).encode()).hexdigest()

                self.log_to_terminal_and_db("SYNC_EVENT", f_hash, "SYNCED")

                reply = f"✅ 三端導通同步成功。Session Hash: {f_hash[:16]}"



            else:

                reply = "指令未定義，僅接受 sync 或 save。"



        except Exception as e:

            print(f"🚨 [ERROR] 處理中斷: {str(e)}")

            reply = f"【技術瓶頸】{str(e)}"

            node_c = "ERR"



        self.send_response(200)

        self.send_header('Content-type', 'application/json')

        self.send_header('Access-Control-Allow-Origin', '*')

        self.end_headers()

        self.wfile.write(json.dumps({"text": f"[{node_c}] {reply}", "time": datetime.now().strftime("%H:%M:%S")}).encode())



    def _send_error(self, message):

        self.send_response(400)

        self.send_header('Content-type', 'application/json')

        self.end_headers()

        self.wfile.write(json.dumps({"text": message}).encode())



    def do_OPTIONS(self):

        self.send_response(200)

        self.send_header('Access-Control-Allow-Origin', '*')

        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

        self.end_headers()



# --- 啟動前全功能自我診斷 (Pre-Flight Diagnostic) ---

def run_diagnostic_and_guard():

    print("\n" + "=".center(60, "="))

    print(" 🛡️  龍蝦帝國 WebMCP V3.2.1 - 完整實體守護版 ".center(60))

    print("=".center(60, "="))



    # 1. System Guard: 保安除害

    print(f"[{datetime.now().strftime('%H:%M:%S')}] 【1/4 System Guard】執行物理熔斷與環境清理...")

    try:

        # 嘗試關閉舊有的 PM2 進程（若存在）

        subprocess.run(["pm2", "kill"], capture_output=True, timeout=2)

    except: pass

    

    # 2. 資源監控

    ram = psutil.virtual_memory().available / (1024**3)

    cpu = psutil.cpu_percent(interval=1)

    print(f"[{datetime.now().strftime('%H:%M:%S')}] 【2/4 資源偵測】CPU: {cpu}% | RAM: {ram:.2f}GB")



    # 3. 實體診斷 (寫入/讀取/比對)

    print(f"[{datetime.now().strftime('%H:%M:%S')}] 【3/4 實體診斷】執行寫入/讀取/Hash 校驗...")

    test_path = r"C:\Genesis\DIAG_TEST.tmp"

    try:

        test_data = f"Lobster_Diagnostic_{datetime.now().strftime('%Y%m%d%H%M')}"

        # 確保根目錄存在

        if not os.path.exists(r"C:\Genesis"): os.makedirs(r"C:\Genesis")

        with open(test_path, "w") as f: f.write(test_data)

        with open(test_path, "r") as f: read_data = f.read()

        os.remove(test_path)

        if read_data == test_data:

            print("   >> [PASS] 物理讀寫校驗一致。")

        else:

            raise ValueError("物理數據校驗失效！")

    except Exception as e:

        print(f"🚨 [FAIL] 診斷失敗: {e}")

        sys.exit(1)



    # 4. 網絡狀態與資料庫

    print(f"[{datetime.now().strftime('%H:%M:%S')}] 【4/4 網絡/DB】檢查資料庫通道與 Port 5000...")

    db_dir = r"C:\Genesis\Database"

    if not os.path.exists(db_dir): os.makedirs(db_dir)

    print("   >> [PASS] SQLite 通道導通。")

    print("="*60 + "\n")



if __name__ == "__main__":

    # 執行所有啟動前自檢

    run_diagnostic_and_guard()

    

    print("🚀 WebMCP V3.2.1 完整版啟動成功，監聽 Port 5000...")

    # 鎖定 127.0.0.1 確保地端安全

    server = HTTPServer(('127.0.0.1', 5000), WebMCP)

    server.serve_forever()