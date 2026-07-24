# 檔案：C:\Genesis\Genesis_Core\Align_And_Merge.py

import sqlite3

import os



def align_and_merge():

    old_db = r"C:\Genesis\Genesis_Core\Data\System_Core.db"

    new_db = r"C:\Genesis\Config\System_Paths.db"

    

    # 物理檢查檔案是否存在，不存在則立刻跳出

    if not os.path.exists(old_db):

        print(f"File not found: {old_db}")

        return

    if not os.path.exists(new_db):

        print(f"File not found: {new_db}")

        return



    # 連接資料庫

    conn_new = sqlite3.connect(new_db)

    conn_old = sqlite3.connect(old_db)

    

    try:

        # 僅執行單純的資料轉移，不對資料庫結構做任何變更

        # 確保目標只有 'paths' 表，這是我們雙方確認過的結構

        data = conn_old.execute("SELECT key, path FROM paths").fetchall()

        for key, path in data:

            conn_new.execute("INSERT OR REPLACE INTO paths (key, path) VALUES (?, ?)", (key, path))

        conn_new.commit()

    except Exception as e:

        print(f"Error: {e}")

    finally:

        conn_new.close()

        conn_old.close()



if __name__ == "__main__":

    align_and_merge()