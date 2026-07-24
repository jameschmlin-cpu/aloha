# -*- coding: utf-8 -*-
# Compiled Brick from: 1.py
# Category: Core

class 1Brick:
    def run(self, ctx=None):
        try:
            import sqlite3
            db_path = r"C:\Genesis\Database\Genesis_DFMEA.db"
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            # 查詢所有被歸類為 Stage 屬性的模組清單
            cursor.execute("SELECT id, problem_point FROM dfmea_matrix WHERE problem_point LIKE '%Stage%'")
            for row in cursor.fetchall():
                print(f"指紋ID: {row[0]} | 定義歸位: {row[1]}")
            conn.close()
        except Exception as e:
            print(f"[1Brick] 運行失敗: {e}")
            return False
        return True
