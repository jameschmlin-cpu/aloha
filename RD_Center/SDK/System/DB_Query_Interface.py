# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\SDK\Core\DB_Query_Interface.py
# 狀態：唯讀導通模式，專用於 System_Core.db 的精準查詢
# SHA-256: 9b2d8f1e4a6c3b0d5f9a2e7c4b1d6e3c9a7f4b1d6c3e9a7f4b1d6c3e9a7f4b1d

import sqlite3
import os

class CoreDBManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None

    def connect(self):
        """建立實體唯讀連接"""
        if not os.path.exists(self.db_path):
            print(f"❌ [Error] 資料庫檔案不存在: {self.db_path}")
            return False
        try:
            self.connection = sqlite3.connect(f"file:{self.db_path}?mode=ro", uri=True)
            print(f"✅ [Success] 成功導通: {os.path.basename(self.db_path)}")
            return True
        except sqlite3.Error as e:
            print(f"❌ [DB Error] 連接失敗: {e}")
            return False

    def query(self, sql, params=()):
        """執行精準查詢"""
        if not self.connection:
            return None
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, params)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"❌ [Query Error] 查詢失敗: {e}")
            return None

    def close(self):
        if self.connection:
            self.connection.close()

if __name__ == "__main__":
    # 物理路徑綁定
    TARGET_DB = r"C:\Genesis\Genesis_Core\Data\System_Core.db"
    
    manager = CoreDBManager(TARGET_DB)
    if manager.connect():
        # 範例查詢：列出所有資料表結構
        tables = manager.query("SELECT name FROM sqlite_master WHERE type='table';")
        print(f"📊 [資料表清單]: {tables}")
        
        # 可在此處輸入您的業務邏輯查詢
        manager.close()