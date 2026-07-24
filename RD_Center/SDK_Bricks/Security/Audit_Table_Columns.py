# -*- coding: utf-8 -*-
# Compiled Brick from: Audit_Table_Columns.py
# Category: Security

class AuditTableColumnsBrick:
    def run(self, ctx=None):
        try:
            # Category: Security
            # -*- coding: utf-8 -*-
            # 檔案名稱：C:\Genesis\Audit_Table_Columns.py
            # 核心功能：精準列出 dfmea_matrix 表格的所有欄位，徹底排除欄位名稱錯誤

            import sqlite3
            import os

            def audit_columns():
                db_path = r"C:\Genesis\Database\Genesis_DFMEA.db"
                table_name = "dfmea_matrix"

                if not os.path.exists(db_path):
                    print(f"[嚴重錯誤] 資料庫檔案不存在: {db_path}")
                    return

                try:
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()

                    # 執行 PRAGMA table_info 這是查詢表格結構的標準工業級做法
                    cursor.execute(f"PRAGMA table_info({table_name});")
                    columns = cursor.fetchall()

                    print(f"=== {table_name} 表格欄位清單 ===")
                    if not columns:
                        print("  (未找到該表格，或表格為空)")
                    else:
                        for col in columns:
                            # col[1] 是欄位名稱, col[2] 是資料型態
                            print(f"  - 欄位名稱: {col[1]} | 型態: {col[2]}")

                    conn.close()
                except Exception as e:
                    print(f"[診斷失敗] 查詢錯誤: {e}")

            if __name__ == "__main__":
                audit_columns()
        except Exception as e:
            print(f"[AuditTableColumnsBrick] 運行失敗: {e}")
            return False
        return True
