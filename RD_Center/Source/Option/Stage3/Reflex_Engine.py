# -*- coding: utf-8 -*-
# 檔案路徑：C:\Genesis\Genesis_Core\Stage3\Reflex_Engine.py

from Stage2.Hash_Validator import Hash_Validator
import sqlite3
import time

class Reflex_Engine(Hash_Validator):
    def __init__(self):
        super().__init__() 
        self.reflex_db = r"C:\Genesis\Library\Common_Memory\Reflex_Table.db"

    def process_reflex(self, event_id, context):
        """
        完整版決策邏輯：整合上下文感知、資料庫權重計算與狀態機判定
        """
        # 1. 前置安全檢查 (來自繼承鏈 S2)
        if not self.validate(r"C:\Genesis\Core\Dispatcher.dll"):
            return "STP_SECURITY_BLOCK"

        # 2. 實體決策邏輯：讀取多維度規則表
        conn = sqlite3.connect(self.reflex_db)
        cursor = conn.cursor()
        
        # 抓取基礎權重、反應時間閾值與風險係數
        cursor.execute("SELECT strategy, base_weight, risk_threshold FROM Rules WHERE id=?", (event_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return "STP_FALLBACK_DEFAULT"

        strategy, base_weight, risk_threshold = row
        
        # 3. 複雜決策運算 (Context-Awareness)
        # 檢查系統負載與上下文意圖 (這才是 AI Studio 對接的邏輯核心)
        is_overload = context.get('cpu_load', 0) > 85
        user_intent = context.get('intent', 'NORMAL')
        
        # 權重修正算法 (Dynamic Weight Adjustment)
        final_weight = base_weight
        if is_overload:
            final_weight -= 0.3
        if user_intent == "DEBUG":
            final_weight += 0.5
            
        # 4. 決策狀態機執行
        if final_weight < risk_threshold:
            return "STP_REFLEX_ABORT"
        elif final_weight > 1.5:
            return f"STP_REFLEX_BOOST: {strategy}"
            
        return f"STP_REFLEX_EXEC: {strategy}"

    def update_reflex_history(self, event_id, result):
        # 記錄決策歷史，確保 S4 能調用並執行自我進化
        conn = sqlite3.connect(self.reflex_db)
        conn.execute("INSERT INTO History (id, result, ts) VALUES (?, ?, ?)", 
                     (event_id, result, time.time()))
        conn.commit()
        conn.close()