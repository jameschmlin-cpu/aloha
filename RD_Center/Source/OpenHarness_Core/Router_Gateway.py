import json
import os
import sqlite3
from datetime import datetime

# ==========================================
# 核心實體路徑定錨
# ==========================================
BASE_PATH = r"C:\Genesis"
DB_PATH = os.path.join(BASE_PATH, "Database", "Lobster_Connectivity.db")
REGISTRY_FILE = os.path.join(BASE_PATH, "SDK", "Registry.json")

class LobsterRouterGateway:
    """
    龍蝦系統中層核心第 17 號 Class
    專職負責全局 103 個模組之動態路由分流與網關隔離，確保各系統模組間的物理邊界清晰。
    """
    def __init__(self):
        self.db_path = DB_PATH
        self.registry_path = REGISTRY_FILE

    def write_router_telemetry(self, route_path: str, status: str, detail: str):
        """標準化網關日誌落地：強制寫入 SQLite 行車記錄器"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO connectivity_logs (timestamp, task_name, status, detail)
                VALUES (?, ?, ?, ?)
            ''', (timestamp, f"[Router_Gateway] {route_path}", status, detail))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[ROUTER_DB_FATAL] {e}")

    def route_to_component(self, raw_intent: dict) -> dict:
        """
        中層網關路由核心邏輯：
        解析高層意圖，強制依據 Keep 藍圖的 5 大群組進行物理路徑分流與核可驗證。
        """
        module_id = raw_intent.get("module_id", "UNKNOWN")
        action = raw_intent.get("action", "UNKNOWN")
        
        # 1. 安全提權查驗：解析模組首碼 (前綴)
        prefix = module_id.split("_")[0] if "_" in module_id else "INVALID"
        
        # 2. 物理網關過濾：驗證是否屬於 Keep 藍圖定義之 5 大群組
        valid_prefixes = ["ACT", "FIN", "AUT", "OPR", "SYS"]
        if prefix not in valid_prefixes:
            fail_detail = f"網關攔截：非法路由請求！模組識別碼 {module_id} 的前綴不符合五大群組資產規範。"
            self.write_router_telemetry(f"REJECT/{module_id}", "BLOCKED", fail_detail)
            return {
                "status": "TECHNICAL_RESTRAINT",
                "error_code": "0x502_BAD_GATEWAY",
                "message": fail_detail
            }

        # 3. 讀取 Registry.json 進行實體拓撲咬合驗證
        with open(self.registry_path, 'r', encoding='utf-8') as f:
            registry = json.load(f)

        if module_id not in registry.get("components", {}):
            fail_detail = f"技術瓶頸：網關拒絕路由！目標組件 {module_id} 尚未在中層註冊，無法建立實體管線。"
            self.write_router_telemetry(f"DENY/{module_id}", "REJECTED", fail_detail)
            return {
                "status": "TECHNICAL_RESTRAINT",
                "error_code": "0x404_ROUTE_NOT_FOUND",
                "message": fail_detail
            }

        # 4. 路由分流成功，封裝標準網關傳輸合約
        target_file = registry["components"][module_id].get("file_name", "UNKNOWN.py")
        physical_route = os.path.join(BASE_PATH, "SDK", "Components", target_file)
        
        success_detail = f"網關動態路由導通成功！指令 {action} 已成功分流至 {prefix} 資料總線。實體對位路徑: {physical_route}"
        self.write_router_telemetry(f"FORWARD/{module_id}", "PASS", success_detail)
        
        return {
            "status": "GATEWAY_FORWARDED",
            "route_info": {
                "group_prefix": prefix,
                "target_module": module_id,
                "physical_target_path": physical_route,
                "action_intent": action
            },
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

if __name__ == "__main__":
    router = LobsterRouterGateway()
    
    print("\n" + "="*60)
    print(" 龍蝦帝國：中層第 17 號 Class Router_Gateway 網關路由測試 ")
    print("="*60)
    
    # 測試情境 1：合法路由至已掛戶籍的行政薪資模組
    print("【測試 1：合法 5 大群組指令路由分流】")
    intent1 = {"module_id": "ACT_001_ADMIN_SALARY", "action": "CALCULATE_SOP"}
    report1 = router.route_to_component(intent1)
    print(f"網關分流狀態: {report1['status']}\n路由目標路徑: {report1.get('route_info', {}).get('physical_target_path', 'NONE')}")
    
    print("-" * 50)
    
    # 測試情境 2：外部惡意或大鍋炒的混亂垃圾指令試圖闖入網關
    print("【測試 2：非法前綴惡意入侵網關】")
    intent2 = {"module_id": "BAD_FRAUD_MOD", "action": "ESCAPE_LOGIC"}
    report2 = router.route_to_component(intent2)
    print(f"網關分流狀態: {report2['status']}\n攔截回報內容: {report2['message']}")
    print("="*60 + "\n")