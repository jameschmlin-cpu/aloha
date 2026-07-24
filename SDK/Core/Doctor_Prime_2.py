# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\RD_Center\Source\Option\Stage_1\Doctor_Prime_2.py
# 狀態：DFMEA FM-04 徹底淨化版 (已消除空殼與邏輯真空)

import sys
import os
import time

GENESIS_ROOT = r"C:\Genesis"
SOURCE_PATH = os.path.join(GENESIS_ROOT, "RD_Center", "Source", "Option", "Stage_1")
sys.path.insert(0, SOURCE_PATH)

from Doctor_Prime import Doctor_Prime
from DFMEA_Engine import DFMEA_Engine
from DFMEA_Unified_Gate import DFMEAUnifiedGate

class Doctor_Prime_2(Doctor_Prime, DFMEA_Engine, DFMEAUnifiedGate):
    def __init__(self):
        Doctor_Prime.__init__(self)
        DFMEA_Engine.__init__(self)
        DFMEAUnifiedGate.__init__(self)
        
        # 強制進行物理完整性校驗
        if not self.verify_file_integrity(os.path.abspath(__file__)):
            self.report("FATAL", "初始完整性檢查失敗，系統進入鎖定狀態。")
            sys.exit(1)
        
        self.report("INIT", "Doctor_Prime_2 (DFMEA_Engine Verified) 已成功掛載。")

    def run_ag_cycle(self):
        """實體 AG 循環：強制執行狀態同步，無任何佔位符"""
        self.report("AG_CYCLE", "執行 ag_cycle 核心守護循環...")
        
        # 執行節點狀態同步確認 (實體動作)
        node_results = self.sync_node_status(["Node_A", "Node_B", "Node_C", "Node_D"])
        
        # 針對節點狀態進行強制決策，嚴禁無效跳轉
        if not node_results:
            self.report("WARNING", "節點同步異常，觸發強制重置程序。")
            self.reset_node_infrastructure()
        else:
            self.report("INFO", "全節點狀態同步完成，系統運行正常。")

    def run_guard(self):
        """強化版守護循環：替換所有可能導致空殼化的跳轉邏輯"""
        while True:
            # 完整性自檢
            if not self.verify_file_integrity(os.path.abspath(__file__)):
                self.report("CRITICAL", "偵測到檔案 Hash 異動，執行強制復原。")
                self.rollback_state(os.path.abspath(__file__))
                # 復原後立即重啟進程
                os.execv(sys.executable, ['python'] + sys.argv)
            
            # 執行守護循環
            self.run_ag_cycle()
            time.sleep(30)

if __name__ == "__main__":
    try:
        doc = Doctor_Prime_2()
        doc.run_guard()
    except Exception as e:
        print(f"[FATAL] 系統整合啟動失敗: {e}")
        sys.exit(1)