# -*- coding: utf-8 -*-
# 檔案位置: C:\Genesis\Library\SDK\Agent_Library_Bridge.py
import sys
sys.path.append(r"C:\Genesis")

from Base_Template import Base_Template
from Library_Main import LibraryCore

class Agent_Library_Bridge(Base_Template, LibraryCore):
    """【記憶橋接器】負責資料庫存取"""
    def __init__(self, brick_id="BRIDGE_01"):
        Base_Template.__init__(self, brick_id=brick_id)
        LibraryCore.__init__(self, db_path=r"C:\Genesis\Library\LibOption\LibrarySystem\Shared_Knowledge.db")

    def get_intelligent_advice(self, fm_code):
        def task():
            # 顯式呼叫 LibraryCore 的查詢邏輯，避免多重繼承之 MRO 尋址錯誤
            return LibraryCore.query(self, fm_code)
        return self.run_protected(stage_id="QUERY", task=task)