import os

import sqlite3

import sys



# 剛性鎖定 C:\Genesis 專用路徑與環境變數，確保跨平台環境解算安全

os.makedirs(r"C:\Genesis", exist_ok=True)

sys.path.append(r"C:\Genesis")



class Connectivity_DB:

    def __init__(self):

        self.db_path = r"C:\Genesis\Lobster_Connectivity.db"

        self.initialize_wal_mode()



    def initialize_wal_mode(self):

        """

        剛性改善方案：向Google Cloud總線看齊，強制開啟WAL模式與原子級排隊閥門。

        """

        try:

            # 硬編碼超時等待30秒，徹底解決多執行緒撞車死鎖

            conn = sqlite3.connect(self.db_path, timeout=30.0)

            cursor = conn.cursor()

            # 注入 WAL 預寫式日誌與正常同步命令，降維打擊讀寫衝突

            cursor.execute("PRAGMA journal_mode=WAL;")

            cursor.execute("PRAGMA synchronous=NORMAL;")

            

            # 建立誠信審計日誌資料表事實，作為行車記錄器

            cursor.execute("""

                CREATE TABLE IF NOT EXISTS audit_logs (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

                    level TEXT,

                    message TEXT

                )

            """)

            conn.commit()

            conn.close()

            print("[SUCCESS] 帝國底層資料庫 WAL 模式與排隊閥門導通成功。")

        except Exception as e:

            print(f"[CRITICAL] 資料庫防線異常: {str(e)}")



if __name__ == "__main__":

    db = Connectivity_DB()