# C:\Genesis\Engine\Verify_Database.py
import sqlite3

db_path = r"C:\Genesis\Database\Path_Database.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 寫入您剛才指定的路徑清單
path_entries = [
    ('CORE_ENGINE', r'C:\Genesis\Engine\Genesis_Native_Core.py'),
    ('COMMAND_CENTER', r'C:\Genesis\Management_Hub\Empire_Command_Center.py'),
    ('PREFERENCE', r'C:\Genesis\Management_Hub\Preference.md'),
    ('GEMINI_CC', r'C:\Genesis\Management_Hub\Gemini_Command_Center.py')
]

cursor.executemany('INSERT OR REPLACE INTO path_map VALUES (?, ?)', path_entries)
conn.commit()

# 撈出驗證
print(f"--- [資料庫內容驗證: {db_path}] ---")
cursor.execute("SELECT * FROM path_map")
for row in cursor.fetchall():
    print(f"KEY: {row[0]} | PATH: {row[1]}")

conn.close()