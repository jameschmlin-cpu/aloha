# Category: Security

import hashlib
def verify_integrity(target_path):
    # 物理校驗邏輯：讀取目標檔案並計算 Hash 比對
    if not os.path.exists(target_path): return False
    with open(target_path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()
