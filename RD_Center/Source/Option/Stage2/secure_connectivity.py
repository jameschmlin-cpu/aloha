# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\SDK\Base\secure_connectivity.py
# 狀態：第二階段最終實作 - 單一入口佇列機制 (Queue) + 診斷初始化

import sqlite3
import hashlib
import queue
import threading
import sys
from SDK.Base.connectivity_base import BaseConnectivityOP

class SystemStateError(Exception): pass

class SecureConnectivityOP(BaseConnectivityOP):
    def __init__(self):
        self._init_stage = "SECURE_INIT"
        super().__init__()
        
        # 實作：單一入口佇列 (Queue) - 解決 Lock 問題
        self.write_queue = queue.Queue()
        self._db_lock = threading.Lock()
        self._ready = False
        
        # 啟動背景處理者 (Worker)
        self._start_worker()
        
        self._ready = True
        self._init_stage = "SECURE_READY"
        sys.stdout.write(f"[診斷] {self._init_stage}: 佇列系統已啟動\n")

    def _start_worker(self):
        """背景單一執行緒，專門負責與 DB 對話"""
        def worker():
            while True:
                table, data_dict = self.write_queue.get()
                self._execute_db_write(table, data_dict)
                self.write_queue.task_done()
        
        t = threading.Thread(target=worker, daemon=True)
        t.start()

    def _execute_db_write(self, table, data_dict):
        """實體寫入邏輯：這是資料庫的唯一入口"""
        with self._db_lock:
            try:
                conn = sqlite3.connect(r"C:\Genesis\Genesis_Core\Data\Unified_Empire_Memory.db")
                data_dict['audit_hash'] = hashlib.sha256(str(data_dict).encode('utf-8')).hexdigest()
                columns = ', '.join(data_dict.keys())
                placeholders = ', '.join(['?'] * len(data_dict))
                conn.execute(f"INSERT INTO {table} ({columns}) VALUES ({placeholders})", tuple(data_dict.values()))
                conn.commit()
                conn.close()
            except Exception as e:
                sys.stderr.write(f"[錯誤] 佇列寫入失敗: {e}\n")

    def secure_write(self, table, data_dict):
        """業務模組呼叫此函數進行排隊登記"""
        if not self._ready:
            raise SystemStateError(f"保護觸發：層級 {self._init_stage} 尚未就緒，拒絕存取。")
        self.write_queue.put((table, data_dict))
        return True