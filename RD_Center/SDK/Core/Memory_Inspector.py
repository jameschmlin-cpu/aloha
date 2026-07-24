# -*- coding: utf-8 -*-

# 檔案：C:\Genesis\Genesis_Core\Memory_Inspector.py

# 狀態：實體結構審查工具 - 針對 Unified_Empire_Memory.db



import sqlite3

import os

import sys



def inspect_memory_db():

    db_path = r"C:\Genesis\Genesis_Core\Data\Unified_Empire_Memory.db"

    if not os.path.exists(db_path):

        sys.stdout.write("[錯誤] 記憶資料庫路徑缺失\n")

        return



    conn = sqlite3.connect(db_path)

    cursor = conn.cursor()

    

    # 執行結構審查

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

    tables = cursor.fetchall()

    

    sys.stdout.write(f"--- [實體審查] 記憶庫結構: {db_path} ---\n")

    for table in tables:

        table_name = table[0]

        sys.stdout.write(f"Table: {table_name}\n")

        cursor.execute(f"PRAGMA table_info({table_name});")

        for col in cursor.fetchall():

            sys.stdout.write(f"  - Column: {col[1]} (Type: {col[2]})\n")

    

    # 試探性讀取 State_Table (確認唯讀對接是否正常)

    try:

        cursor.execute("SELECT * FROM State_Table LIMIT 1;")

        row = cursor.fetchone()

        sys.stdout.write(f"\n--- [試探性讀取] State_Table 範例: {row} ---\n")

    except Exception as e:

        sys.stdout.write(f"\n[狀態] State_Table 讀取失敗: {e}\n")

    

    conn.close()



if __name__ == "__main__":

    inspect_memory_db()