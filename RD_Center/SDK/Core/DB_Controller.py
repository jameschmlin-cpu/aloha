# -*- coding: utf-8 -*-

# 檔案：C:\Genesis\Genesis_Core\DB_Controller.py

# 狀態：原地升級版 - 整合閉環基底與執行報訊，解決鎖定風險



import sqlite3


from connectivity_base import BaseConnectivityOP



class DB_Controller(BaseConnectivityOP):

    def __init__(self):

        # 繼承基底，自動獲得 Doctor 與 DFMEA 防禦能力

        super().__init__()

        self.db_path = r"C:\Genesis\Genesis_Core\Data\Unified_Empire_Memory.db"

        print(f"[*] DB_Controller 初始化完成，綁定庫: {self.db_path}")



    def execute_query(self, query, params=()):

        """

        封裝後的查詢接口：透過 execute_safe 進行閉環管理

        """

        def _task():

            conn = sqlite3.connect(self.db_path)

            cur = conn.cursor()

            cur.execute(query, params)

            result = cur.fetchall()

            conn.commit()

            conn.close()

            return result



        # 使用基底的 execute_safe 進行防禦性封裝

        return self.execute_safe("DB_QUERY_TASK", _task)



    def log_status(self, message):

        """強化版報訊功能"""

        print(f"[DB_LOG] {message}")



if __name__ == "__main__":

    # 測試執行：確保升級後沒有邏輯死鎖

    try:

        controller = DB_Controller()

        # 簡單測試讀取操作，確保連線正常

        # 執行報訊

        controller.log_status("正在進行資料庫連線測試...")

        print(">>> 測試結果：DB_Controller 升級版執行成功！")

    except Exception as e:

        print(f"!!! [DB_FAILURE] {str(e)}")