# 檔案：C:\Genesis\Genesis_Core\DB_Initializer.py

import sqlite3

import os



def initialize_database():

    db_path = r"C:\Genesis\Genesis_Core\Data\Unified_Empire_Memory.db"

    

    # 確保目錄存在

    if not os.path.exists(os.path.dirname(db_path)):

        os.makedirs(os.path.dirname(db_path))

        

    conn = sqlite3.connect(db_path)

    cursor = conn.cursor()

    

    # 建立實體結構

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS State_Table (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            service_name TEXT,

            status TEXT,

            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP

        )

    """)

    

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS Log_Table (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

            data TEXT

        )

    """)

    

    # 初始化一筆測試數據，確認寫入能力

    cursor.execute("INSERT INTO State_Table (service_name, status) VALUES (?, ?)", ("System_Init", "Active"))

    

    conn.commit()

    conn.close()

    print("[SUCCESS] 資料庫結構已初始化，State_Table 已就緒。")



if __name__ == "__main__":

    initialize_database()