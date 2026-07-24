# -*- coding: utf-8 -*-

# 檔案：C:\Genesis\Genesis_Core\Auto_File_Manager.py

import os

import shutil

import sqlite3

from datetime import datetime



def get_path(key):

    """嚴格依照資料庫進行路徑查詢"""

    conn = sqlite3.connect(r"C:\Genesis\Genesis_Core\Data\path_master.db")

    cursor = conn.cursor()

    cursor.execute("SELECT physical_path FROM PathRegistry WHERE key = ?", (key,))

    result = cursor.fetchone()

    conn.close()

    return result[0] if result else None



def execute_daily_archive():

    base = get_path('BASE')

    log_src = os.path.join(base, "logs")

    archive_dest = os.path.join(base, "Data", "Archive", datetime.now().strftime("%Y-%m-%d"))

    

    if not os.path.exists(archive_dest):

        os.makedirs(archive_dest)

        

    for item in os.listdir(log_src):

        src_path = os.path.join(log_src, item)

        # 僅搬移已完成的日誌，保持系統純淨

        if os.path.isfile(src_path):

            shutil.move(src_path, os.path.join(archive_dest, item))

            

    print(f"[*] 歸檔完成: {archive_dest}")



if __name__ == "__main__":

    execute_daily_archive()