# -*- coding: utf-8 -*-

# 檔案：C:\Genesis\Genesis_Core\DFMEA_Engine.py

# 狀態：整合 CWE 智庫與閉環修復機制




import os

import sqlite3

from connectivity_base import BaseConnectivityOP

from DFMEA_CWE_Bridge import DFMEABridge 



class DFMEA_Engine(BaseConnectivityOP):

    def __init__(self):

        super().__init__()

        # 物理路徑對接 (改為環境感知)
        def find_genesis_base():
            if "GENESIS_HOME" in os.environ:
                return os.environ["GENESIS_HOME"]
            current = os.path.abspath(__file__)
            while True:
                parent, name = os.path.split(current)
                if name.lower() == "genesis" or os.path.exists(os.path.join(current, "Genesis_Map.json")):
                    return current
                if not name:
                    break
                current = parent
            return r"C:\Genesis"

        genesis_base = find_genesis_base()
        self.db_path = os.path.join(genesis_base, "Database", "Genesis_DFMEA.db")

        self.bridge = DFMEABridge()

        

        if not os.path.exists(self.db_path):

            raise RuntimeError("!!! [SECURITY ALERT] 資料庫物理路徑遺失")



    def dispatch_instinct_command(self, command, params=None):

        """[保留功能] 帝國層級本能指令路由"""

        print(f"[Node-D] 接收本能指令: {command}")

        return True



    def monitor_resources(self):
        """[動態資源管理] 監控 CPU 與記憶體載荷，防範雪崩過載"""
        try:
            import sys
            import psutil
            cpu_usage = psutil.cpu_percent(interval=None)
            mem_usage = psutil.virtual_memory().percent
            
            # 若負載超標 (90% 限流閾值)
            if cpu_usage > 90.0 or mem_usage > 90.0:
                sys.stderr.write(f"⚠️ [警告] 資源使用超載！CPU: {cpu_usage}%, RAM: {mem_usage}%。啟動限流降載處置。\n")
                return False
            return True
        except ImportError:
            # Fallback to standard check
            return True



    def _wake_up_memory(self):

        """[保留功能] 記憶庫喚醒"""

        pass



    def detect_and_act(self, failure_id):

        """[強化功能] 深度診斷：整合 CWE 智庫比對"""

        self._wake_up_memory()

        

        if not self.monitor_resources():

            return "Error: 資源佔用超標"



        conn = sqlite3.connect(self.db_path)

        cur = conn.cursor()

        # 讀取 RPN 相關因子：嚴重度(S)、發生率(O)、偵測度(D)

        cur.execute("SELECT severity, occurrence, detection, corrective FROM dfmea_matrix WHERE id = ?", (failure_id,))

        row = cur.fetchone()

        conn.close()

        

        if not row:

            return f"Error: 模式 {failure_id} 查無記錄"

        

        severity, occurrence, detection, action = row

        rpn = severity * occurrence * detection

        

        # 閉環邏輯：若風險過高，觸發 CWE 智庫的科學防禦方案

        if rpn > 100:

            scientific_solution = self.bridge.audit_and_repair(failure_id)

            return {"status": "CRITICAL", "solution": scientific_solution}

            

        return self._execute_action(failure_id, action)



    def _execute_action(self, fid, action):
        """[保留功能] 執行物理修正"""
        print(f"[Node-C] 偵測模式 {fid}，執行物理修正: {action}")
        return True

    def check_and_register_failure(self, failure_id, problem_point, failure_mode, severity, occurrence, detection, root_cause, prevention, corrective):
        """
        確認不良狀況是否發生過：
        - 若已存在，則返回已有對策。
        - 若未存在，則將新問題點與對策寫入資料庫 Genesis_DFMEA.db 內。
        """
        print(f"[*] [DFMEA_Engine] 開始判定不良狀況 ID: {failure_id} (問題點: {problem_point})")
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        try:
            cur.execute("SELECT id, problem_point, failure_mode, corrective FROM dfmea_matrix WHERE id = ?", (failure_id,))
            row = cur.fetchone()
            
            if row:
                print(f"[+] [DFMEA_Engine] 檢測到過去已發生過相同問題：{failure_id} | 已有對策: {row[3]}")
                conn.close()
                return {"status": "EXISTS", "corrective": row[3], "details": row}
            else:
                print("[-] [DFMEA_Engine] 此問題點未曾發生過，開始寫入新發生問題與對策...")
                cur.execute("""
                    INSERT INTO dfmea_matrix (id, problem_point, failure_mode, severity, occurrence, detection, root_cause, prevention, corrective)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (failure_id, problem_point, failure_mode, severity, occurrence, detection, root_cause, prevention, corrective))
                conn.commit()
                conn.close()
                print(f"[SUCCESS] [DFMEA_Engine] 已成功將新不良狀況 {failure_id} 及其對策寫入 Database！")
                return {"status": "NEW_REGISTERED", "corrective": corrective}
        except Exception as e:
            conn.close()
            print(f"[Error] [DFMEA_Engine] 資料庫操作失敗: {e}")
            return {"status": "ERROR", "message": str(e)}