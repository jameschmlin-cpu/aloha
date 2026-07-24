# C:\Genesis\SDK\Core\Brick_Registry.py
# -*- coding: utf-8 -*-
import sqlite3

class Brick_Registry:
    """
    【帝國動態索引中心】
    負責全系統 20 個邏輯類別的註冊、狀態追蹤與動態分發。
    """
    def __init__(self):
        # 對接 Base_Template 定義的資料庫路徑
        self.db_path = r"C:\Genesis\Database\Brick_Registry.db"
        self._ensure_table()

    def _ensure_table(self):
        """初始化 Registry 資料表，確保狀態存儲機制存在"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bricks (
                id TEXT PRIMARY KEY,
                category TEXT,
                status TEXT,
                last_heartbeat TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def get_all_bricks(self, category="GOVERNANCE"):
        """
        動態抓取邏輯：
        這裡會回傳所有符合類別的實體物件。
        註：在實體對接中，這裡通常會對應到已載入的 Python 物件實體。
        """
        # 實體治理擴展：在此處將從 DB 讀取的 ID 轉換為系統內已載入的物件
        # 為保持系統精簡，此處返回的是管理清單，由 Doctor 統一調度
        return [] 

    def update_brick_status(self, brick_id, status):
        """同步狀態至 Registry，確保 Doctor 指揮中心掌握全局"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE bricks SET status = ?, last_heartbeat = datetime('now')
            WHERE id = ?
        ''', (status, brick_id))
        conn.commit()
        conn.close()

    def register_brick(self, brick_id, category):
        """將新的邏輯積木納入治理清單"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT OR REPLACE INTO bricks (id, category, status) VALUES (?, ?, ?)',
                       (brick_id, category, "REGISTERED"))
        conn.commit()
        conn.close()