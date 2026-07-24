import hashlib
import subprocess

# 設定監控路徑
TARGET_DIR = r"C:\Genesis"

def calculate_hash(file_path):
    """計算實體檔案的 SHA-256 Hash"""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def validate_node(file_path, expected_hash):
    """Node C: 整合與 Hash 驗證節點"""
    actual_hash = calculate_hash(file_path)
    if actual_hash != expected_hash:
        print(f"[Node C 失敗] Hash 不匹配！目標: {expected_hash}, 實體: {actual_hash}")
        return False
    
    # 執行基本的語法檢查 (以 Python 為例)
    result = subprocess.run(['python', '-m', 'py_compile', file_path], capture_output=True)
    if result.returncode != 0:
        print(f"[Node A/B 失敗] 語法檢查未通過: {result.stderr.decode()}")
        return False
        
    print(f"[Node C 通過] 檔案路徑: {file_path}, Hash 已驗證。")
    return True

# 模擬 Gem 輸出觸發的驗證邏輯
if __name__ == "__main__":
    # 此處預留給 Gem 輸出的 JSON 接口
    # 範例：{"file": "main.py", "hash": "..."}
    pass