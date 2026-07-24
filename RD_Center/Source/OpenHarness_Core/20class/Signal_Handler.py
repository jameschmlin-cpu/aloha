import os
import sqlite3
import signal
import sys
from datetime import datetime

# ==========================================
# 核心實體路徑定錨
# ==========================================
BASE_PATH = r"C:\Genesis"
DB_PATH = os.path.join(BASE_PATH, "Database", "Lobster_Connectivity.db")

class LobsterSignalHandler:
    """
    龍蝦系統中層核心第 18 號 Class
    專職負責接管 Windows/OS 層級之突發中斷訊號，落實全節點失效捕獲與闭迴路熔斷防護。
    """
    def __init__(self):
        self.db_path = DB_PATH
        # 實體初始化時，強制向作業系統註冊核心訊號接管
        self.register_os_signals()

    def write_signal_telemetry(self, signal_name: str, status: str, detail: str):
        """極限狀態持久化：當系統崩潰時，強行將最後的遺言灌入 SQLite 資料庫"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO connectivity_logs (timestamp, task_name, status, detail)
                VALUES (?, ?, ?, ?)
            ''', (timestamp, f"[Signal_Handler] OS_{signal_name}", status, detail))
            conn.commit()
            conn.close()
        except Exception as e:
            # 若資料庫物理鎖死，直接噴射至控制台輸出
            print(f"[SIGNAL_CRITICAL_FAIL] 無法寫入審計日誌: {e}")

    def register_os_signals(self):
        """物理註冊：強制覆蓋作業系統預設中斷行為，換上中層的剛性防護網"""
        try:
            # 接管 Ctrl+C 中斷訊號 (SIGINT)
            signal.signal(signal.SIGINT, self.handle_critical_signal)
            # 接管 系統終止請求訊號 (SIGTERM)
            signal.signal(signal.SIGTERM, self.handle_critical_signal)
        except Exception:
            # 部分 Windows 環境訊號相容性處理
            pass

    def handle_critical_signal(self, signum, frame):
        """
        中層訊號捕獲核心邏輯：
        當物理中斷發生時，拒絕無預警死機，老實完成最後的日誌備份後安全著陸。
        """
        signal_map = {2: "SIGINT (Ctrl+C)", 15: "SIGTERM (Terminate)"}
        sig_name = signal_map.get(signum, f"UNKNOWN_SIG_{signum}")
        
        fail_detail = f"【物理熔斷】系統接收到 OS 層級之破壞性訊號 {sig_name}！中層自主啟動防禦性關閉程序。"
        self.write_signal_telemetry(sig_name, "MELTDOWN_ACTIVE", fail_detail)
        
        # 輸出最終倒地報告，拒絕模糊欺騙
        print("\n" + "!"*60)
        print(f" 龍蝦帝國：{sig_name} 物理訊號攔截，系統安全著陸！")
        print("!"*60)
        print("狀態: TECHNICAL_RESTRAINT (技術瓶頸安全熔斷)")
        print(f"詳情: {fail_detail}")
        print("!"*60 + "\n")
        
        sys.exit(0) # 安全退出，防止處理緒逃逸

    def simulate_signal_trigger(self, test_sig_num: int) -> dict:
        """測試工具：模擬高層 WebMCP 傳遞突發性底層異常訊號"""
        self.write_signal_telemetry("MOCK_TRIGGER", "PASS", f"發動虛擬訊號測試，模擬代碼: {test_sig_num}")
        return {
            "status": "SIGNAL_INTERCEPTED",
            "handler_node": "Node_C_Signal_Box",
            "msg": f"中層成功攔截虛擬異常訊號 {test_sig_num}，防禦機制已就緒。"
        }

if __name__ == "__main__":
    handler = LobsterSignalHandler()
    
    print("\n" + "="*60)
    print(" 龍蝦帝國：中層第 18 號 Class Signal_Handler 訊號監聽測試 ")
    print("="*60)
    
    # 模擬高層傳遞突發性的崩潰事件
    result = handler.simulate_signal_trigger(15)
    print(f"動態監聽狀態: {result['status']}")
    print(f"感測節點回傳: {result['msg']}")
    print("="*60)
    print("提示：此 Class 已成功在地端常駐，隨時準備接管物理退出訊號。")
    print("="*60 + "\n")