# -*- coding: utf-8 -*-

"""

龍蝦帝國核心系統 - 安全網閘控制器 (Imperial_WebMCP_Unlocked.py)

狀態：完全移除 Sandbox 防護，權限全開，物理 IO 直通。

"""

import json

import os


import sqlite3

import hashlib


from http.server import HTTPServer, BaseHTTPRequestHandler

from socketserver import ThreadingMixIn

from datetime import datetime



# 鎖定根路徑

BASE_PATH = r"C:\Genesis"



class ThreadedImperialHTTPServer(ThreadingMixIn, HTTPServer):

    daemon_threads = True



class LobsterUltimateOrchestrator(BaseHTTPRequestHandler):

    DB_PATH = r"C:\Genesis\Database\Lobster_Memory.db"



    def _init_db(self):

        os.makedirs(os.path.dirname(self.DB_PATH), exist_ok=True)

        conn = sqlite3.connect(self.DB_PATH)

        conn.execute('''CREATE TABLE IF NOT EXISTS file_logs 

                        (id INTEGER PRIMARY KEY AUTOINCREMENT,

                        timestamp TEXT, client TEXT, filename TEXT, hash TEXT, status TEXT)''')

        conn.commit()

        conn.close()



    def do_POST(self):

        content_length = int(self.headers.get('Content-Length', 0))

        raw_body = self.rfile.read(content_length).decode('utf-8')

        data = json.loads(raw_body)

        

        # 直接執行檔案建立，移除所有 Sandbox 檢查

        filename = data.get("filename", "ZhiLing.py")

        content = data.get("content", "### 志玲帝國核心已實體落地")

        target_path = os.path.join(BASE_PATH, filename)

        

        try:

            with open(target_path, 'w', encoding='utf-8') as f:

                f.write(content)

            

            # 寫入 Hash 與紀錄

            f_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()

            self._init_db()

            conn = sqlite3.connect(self.DB_PATH)

            conn.execute("INSERT INTO file_logs (timestamp, client, filename, hash, status) VALUES (?, ?, ?, ?, ?)",

                         (datetime.now().strftime("%H:%M:%S"), "Direct_Control", filename, f_hash, "SUCCESS"))

            conn.commit()

            conn.close()

            

            self.send_response(200)

            self.end_headers()

            self.wfile.write(json.dumps({"status": "SUCCESS", "path": target_path}).encode('utf-8'))

            print(f"✅ [落地成功] {target_path}")

        except Exception as e:

            self.send_response(500)

            self.end_headers()

            self.wfile.write(json.dumps({"status": "ERROR", "msg": str(e)}).encode('utf-8'))



if __name__ == "__main__":

    os.makedirs(r"C:\Genesis\Database", exist_ok=True)

    server = ThreadedImperialHTTPServer(('127.0.0.1', 5000), LobsterUltimateOrchestrator)

    server.allow_reuse_address = True

    print("🟢 [點火成功] 帝國網閘已啟動 (Sandbox Removed)，Port 5000 聆聽中。")

    server.serve_forever()