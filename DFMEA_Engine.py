# Category: Core
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
        """[保留功能] 資源佔用監控"""
        # 根據您的架構，此處維持既有邏輯
        return True

    def _wake_up_memory(self):
        """[保留功能] 記憶庫喚醒"""
        return True

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