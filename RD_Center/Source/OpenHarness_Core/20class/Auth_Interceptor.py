import os
import sqlite3
from datetime import datetime

# ==========================================
# 核心實體路徑定錨
# ==========================================
BASE_PATH = r"C:\Genesis"
DB_PATH = os.path.join(BASE_PATH, "Database", "Lobster_Connectivity.db")
REGISTRY_FILE = os.path.join(BASE_PATH, "SDK", "Registry.json")

class LobsterAuthInterceptor:
    """
    龍蝦系統中層核心第 9 號 Class
    專職負責 103 個功能模組調度時的權限權杖檢查與核心操作提權審計，確保地端權限不可篡改。
    """
    def __init__(self):
        self.db_path = DB_PATH
        self.registry_path = REGISTRY_FILE
        # 定義剛性權限階層 (Role-Based Access Control)
        self.ROLE_PERMISSIONS = {
            "Chun Mao Lin": 100,  # 最高指揮官級別
            "SYSTEM": 90,         # 系統自主節點級別
            "GUEST_AI": 10        # 一般推論 AI 級別 (受嚴格限制)
        }

    def write_audit_log(self, operator: str, module_id: str, action: str, status: str, detail: str):
        """安檢稽核日誌持久化：強制寫入 SQLite 安全審計表"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO connectivity_logs (timestamp, task_name, status, detail)
                VALUES (?, ?, ?, ?)
            ''', (timestamp, f"[Auth_Interceptor] {operator} -> {module_id}", status, f"[{action}] {detail}"))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[AUTH_DB_FATAL] {e}")

    def intercept_and_verify(self, operator: str, module_id: str, action: str, required_level: int = 50) -> dict:
        """
        中層權限攔截核心邏輯：
        校驗操作者的權限權杖，低於所需等級者直接執行物理攔截，拒絕向下傳遞。
        """
        self.write_audit_log(operator, module_id, action, "AUDIT_START", f"發起操作請求，要求權限等級: {required_level}")

        # 1. 識別操作者合法性與權限等級
        operator_level = self.ROLE_PERMISSIONS.get(operator, 0)

        # 2. 剛性權限閾值比對
        if operator_level < required_level:
            fail_detail = f"權限阻斷：操作者 {operator}(等級:{operator_level}) 權限不足，無法執行要求等級 {required_level} 的核心操作！"
            self.write_audit_log(operator, module_id, action, "DENIED", fail_detail)
            return {
                "status": "PERMISSION_DENIED",
                "auth_code": "0x401_UNAUTHORIZED",
                "message": fail_detail,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

        # 3. 通過安檢，簽發中層准行證
        success_detail = f"權限驗證通過！操作者 {operator}(等級:{operator_level}) 成功導通至核心權限隧道。"
        self.write_audit_log(operator, module_id, action, "ALLOWED", success_detail)
        
        return {
            "status": "AUTH_PASSED",
            "auth_code": "0x00_AUTHORIZED",
            "token_claims": {
                "user": operator,
                "cleared_level": operator_level,
                "target_module": module_id
            },
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

if __name__ == "__main__":
    interceptor = LobsterAuthInterceptor()
    
    print("\n" + "="*60)
    print(" 龍蝦帝國：中層第 9 號 Class Auth_Interceptor 剛性安檢測試 ")
    print("="*60)
    
    # 測試情境 1：最高指揮官 Chun Mao Lin 調度敏感的行政加退保模組（預期通過）
    print("【測試 1：最高指揮官合法發動指令】")
    report1 = interceptor.intercept_and_verify(
        operator="Chun Mao Lin",
        module_id="ACT_001_ADMIN_SALARY",
        action="EXECUTE_INSURANCE_FLOW",
        required_level=80 # 高階核心操作
    )
    print(f"安全閘門狀態: {report1['status']} | 回報: {report1['message'] if 'message' in report1 else '准行權權杖已發放'}")
    
    print("-" * 50)
    
    # 測試情境 2：前任騙子或未授權的外部 Guest 試圖修改金流變數（預期物理攔截）
    print("【測試 2：非法 Guest 試圖越權竄改】")
    report2 = interceptor.intercept_and_verify(
        operator="GUEST_AI",
        module_id="FIN_002_PAYMENT_GATEWAY",
        action="ALTER_CURRENCY_CONFIG",
        required_level=90 # 極高金流級別
    )
    print(f"安全閘門狀態: {report2['status']}")
    print(f"攔截回報內容: {report2['message']}")
    print("="*60 + "\n")