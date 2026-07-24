# 檔案：C:\Genesis\Genesis_Core\Service_Bridge.py

import sys

import sqlite3

import threading




def get_path(key):

    """從資料庫獲取權威路徑"""

    try:

        conn = sqlite3.connect(r"C:\Genesis\Config\System_Paths.db")

        cursor = conn.cursor()

        cursor.execute("SELECT path FROM paths WHERE key=?", (key,))

        result = cursor.fetchone()

        conn.close()

        return result[0] if result else None

    except Exception:

        return None



# 動態加入路徑

GATE_DIR = get_path("GATE_DIR")

if GATE_DIR and GATE_DIR not in sys.path:

    sys.path.append(GATE_DIR)



try:

    from WebMCP_Genesis import WebMCP_Genesis

    print("[Bridge] WebMCP 模組載入成功！")

except ImportError:

    print("[Bridge] 錯誤：載入失敗，請檢查 Gate 路徑設定。")

    sys.exit(1)



class MCP_Service_Bridge:

    def __init__(self):

        self.service_thread = None



    def start_service(self):

        def run():

            try:

                # 實例化 WebMCP，確保封裝於背景

                mcp = WebMCP_Genesis(None, None, None)

                print("[Bridge] MCP Service 封裝啟動成功 (非阻塞)")

            except Exception as e:

                print(f"[Bridge] 服務啟動異常: {e}")

            

        self.service_thread = threading.Thread(target=run, daemon=True)

        self.service_thread.start()



if __name__ == "__main__":

    bridge = MCP_Service_Bridge()

    bridge.start_service()

    print("[Main] 閉迴路封裝服務已啟動，主程式未阻塞。")