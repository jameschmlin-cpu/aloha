# -*- coding: utf-8 -*-

# 檔案：C:\Genesis\Genesis_Core\Node_Guardian.py

import sys

import sqlite3


from connectivity_base import BaseConnectivityOP



class NodeGuardian(BaseConnectivityOP):

    def __init__(self):

        super().__init__()

        self.report("INIT", "Node 守護者已掛載，開始全節點通訊校驗...")



    def check_all_nodes(self):

        """需求1：執行 Node A-D 物理節點連線狀態檢查"""

        nodes = ["Node_A", "Node_B", "Node_C", "Node_D"]

        results = {}

        

        try:

            conn = sqlite3.connect(self.db_path)

            for node in nodes:

                row = conn.execute("SELECT status FROM State_Table WHERE service_name = ?", (node,)).fetchone()

                status = row[0] if row else "INACTIVE"

                results[node] = status

                self.report("NODE_CHECK", f"{node} 狀態: {status}")

            conn.close()

        except Exception as e:

            self.report("FATAL", f"節點檢測鏈斷裂: {str(e)}")

            sys.exit(1)

            

        return results



    def get_system_health(self):

        """判斷是否觸發環境震盪熔斷"""

        stats = self.check_all_nodes()

        if list(stats.values()).count("ACTIVE") < 2:

            self.report("ALERT", "節點活躍度過低，觸發環境震盪熔斷機制。")

            return False

        return True