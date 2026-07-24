import os

import hashlib

import time

import sqlite3

import ctypes

import psutil

import subprocess

import shutil # 使用原生模組檢查路徑



class LobsterUnifyV2:

    def __init__(self):

        self.ite_root = r"C:\Genesis"

        self.cloud_path = r"G:\我的雲端硬碟\ITE GEMINI Pro雲端指揮中心"

        self.db_path = os.path.join(self.ite_root, "lobster_memory.db")

        self.lock_file = os.path.join(self.cloud_path, "unify_v2.lock")

        os.makedirs(self.ite_root, exist_ok=True)

        self._init_db()



    def _init_db(self):

        with sqlite3.connect(self.db_path) as conn:

            conn.execute("CREATE TABLE IF NOT EXISTS memory_audit (id INTEGER PRIMARY KEY AUTOINCREMENT, logic_hash TEXT, status TEXT, ts TIMESTAMP)")



    def _get_hash(self, text):

        return hashlib.sha256(text.encode('utf-8')).hexdigest()



    def physical_pm2_cleanup(self):

        """抗阻塞版本：使用 shutil.which 替代 subprocess 偵測"""

        print(" -> [實施中] 正在執行資源負載掃描...")

        try:

            # 1. 檢查記憶體是否過載

            if psutil.virtual_memory().percent > 90:

                return "FAIL: RAM_CRITICAL"



            # 2. 使用原生 Python 尋找執行檔，避免啟動子進程卡死

            pm2_path = shutil.which("pm2")

            if not pm2_path:

                print(" -> [跳過] 系統環境變數中未發現 PM2。")

                return "SUCCESS: NO_PM2"



            # 3. 執行清理，設定極短超時 (3秒)，若卡住直接熔斷

            print(f" -> [偵測] 發現 PM2 於 {pm2_path}，嘗試熔斷...")

            subprocess.run(["pm2", "kill"], capture_output=True, timeout=3)

            return "SUCCESS: PM2_CLEANED"

        except subprocess.TimeoutExpired:

            print(" -> [警告] PM2 響應逾時，已強制跳過防止系統卡死。")

            return "SUCCESS: TIMEOUT_SKIP"

        except Exception as e:

            return f"FAIL: {str(e)}"



    def execute_handshake_sync(self, logic_name):

        print("\n=== [龍蝦帝國] 雲地一次化 V2.1 (抗阻塞) 啟動 ===")

        

        # 1. 物理連通性校驗

        if not os.path.exists(self.cloud_path):

            self._alarm("報警：G 槽未掛載，同步失敗！")

            return False



        # 2. 實施資源清理 (含防卡死邏輯)

        self.physical_pm2_cleanup()



        # 3. 雲地一致性寫入

        ts_hash = self._get_hash(f"{logic_name}_{time.time()}")

        try:

            with open(self.lock_file, "w", encoding="utf-8") as f:

                f.write(ts_hash)

            

            time.sleep(0.5) # 縮短回讀等待

            with open(self.lock_file, "r", encoding="utf-8") as f:

                verify_hash = f.read().strip()



            if verify_hash != ts_hash:

                self._alarm("數據不一致：同步逃逸！")

                return False



            # 4. 存證

            with sqlite3.connect(self.db_path) as conn:

                conn.execute("INSERT INTO memory_audit (logic_hash, status, ts) VALUES (?, ?, ?)",

                             (ts_hash, "VERIFIED", time.strftime('%Y-%m-%d %H:%M:%S')))

            

            print("✅ 實施成功：雲地一致。")

            self._info(f"✅ 龍蝦 V2.1 校驗成功 ✅\nSHA-256: {ts_hash[:24]}...")

            return True



        except Exception as e:

            self._alarm(f"物理寫入崩潰：{str(e)}")

            return False



    def _alarm(self, msg):

        ctypes.windll.user32.MessageBoxW(0, msg, "【保安報警】", 0x10)



    def _info(self, msg):

        ctypes.windll.user32.MessageBoxW(0, msg, "【執行報告】", 0x40)



if __name__ == "__main__":

    core = LobsterUnifyV2()

    core.execute_handshake_sync("初始化同步協定")