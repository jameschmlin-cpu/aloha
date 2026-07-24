# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\RD_Center\SDK\Quality_Control\DFMEA_Module.py
# 狀態：路徑已修正為 Genesis 標準，實體邏輯閉環

import sys
import os

# 強制路徑指向 Genesis 根目錄
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

GENESIS_BASE = find_genesis_base()
sys.path.append(os.path.join(GENESIS_BASE, "RD_Center"))

from SDK.Core.Base_Template import OpenHarness_Base
from SDK.Quality_Control.Hardware_Bridge import HardwareBridge
from SDK.Quality_Control.DFMEA_CWE_Bridge import DFMEABridge

class DFMEA_Module(OpenHarness_Base):
    def __init__(self):
        super().__init__()
        self.hw_monitor = HardwareBridge()
        self.cwe_guard = DFMEABridge()
        self.db_path = os.path.join(GENESIS_BASE, "Database", "Genesis_DFMEA.db")

    def S1_Communication(self):
        """實體鏈路測試"""
        return self.hw_monitor.check_connection()

    def S2_Registry(self):
        """規則庫掛載：指向 Genesis"""
        return os.path.exists(self.db_path)

    def S3_Command_Center(self):
        return True

    def S4_Monitor_Defense(self):
        """閉環防禦：HW (Howell) -> CWE (Security)"""
        # 1. 物理感知
        hw_data = self.hw_monitor.get_physical_status()
        if hw_data.get("status") == "ERROR":
            return False
            
        # 2. CWE 安全審計
        return self.cwe_guard.audit_and_repair("SYSTEM_DEFENSE_ACTIVE")

    def run(self):
        print("[System] DFMEA_Module 啟動於 Genesis 核心路徑")
        if self.S4_Monitor_Defense():
            print("[System] 品質防禦鏈閉環成功。")
        else:
            print("[System] 風險偵測：熔斷。")

if __name__ == "__main__":
    module = DFMEA_Module()
    module.run()