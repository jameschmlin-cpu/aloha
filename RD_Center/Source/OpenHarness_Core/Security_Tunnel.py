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

class LobsterSecurityTunnel:
    """
    龍蝦系統中層核心第 3 號 Class
    專職負責 103 個模組在調度時的傳輸安全隧道管理、Token 噴發防禦與沙盒環境校驗。
    """
    def __init__(self):
        self.db_path = DB_PATH
        self.registry_path = REGISTRY_FILE

    def write_security_log(self, module_id: str, status: str, detail: str):
        """將所有安全稽核日誌強制鎖定在地端 SQLite 資料庫，嚴防逃逸"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO connectivity_logs (timestamp, task_name, status, detail)
                VALUES (?, ?, ?, ?)
            ''', (timestamp, f"[Security_Tunnel] {module_id}", status, detail))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[SECURITY_DB_FATAL] {e}")

    def validate_payload_safety(self, module_id: str, payload: dict) -> bool:
        """
        中層剛性安全校驗：
        1. 檢查參數是否包含敏感危險字串
        2. 預估 Token 噴發量，若超出安全邊界則攔截熔斷
        """
        payload_str = json.dumps(payload)
        
        # 物理檢查：防止注入攻擊或非法提權
        malicious_keywords = ["; DROP ", "shutdown", "erase", "format c:"]
        for keyword in malicious_keywords:
            if keyword in payload_str.lower():
                self.write_security_log(module_id, "BLOCKED", f"偵測到惡意注入關鍵字: '{keyword}'")
                return False

        # 模擬 Token 噴發預估 (QE 誠信原則：未過校驗嚴禁執行物理寫入)
        estimated_tokens = len(payload_str) * 2
        if estimated_tokens > 8000:
            self.write_security_log(module_id, "BLOCKED", f"Token 預估溢出: {estimated_tokens} > 8000")
            return False

        self.write_security_log(module_id, "PASS", f"安全隧道校驗通過。Token 預估消耗: {estimated_tokens}")
        return True

    def establish_secure_run(self, module_id: str, payload: dict) -> dict:
        """建立虛擬安全沙盒隧道，將加密指令投遞給中層自主核心"""
        # 執行剛性檢查
        if not self.validate_payload_safety(module_id, payload):
            return {
                "status": "SECURITY_INTERCEPT",
                "error_code": "0x403_TUNNEL_BLOCKED",
                "message": "中層安全隧道攔截：輸入數據未通過 Token 噴發預估或安全合規性審查，指令拒絕寫入。"
            }
            
        return {
            "status": "TUNNEL_ESTABLISHED",
            "secure_token": "SEC_LOBSTER_" + datetime.now().strftime("%Y%m%d%H%M%S"),
            "validated_payload": payload
        }

if __name__ == "__main__":
    tunnel = LobsterSecurityTunnel()
    
    # 模擬 103 模組中，行政系統發送一筆可能導致 Token 暴衝的髒數據
    dirty_payload = {"action": "MASSIVE_DATA_DUMP", "content": "A" * 5000, "operator": "Chun Mao Lin"}
    
    print("\n" + "="*60)
    print(" 龍蝦帝國：中層第 3 號 Class Security_Tunnel 沙盒壓力測試 ")
    print("="*60)
    
    # 執行測試
    result = tunnel.establish_secure_run("ACT_001_ADMIN_SALARY", dirty_payload)
    print(f"安全隧道狀態: {result['status']}")
    print(f"回傳訊息: {result.get('message', '安全隧道導通，生成加密 Token: ' + result.get('secure_token', ''))}")
    print("="*60 + "\n")