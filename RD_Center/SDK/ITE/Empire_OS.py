import json
import os
import subprocess
import requests
import time

import psutil

from http.server import HTTPServer, BaseHTTPRequestHandler



# 核心路徑與算力參數

BASE_PATH = r"C:\Genesis"

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"



class EmpireCore(BaseHTTPRequestHandler):

    def _set_headers(self):

        self.send_response(200)

        self.send_header('Access-Control-Allow-Origin', '*')

        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')

        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

        self.send_header('Content-type', 'application/json')

        self.end_headers()



    def do_OPTIONS(self):

        self._set_headers()



    def _get_live_data(self, node_id):

        """實體穿透：獲取真實硬體數據，不毀損主管原有填充格式"""

        timestamp_hash = f"SHA256_LOCKED_{node_id}_{int(time.time())}"

        data = {

            "id": node_id,

            "hash": timestamp_hash,

            "vram": "N/A",

            "temp": "N/A",

            "load": f"{psutil.cpu_percent()}%",

            "status": "實體鎖定 (LOCKED)",

            "dfmea": "Low Risk (Grade 2)"

        }



        if node_id == "RTX3060":

            try:

                cmd = "nvidia-smi --query-gpu=memory.used,memory.total,temperature.gpu,utilization.gpu --format=csv,noheader,nounits"

                out = subprocess.check_output(cmd, shell=True).decode().strip().split(',')

                data["vram"] = f"{out[0].strip()}MB / {out[1].strip()}MB"

                data["temp"] = f"{out[2].strip()}°C"

                data["load"] = f"{out[3].strip()}%"

            except:

                data["status"] = "GPU 離線"

        return data



    def do_GET(self):

        if '/data' in self.path:

            node_id = self.path.split('=')[-1] if '=' in self.path else "MAIN"

            self._set_headers()

            self.wfile.write(json.dumps(self._get_live_data(node_id)).encode('utf-8'))



    def do_POST(self):

        content_length = int(self.headers['Content-Length'])

        post_data = json.loads(self.rfile.read(content_length))

        user_msg = post_data.get('msg', '')

        

        prompt = (f"【最高權限指令：嚴禁使用英文。你必須使用在地台灣繁體中文回覆。】\n"

                  f"你是龍蝦帝國治安官志玲(L4)。主管指令：{user_msg}\n"

                  f"任務：進行頂真分析，回報內容需符合台灣資深工程師的專業口吻。")



        try:

            res = requests.post(OLLAMA_URL, json={"model": "llama3", "prompt": prompt, "stream": False}, timeout=60)

            reply = res.json().get('response', "算力回傳異常")

        except:

            reply = "【技術瓶頸】SubC1 算力導通失敗。"



        self._set_headers()

        self.wfile.write(json.dumps({"text": reply}).encode('utf-8'))



if __name__ == "__main__":

    os.system("for /f \"tokens=5\" %a in ('netstat -aon ^| findstr :5000') do taskkill /f /pid %a >nul 2>&1")

    print(r"🚀 [龍蝦部隊] 實體數據穿透版 OS 已定錨 C:\Genesis")

    server = HTTPServer(('127.0.0.1', 5000), EmpireCore)

    server.serve_forever()