# 檔案：C:\Genesis\Genesis_Core\Init_Registry.py

import sqlite3




def init_registry():

    db_path = r"C:\Genesis\Config\System_Paths.db"

    conn = sqlite3.connect(db_path)

    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS paths (key TEXT PRIMARY KEY, path TEXT)''')

    

    # 寫入權威路徑，不再隨意改動

    paths = {

        "GATE_DIR": r"C:\Genesis\Genesis_Core\Gate",

        "CONFIG_DIR": r"C:\Genesis\Config",

        "ARTISAN_DIR": r"C:\Genesis\Genesis_Core\Artisan"

    }

    

    for key, path in paths.items():

        cursor.execute("INSERT OR REPLACE INTO paths (key, path) VALUES (?, ?)", (key, path))

    

    conn.commit()

    conn.close()

    print(f"[System] 路徑已寫入資料庫: {db_path}")



init_registry()