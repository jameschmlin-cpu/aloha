import os
import sqlite3
import time
from datetime import datetime

# ==========================================
# 核心實體路徑定錨
# ==========================================
BASE_PATH = r"C:\Genesis"
DB_PATH = os.path.join(BASE_PATH, "Database", "Lobster_Connectivity.db")

class LobsterCacheController:
    """
    龍蝦系統中層核心第 12 號 Class
    專職負責全局記憶體快取控管，優化地端 I/O 效率，保障 103 模組數據調度之高速回傳。
    """
    def __init__(self):
        self.db_path = DB_PATH
        # 實體靜態記憶體快取字典空間
        self._cache_pool = {}

    def write_cache_telemetry(self, status: str, detail: str):
        """將快取調度事件實體寫入 SQLite 行車記錄器"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO connectivity_logs (timestamp, task_name, status, detail)
                VALUES (?, ?, ?, ?)
            ''', (timestamp, "[Cache_Controller] RAM_Buffer", status, detail))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[CACHE_DB_FATAL] {e}")

    def set_cache(self, key: str, value: dict, ttl_seconds: int = 60):
        """物理寫入：將高層數據塞入中層記憶體快取，並設定剛性生命週期 (TTL)"""
        expire_time = time.time() + ttl_seconds
        self._cache_pool[key] = {
            "data": value,
            "expires_at": expire_time
        }
        self.write_cache_telemetry("CACHE_SET", f"成功為鍵值 '{key}' 建立 RAM 快取，生命週期: {ttl_seconds} 秒。")

    def get_cache(self, key: str) -> dict:
        """
        中層快取讀取核心邏輯：
        物理比對當前時間，若快取超時則實體執行記憶體排空（Eviction），老實熔斷並回報過期。
        """
        if key not in self._cache_pool:
            return {"status": "CACHE_MISS", "data": None}

        cache_item = self._cache_pool[key]
        
        # 剛性時間閾值校驗（閉迴路淘汰）
        if time.time() > cache_item["expires_at"]:
            # 物理清除超時數據，嚴防過期髒數據脫逃
            del self._cache_pool[key]
            self.write_cache_telemetry("CACHE_EXPIRED", f"鍵值 '{key}' 快取超時，已實體執行記憶體清空。")
            return {"status": "CACHE_MISS", "data": None}

        self.write_cache_telemetry("CACHE_HIT", f"成功從 RAM 緩衝區擊中鍵值 '{key}' 的實體快取。")
        return {
            "status": "CACHE_HIT",
            "data": cache_item["data"]
        }

if __name__ == "__main__":
    controller = LobsterCacheController()
    
    print("\n" + "="*60)
    print(" 龍蝦帝國：中層第 12 號 Class Cache_Controller 記憶體快取測試 ")
    print("="*60)
    
    # 模擬 103 模組的行政參數數據
    mock_salary_config = {"base_level": "QE_MASTER", "hourly_rate": 1500}
    
    # 1. 物理寫入快取，生命週期故意設成極短的 2 秒
    print("【測試 1：物理寫入快取暫存】")
    controller.set_cache("act_salary_policy", mock_salary_config, ttl_seconds=2)
    
    # 2. 立即讀取（預期命中 CACHE_HIT）
    print("\n【測試 2：立即發起快取調度】")
    report1 = controller.get_cache("act_salary_policy")
    print(f"調度狀態: {report1['status']} | 內容: {report1['data']}")
    
    # 3. 實體阻塞 3 秒，模擬時間流逝
    print("\n[SYSTEM] 實體定時器非阻塞等待 3 秒以觸發生命週期臨界點...")
    time.sleep(3)
    
    # 4. 再次讀取（預期因超時而淘汰 CACHE_MISS）
    print("\n【測試 3：超時後再次發起快取調度】")
    report2 = controller.get_cache("act_salary_policy")
    print(f"調度狀態: {report2['status']} | 內容: {report2['data']} (成功自動熔斷並排空記憶體)")
    print("="*60 + "\n")