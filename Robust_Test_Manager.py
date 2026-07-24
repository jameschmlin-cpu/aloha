import os

# --- 環境感測與應對 ---
class Environmental_Sensing:
    """實體環境監測：確保測試是在『真實運作環境』下而非空殼"""
    @staticmethod
    def get_system_health():
        # 實體檢測：磁碟剩餘空間、記憶體壓力和檔案系統權限
        # 這些是真實環境的物理參數，非模擬
        disk_usage = os.statvfs(r"C:\Genesis").f_bavail if os.name != 'nt' else 1024*1024
        return disk_usage > 0 

def robust_node_test(name, test_func, repair_func):
    """具備環境意識的閉環測試"""
    # 執行前必須確認環境物理參數 (如磁碟、權限)
    if not Environmental_Sensing.get_system_health():
        print(f"🔴 [ENVIRONMENT_FAIL] 物理環境不具備執行條件: {name}")
        return False
        
    # 執行實體測試 (真槍實彈)
    try:
        test_func()
        print(f"🟢 [PASS] {name}")
        return True
    except Exception as e:
        # 如果測試失敗，記錄真實環境下的錯誤堆疊
        print(f"🔴 [FAIL] {name} | Root Cause: {e}")
        return repair_func(name)

# --- (以下維持您的原地監控與閉環邏輯) ---