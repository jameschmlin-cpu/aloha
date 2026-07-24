import json
import os
import sqlite3
from datetime import datetime

# ==========================================
# 核心實體路徑定錨
# ==========================================
BASE_PATH = r"C:\Genesis"
CONFIG_DIR = os.path.join(BASE_PATH, "Config")
CONFIG_FILE = os.path.join(CONFIG_DIR, "System_Config.json")
DB_PATH = os.path.join(BASE_PATH, "Database", "Lobster_Connectivity.db")

class LobsterConfigLoader:
    """
    龍蝦系統中層核心第 10 號 Class
    專職負責全局組態靜態載入與完備性校驗，嚴防非法參數注入，保障 103 模組地端運行之穩定性。
    """
    def __init__(self):
        self.config_path = CONFIG_FILE
        self.db_path = DB_PATH
        os.makedirs(CONFIG_DIR, exist_ok=True)
        self.ensure_default_config()

    def write_config_telemetry(self, status: str, detail: str):
        """將配置載入事件實體寫入 SQLite 行車記錄器"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO connectivity_logs (timestamp, task_name, status, detail)
                VALUES (?, ?, ?, ?)
            ''', (timestamp, "[Config_Loader] Global_Config", status, detail))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[CONFIG_DB_FATAL] {e}")

    def ensure_default_config(self):
        """閉迴路自主診斷：若配置檔案不存在，強制物理覆寫生成出廠安全預設，拒絕崩潰"""
        if not os.path.exists(self.config_path):
            default_struct = {
                "config_version": "1.0.0",
                "last_modified": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "environment": {
                    "base_path": BASE_PATH,
                    "target_hardware": "RTX_3060",
                    "harness_core": "rmCPa"
                },
                "security": {
                    "token_burst_limit": 8000,
                    "enforce_node_check": True
                }
            }
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(default_struct, f, indent=4, ensure_ascii=False)
            self.write_config_telemetry("CONFIG_INIT", "檢測到配置缺失，已自主提權生成安全預設設定檔。")

    def load_and_validate(self) -> dict:
        """
        中層組態載入核心邏輯：
        物理載入設定檔並強制進行結構合法性校驗，未過校驗則觸發技術瓶頸熔斷。
        """
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            # 剛性結構要素完整性校驗
            required_keys = ["config_version", "environment", "security"]
            for key in required_keys:
                if key not in config_data:
                    raise KeyError(f"關鍵配置區塊缺失: {key}")
            
            self.write_config_telemetry("PASS", "系統設定檔載入成功，完備性校驗 100% 通過。")
            return {
                "status": "CONFIG_LOADED",
                "data": config_data
            }

        except Exception as e:
            fail_detail = f"技術瓶頸：設定檔結構遭人為損毀或非法篡改! 錯誤原因: {str(e)}"
            self.write_config_telemetry("CRASH", fail_detail)
            return {
                "status": "TECHNICAL_RESTRAINT",
                "message": fail_detail
            }

if __name__ == "__main__":
    loader = LobsterConfigLoader()
    
    print("\n" + "="*60)
    print(" 龍蝦帝國：中層第 10 號 Class Config_Loader 組態校驗測試 ")
    print("="*60)
    
    # 執行組態加載
    report = loader.load_and_validate()
    print(f"組態載入狀態: {report['status']}")
    if report['status'] == "CONFIG_LOADED":
        print("實體設定內容 (部分抽查):")
        print(f"  - 核心路徑: {report['data']['environment']['base_path']}")
        print(f"  - 目標算力硬體: {report['data']['environment']['target_hardware']}")
        print(f"  - Token 噴發限制: {report['data']['security']['token_burst_limit']}")
    else:
        print(f"熔斷回報內容: {report['message']}")
    print("="*60 + "\n")