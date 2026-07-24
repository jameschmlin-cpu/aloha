import os
import sys
import hashlib
import yaml
import diskcache

try:
    import psutil
except ImportError:
    print("[ERROR] 系統未安裝 psutil，請先執行 pip install psutil")
    sys.exit(1)

GENESIS_ROOT = r"C:\Genesis"
CONFIG_PATH = os.path.join(GENESIS_ROOT, "genesis_config.yaml")

def load_genesis_config():
    """載入 Genesis 全域設定檔"""
    if not os.path.exists(CONFIG_PATH):
        print(f"[ERROR] 找不到設定檔: {CONFIG_PATH}")
        sys.exit(1)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def run_genesis_master_controller(task_type="lightweight", payload="system_health_check"):
    """
    Genesis 智慧總管主控迴圈：
    - 結合 DiskCache 檢查是否已有相同指令的快取結果，省去重複計算與 Token 消耗。
    - 依據 task_type 自動分流（lightweight vs heavyweight）。
    """
    config = load_genesis_config()
    print(f"[INFO] 正在初始化 Genesis 總管中樞 (運行模式: {config['system']['mode']})")
    
    # 初始化 DiskCache
    cache_path = config["cache"]["path"]
    os.makedirs(cache_path, exist_ok=True)
    cache = diskcache.Cache(cache_path)
    
    # 建立 payload 的雜湊作為快取 Key
    cache_key = hashlib.sha256(f"{task_type}:{payload}".encode('utf-8')).hexdigest()
    
    # 1. 檢查快取（命中則零成本返回，省去 AI 呼叫開銷）
    cached_result = cache.get(cache_key)
    if cached_result:
        print(f"[CACHE HIT] 命中 DiskCache 智慧快取，直接調用歷史結果，零成本返回！")
        return cached_result
    
    # 2. 模型分流決策
    if task_type == "lightweight":
        model_info = config["models"]["lightweight"]
        print(f"[ROUTING] 任務指派至【輕量防禦層】：使用 {model_info['model_name']}（極低資源消耗）")
        result = f"Lightweight execution completed for: {payload} using {model_info['model_name']}"
    else:
        model_info = config["models"]["heavyweight"]
        print(f"[ROUTING] 任務指派至【重磅架構層】：使用 {model_info['model_name']}（高精度重構）")
        result = f"Heavyweight execution completed for: {payload} using {model_info['model_name']}"
    
    # 3. 寫入快取
    cache.set(cache_key, result, expire=config["cache"]["expire_seconds"])
    
    # 4. 產生 Node C 實體 Hash
    hasher = hashlib.sha256(result.encode('utf-8'))
    entity_hash = hasher.hexdigest()
    print(f"[NODE C HASH] 總管閉環執行實體代碼: {entity_hash}")
    
    return result

if __name__ == "__main__":
    # 測試執行輕量巡檢任務
    run_genesis_master_controller(task_type="lightweight", payload="daily_system_audit")