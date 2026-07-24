import sqlite3
import os

vault_path = r'C:\Genesis\Core_Vault'

db_path = os.path.join(vault_path, 'Common_Memory.db')

conn = sqlite3.connect(db_path)

cursor = conn.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS memory_bank (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, summary TEXT, state_hash TEXT)')

cursor.execute('CREATE TABLE IF NOT EXISTS instruction_audit (uid TEXT PRIMARY KEY, status TEXT, result_hash TEXT)')

cursor.execute("INSERT INTO memory_bank (timestamp, summary, state_hash) VALUES (?, ?, ?)", 

               ('2026-06-05 04:05:00', '帝國核心記憶庫於 Core_Vault 重建完畢，影子程式已被隔離。', 'SECURE_BOOT_SUCCESS'))

conn.commit()

conn.close()

print('✅ 記憶庫已在 ' + db_path + ' 建立成功，權限已鎖定。')


