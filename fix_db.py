import sqlite3

db_path = r"C:\Genesis\Database\Path_Registry.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # 強制新增欄位，忽略錯誤 (若欄位已存在)
    cursor.execute("ALTER TABLE path_map ADD COLUMN backup_path TEXT;")
    conn.commit()
    print("[SUCCESS] backup_path 欄位修正完成。")
except sqlite3.OperationalError:
    print("[INFO] backup_path 欄位已存在。")
finally:
    conn.close()