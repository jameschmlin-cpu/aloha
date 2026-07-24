import sqlite3
conn = sqlite3.connect(r'C:\Genesis\Database\Genesis_Tasks.db')
count = conn.execute("SELECT count(*) FROM tasks WHERE status = 'COMPLETED'").fetchone()[0]
print(f"已完成任務總數: {count}")
conn.close()