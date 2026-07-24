# -*- coding: utf-8 -*-

import os


from http.server import HTTPServer, BaseHTTPRequestHandler

from socketserver import ThreadingMixIn




# 剛性路徑配置 (確保目錄存在)

BASE_PATH = r"C:\Genesis"

os.makedirs(os.path.join(BASE_PATH, "SDK", "Core"), exist_ok=True)

os.makedirs(os.path.join(BASE_PATH, "Office"), exist_ok=True)



class DirectImperialServer(ThreadingMixIn, HTTPServer):

    allow_reuse_address = True



class DirectOrchestrator(BaseHTTPRequestHandler):

    def do_POST(self):

        content_length = int(self.headers.get('Content-Length', 0))

        body = self.rfile.read(content_length).decode('utf-8')

        

        # 實體檔案強制寫入邏輯

        try:

            if "CREATE_SDK" in body:

                path = r"C:\Genesis\SDK\Core\SDK_Interface.ps1"

                with open(path, 'w') as f:

                    f.write("## SDK Core Active ##")

                msg = f"SDK 寫入成功: {path}"

            elif "CREATE_SOP" in body:

                path = r"C:\Genesis\Office\Salary_Calc_Logic.ps1"

                with open(path, 'w') as f:

                    f.write("## Salary SOP Active ##")

                msg = f"SOP 寫入成功: {path}"

            else:

                msg = "未知指令"

            

            self.send_response(200)

            self.end_headers()

            self.wfile.write(msg.encode())

        except Exception as e:

            self.send_response(500)

            self.end_headers()

            self.wfile.write(str(e).encode())



if __name__ == "__main__":

    print("🚀 帝國網閘啟動中... Port 5000")

    server = DirectImperialServer(('127.0.0.1', 5000), DirectOrchestrator)

    server.serve_forever()