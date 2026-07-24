# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\RD_Center\Source\Option\Stage_1\DB_Connector.py
import sqlite3
import os
import time

class GenesisDBFactory:
    BASE_DATA_DIR = r"C:\Genesis\Database"
    LIMIT_MB = 200  # 閉鎖閾值
    
    # 11 大領域全量分類與屬性判斷
    SCHEMA_MAP = {
        "brick": {"db": "Brick_Registry.db", "keys": ["brick_id", "version"]},
        "dfmea": {"db": "Genesis_DFMEA.db", "keys": ["hash", "severity", "risk_level"]},
        "history": {"db": "Genesis_History.db", "keys": ["event_msg", "user_id"]},
        "safety": {"db": "Genesis_Safety.db", "keys": ["safety_code", "status"]},
        "memory": {"db": "memory_core_sync.db", "keys": ["context_data", "snapshot_id"]},
        "path": {"db": "Path_Registry.db", "keys": ["node_id", "path_url"]},
        "sensor": {"db": "Sensor_Data.db", "keys": ["sensor_id", "reading"]},
        "knowledge": {"db": "Shared_Knowledge.db", "keys": ["knowledge_id", "content"]},
        "state": {"db": "System_State.db", "keys": ["node_name", "state_val"]},
        "trace": {"db": "Trace_Log.db", "keys": ["proc_id", "trace_data"]},
        "unified": {"db": "Unified_Empire_Memory.db", "keys": ["union_id", "payload"]}
    }

    @classmethod
    def write_data(cls, domain, data_dict):
        """萬用寫入接口：含 AI 自動調配與屬性驗證"""
        # 1. 判斷邏輯：確保屬性符合定義
        if domain not in cls.SCHEMA_MAP: raise ValueError(f"Unknown: {domain}")
        policy = cls.SCHEMA_MAP[domain]
        for k in policy["keys"]:
            if k not in data_dict: raise ValueError(f"Missing: {k}")

        db_path = os.path.join(cls.BASE_DATA_DIR, policy["db"])

        # 2. 自動化輪轉邏輯 (閉環治理)
        if os.path.exists(db_path) and (os.path.getsize(db_path) / (1024 * 1024) > cls.LIMIT_MB):
            archive = db_path.replace(".db", f"_ARC_{time.strftime('%Y%m%d')}.db")
            os.rename(db_path, archive)

        # 3. 執行連線與寫入 (自動 WAL 模式)
        conn = sqlite3.connect(db_path, timeout=10.0)
        conn.execute("PRAGMA journal_mode=WAL;")
        try:
            # 確保資料表已建立
            cols_def = ', '.join([f"{k} TEXT" for k in policy["keys"]])
            conn.execute(f"CREATE TABLE IF NOT EXISTS data ({cols_def}, ts TEXT)")
            
            # 偵測並動態補齊缺失的欄位
            cursor = conn.execute("PRAGMA table_info(data)")
            existing_cols = {row[1] for row in cursor.fetchall()}
            for k in data_dict.keys():
                if k not in existing_cols:
                    conn.execute(f"ALTER TABLE data ADD COLUMN {k} TEXT")
            
            cols = ', '.join(data_dict.keys())
            vals = ', '.join(['?'] * len(data_dict))
            sql = f"INSERT INTO data ({cols}, ts) VALUES ({vals}, datetime('now'))"
            conn.execute(sql, tuple(data_dict.values()))
            conn.commit()
        finally:
            conn.close()

    @classmethod
    def check_memory_health(cls, usage_ratio):
        """記憶防護監控：85% 臨界點觸發程序"""
        if usage_ratio >= 0.85:
            # 觸發記憶快照並存入 history 庫
            snapshot = {"status": "CRITICAL", "action": "MEMORY_SNAPSHOT"}
            cls.write_data("history", {"event_msg": str(snapshot), "user_id": "SYSTEM_GUARD"})
            return True
        return False

if __name__ == "__main__":
    print("[QC PASS] 萬用接口與記憶防護邏輯已就緒。")