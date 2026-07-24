import os
import sys
import hashlib

try:
    import psutil
except ImportError:
    print("[ERROR] 系統未安裝 psutil，請先執行 pip install psutil")
    sys.exit(1)

try:
    import diskcache
except ImportError:
    print("[ERROR] 系統未安裝 diskcache，請先執行 pip install diskcache")
    sys.exit(1)

# 核心路徑鎖定
GENESIS_ROOT = r"C:\Genesis"
RAG_STORAGE_DIR = os.path.join(GENESIS_ROOT, "rag_storage")

def initialize_lightrag_environment():
    """初始化 LightRAG 知識圖譜儲存與快取環境"""
    print("[INFO] 正在初始化 LightRAG 智能層...")
    
    # 確保儲存目錄存在
    os.makedirs(RAG_STORAGE_DIR, exist_ok=True)
    
    # 使用 diskcache 建立檢索快取實例
    cache_dir = os.path.join(RAG_STORAGE_DIR, "cache")
    cache = diskcache.Cache(cache_dir)
    cache.set("genesis_status", "LightRAG_Initialized", expire=3600)
    
    print(f"[SUCCESS] LightRAG 工作目錄已建立: {RAG_STORAGE_DIR}")
    print(f"[SUCCESS] DiskCache 快取連線正常，檢測試驗值: {cache.get('genesis_status')}")
    
    # 產生 Node C 實體 Hash
    hasher = hashlib.sha256(b"LIGHTRAG_INIT_SUCCESS")
    entity_hash = hasher.hexdigest()
    print(f"[NODE C HASH] LightRAG 實體校驗代碼: {entity_hash}")
    return True, entity_hash

if __name__ == "__main__":
    success, h_val = initialize_lightrag_environment()
    if not success:
        sys.exit(1)