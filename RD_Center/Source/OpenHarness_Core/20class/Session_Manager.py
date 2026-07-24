import os
import sqlite3
import time
from datetime import datetime

# ==========================================
# 核心實體路徑定錨
# ==========================================
BASE_PATH = r"C:\Genesis"
DB_PATH = os.path.join(BASE_PATH, "Database", "Lobster_Connectivity.db")

class LobsterSessionManager:
    """
    龍蝦系統中層核心第 16 號 Class
    專職負責 WebMCP 與中層之間的通訊會期（Session）生命週期管理與動態心跳審查，防範安全逃逸。
    """
    def __init__(self):
        self.db_path = DB_PATH
        # 地端會期記憶體暫存池
        self._session_pool = {}

    def write_session_telemetry(self, session_id: str, status: str, detail: str):
        """將會期變更與心跳事件實體寫入 SQLite 行車記錄器"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO connectivity_logs (timestamp, task_name, status, detail)
                VALUES (?, ?, ?, ?)
            ''', (timestamp, f"[Session_Manager] {session_id}", status, detail))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[SESSION_DB_FATAL] {e}")

    def create_session(self, operator: str, ttl_seconds: int = 900) -> str:
        """物理簽發：為合法操作者建立獨立的安全通訊會期"""
        session_id = "SSN_" + datetime.now().strftime("%Y%m%d%H%M%S") + "_" + operator.replace(" ", "_")
        expire_time = time.time() + ttl_seconds
        
        self._session_pool[session_id] = {
            "operator": operator,
            "created_at": time.time(),
            "last_heartbeat": time.time(),
            "expires_at": expire_time,
            "status": "ACTIVE"
        }
        self.write_session_telemetry(session_id, "CREATED", f"操作者 {operator} 成功開啟通訊會期，時效 {ttl_seconds} 秒。")
        return session_id

    def verify_and_heartbeat(self, session_id: str) -> dict:
        """
        中層會期驗證核心邏輯：
        物理比對當前時間，若會期超時，冷酷熔斷並強制將狀態標記為 EXPIRED，絕不姑息。
        """
        if session_id not in self._session_pool:
            return {"status": "INVALID_SESSION", "message": "錯誤：此會期代碼在系統中不存在。"}

        session = self._session_pool[session_id]
        current_time = time.time()

        # 剛性時間閾值校驗（閉迴路會期超時攔截）
        if current_time > session["expires_at"]:
            session["status"] = "EXPIRED"
            self.write_session_telemetry(session_id, "TIMEOUT_MELTDOWN", "會期已跨越安全時間臨界點，中層強制發動防禦熔斷。")
            return {
                "status": "SESSION_MELTDOWN",
                "message": "技術瓶頸：通訊會期已超時失效，拒絕執行後續指令，控制權強制收回！"
            }

        # 更新心跳時間戳，維持會期活躍度
        session["last_heartbeat"] = current_time
        self.write_session_telemetry(session_id, "HEARTBEAT_OK", "收到心跳訊號，會期完整性確認良率 100%。")
        
        return {
            "status": "SESSION_VALID",
            "operator": session["operator"],
            "remaining_seconds": int(session["expires_at"] - current_time)
        }

if __name__ == "__main__":
    manager = LobsterSessionManager()
    
    print("\n" + "="*60)
    print(" 龍蝦帝國：中層第 16 號 Class Session_Manager 會期管理測試 ")
    print("="*60)
    
    # 1. 物理簽發最高指揮官的專屬連線會期，為測試故意將時效設為極短的 2 秒
    print("【測試 1：簽發指揮官專屬安全會期】")
    my_session = manager.create_session("Chun Mao Lin", ttl_seconds=2)
    print(f"成功生成實體會期代碼: {my_session}")
    
    # 2. 立即進行心跳驗證（預期通過）
    print("\n【測試 2：立即發起動態心跳驗證】")
    report1 = manager.verify_and_heartbeat(my_session)
    print(f"會期狀態: {report1['status']} | 剩餘可用時間: {report1.get('remaining_seconds', 0)} 秒")
    
    # 3. 實體非阻塞等待 3 秒以強行超越生命週期臨界點
    print("\n[SYSTEM] 實體定時器非阻塞等待 3 秒以觸發會期超時邊界...")
    time.sleep(3)
    
    # 4. 再次發起心跳驗證（預期超時，強制熔斷並收回控制權）
    print("\n【測試 3：超時後發起心跳驗證】")
    report2 = manager.verify_and_heartbeat(my_session)
    print(f"會期狀態: {report2['status']}")
    print(f"熔斷回報內容: {report2['message']}")
    print("="*60 + "\n")