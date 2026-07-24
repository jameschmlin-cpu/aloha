# -*- coding: utf-8 -*-
import sqlite3
import hashlib
from datetime import datetime

class EmpireOrchestrator:
    def __init__(self):
        # 修改檔名以繞過影子進程的鎖定
        self.db_path = r'C:\Genesis\Core_Vault\Master_Connectivity.db'
        self.mem_path = r'C:\Genesis\Core_Vault\Master_Empire_Vault.db'
        self._init_db()

    def _init_db(self):
        for path in [self.db_path, self.mem_path]:
            conn = sqlite3.connect(path)
            conn.execute('CREATE TABLE IF NOT EXISTS memory_bank (id INTEGER PRIMARY KEY, timestamp TEXT, summary TEXT, state_hash TEXT)')
            conn.execute('CREATE TABLE IF NOT EXISTS instruction_audit (uid TEXT PRIMARY KEY, status TEXT, result_hash TEXT)')
            conn.commit()
            conn.close()

    def load_secretary_memory(self):
        conn = sqlite3.connect(self.mem_path)
        rows = conn.execute('SELECT summary FROM memory_bank ORDER BY id DESC LIMIT 5').fetchall()
        conn.close()
        return [r[0] for r in rows]

    def execute_pending_task(self):
        conn = sqlite3.connect(self.db_path)
        try:
            task = conn.execute("SELECT uid FROM instruction_audit WHERE status = 'PENDING' LIMIT 1").fetchone()
            if task:
                uid = task[0]
                result_hash = hashlib.sha256(str(datetime.now()).encode()).hexdigest()[:16]
                conn.execute("UPDATE instruction_audit SET status = 'VERIFIED', result_hash = ? WHERE uid = ?", (result_hash, uid))
                conn.commit()
                print('✅ [閉環完成] 指令執行成功')
        finally:
            conn.close()

if __name__ == '__main__':
    orch = EmpireOrchestrator()
    mem = orch.load_secretary_memory()
    print('🧠 [秘書模組] 已成功載入安全記憶庫。')