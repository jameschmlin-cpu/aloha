# -*- coding: utf-8 -*-

# 檔案：C:\Genesis\Genesis_Core\Schema_Inspector.py

# 狀態：實體結構偵測工具 - 嚴禁假設，由實體回傳結果



import sqlite3

import sys



def inspect_db(db_path):

    if not os.path.exists(db_path):

        sys.stdout.write(f"[錯誤] 找不到資料庫檔案: {db_path}\n")

        return

    

    conn = sqlite3.connect(db_path)

    cursor = conn.cursor()

    

    # 獲取所有表格

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

    tables = cursor.fetchall()

    

    sys.stdout.write(f"--- 偵測報告: {db_path} ---\n")

    for table in tables:

        table_name = table[0]

        sys.stdout.write(f"Table: {table_name}\n")

        # 獲取欄位資訊

        cursor.execute(f"PRAGMA table_info({table_name});")

        columns = cursor.fetchall()

        for col in columns:

            sys.stdout.write(f"  - Column: {col[1]} (Type: {col[2]})\n")

    

    conn.close()



if __name__ == "__main__":

    import os

    inspect_db(r"C:\Genesis\Genesis_Core\Data\System_Core.db")

    inspect_db(r"C:\Genesis\Genesis_Core\Data\Unified_Empire_Memory.db")