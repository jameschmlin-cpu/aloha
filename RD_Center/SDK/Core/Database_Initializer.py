# -*- coding: utf-8 -*-

# 檔案：C:\Genesis\Genesis_Core\Database_Initializer.py

import sqlite3

import os



def init_db():

    db_path = r"C:\Genesis\Genesis_Core\Data\path_master.db"

    

    # 確保資料庫路徑存在

    if not os.path.exists(r"C:\Genesis\Genesis_Core\Data"):

        os.makedirs(r"C:\Genesis\Genesis_Core")

        

    conn = sqlite3.connect(db_path)

    cursor = conn.cursor()

    

    # 建立路徑註冊表

    cursor.execute('''CREATE TABLE IF NOT EXISTS PathRegistry 

                      (key TEXT PRIMARY KEY, physical_path TEXT NOT NULL)''')

    

    # 寫入唯一合法路徑，杜絕任何外部嘗試

    paths = [

        ('BASE', r'C:\Genesis\Genesis_Core'),

        ('REGISTRY', r'C:\Genesis\Genesis_Core\Registry.json'),

        ('LOGS', r'C:\Genesis\Genesis_Core\logs'),

        ('VAULT', r'C:\Genesis\Genesis_Core\Vault')

    ]

    

    cursor.executemany('INSERT OR REPLACE INTO PathRegistry VALUES (?,?)', paths)

    conn.commit()

    conn.close()

    print(f"[*] 成功建立路徑資料庫於: {db_path}")



if __name__ == "__main__":

    init_db()