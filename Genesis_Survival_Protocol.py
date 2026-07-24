import os
import stat
import subprocess
import sqlite3
import time
from genesis_gateway import GenesisGateway

class SurvivalMode:
    def __init__(self, base_path=r"C:\Genesis"):
        self.base_path = base_path
        self.gateway = GenesisGateway()
        # 從網關動態獲取關鍵路徑，而非硬編碼
        self.dfmea_path = self.gateway.paths.get("dfmea_db")
        self.compiler_guard = os.path.join(base_path, "Genesis_Compiler_Guard.py")
        self.is_offline = False

    def check_connection(self):
        """偵測網路狀態，回傳 True 為連線，False 為斷網"""
        return os.system("ping -n 1 8.8.8.8 >nul") == 0

    def trigger_survival(self):
        """核心應變邏輯：物理鎖定 -> 背景編譯器啟動 -> 本地編組"""
        print("[!] 偵測到網路異常中斷，即刻啟動地端動態編組生存模式...")
        
        # 1. 鎖定本地 DFMEA 資料庫，防止外部非法寫入
        if os.path.exists(self.dfmea_path):
            # 將權限設為唯讀 (Read-Only)
            os.chmod(self.dfmea_path, stat.S_IREAD)
            print(f"[安全鎖定] DFMEA 資料庫已物理鎖定: {self.dfmea_path}")
        
        # 2. 自動啟動本地輕量級編譯器 (Compiler_Guard)
        if os.path.exists(self.compiler_guard):
            subprocess.Popen(["python", self.compiler_guard, "--mode", "local_emergency"], 
                             shell=True, stdout=subprocess.DEVNULL)
            print("[核心守護] 本地 Compiler_Guard 門禁已啟動")

        # 3. 執行「本地優先」邏輯轉移 (模擬節點動態編組)
        # 檢查本地 Registry 是否有 PENDING 任務，並將其提升為高優先級
        conn = sqlite3.connect(self.gateway.paths.get("db"))
        cursor = conn.cursor()
        cursor.execute("UPDATE interaction_history SET context = '[LOCAL_ACTIVE]' || context WHERE context LIKE 'TODO%'")
        conn.commit()
        conn.close()
        print("[離線編組] 所有本地任務佇列已活化，進入自主作業模式。")

# 監控迴圈
def monitor_loop():
    survival = SurvivalMode()
    while True:
        if not survival.check_connection():
            if not survival.is_offline:
                survival.trigger_survival()
                survival.is_offline = True
        else:
            if survival.is_offline:
                print("[+] 網路恢復，解除生存模式限制。")
                # 解除唯讀鎖定
                os.chmod(survival.dfmea_path, stat.S_IWRITE)
                survival.is_offline = False
        time.sleep(10)

if __name__ == "__main__":
    monitor_loop()