import os

import sqlite3

import hashlib



# 鎖定路徑

BASE_DIR = r"C:\Genesis"

DB_DIR = r"C:\Genesis\Database"

DB_PATH = os.path.join(DB_DIR, "System_Core.db")



def init_system_core():

    # 確保 Database 目錄存在

    if not os.path.exists(DB_DIR):

        os.makedirs(DB_DIR)

    

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    

    # 建立系統檔案註冊表

    cursor.execute('''CREATE TABLE IF NOT EXISTS file_registry 

                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 

                       name TEXT, path TEXT, ext TEXT, function_desc TEXT)''')

    conn.commit()

    

    # 掃描並匯入

    count = 0

    for root, dirs, files in os.walk(BASE_DIR):

        # 避開 Database 目錄以免發生讀寫衝突

        if "Database" in root:

            continue

            

        for file in files:

            if file.endswith(('.py', '.bat', '.sh', '.json')):

                full_path = os.path.join(root, file)

                ext = os.path.splitext(file)[1]

                

                # 嘗試讀取功能摘要

                try:

                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:

                        func = f.readline().strip()[:50]

                except:

                    func = "不可讀取"

                

                cursor.execute("INSERT INTO file_registry (name, path, ext, function_desc) VALUES (?, ?, ?, ?)",

                               (file, full_path, ext, func))

                count += 1

    

    conn.commit()

    conn.close()

    return count



if __name__ == "__main__":

    imported_count = init_system_core()

    print(f"掃描作業完成，共匯入 {imported_count} 筆程式節點至 {DB_PATH}")

    

    # 產出 Hash

    with open(__file__, 'rb') as f:

        print(f"程式 Hash: {hashlib.sha256(f.read()).hexdigest()}")