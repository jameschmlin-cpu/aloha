import sqlite3
conn = sqlite3.connect(r'C:\Genesis\Core_Vault\Master_Connectivity.db')
try:
    conn.execute("INSERT INTO instruction_audit (uid, status) VALUES ('TEST_001', 'PENDING')")
    conn.commit()
    print('✅ 測試指令 TEST_001 已注入資料庫。')
except sqlite3.IntegrityError:
    print('⚠️ 指令已存在，請確認狀態。')
conn.close()

