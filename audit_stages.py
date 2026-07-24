# Category: Data
import os
import hashlib

# 核心路徑鎖定：C:\Genesis
BASE_PATH = r"C:\Genesis\RD_Center\Source\OpenHarness\OpenHarness-main\src"
STAGES = ["Analysis", "Design", "Implementation", "Verification"]

def get_file_hash(file_path):
    """計算實體檔案的 SHA-256 Hash，確保異動可追溯"""
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def scan_stages():
    """執行全節點掃描，偵測四階段模組配置"""
    print(f"--- 啟動全節點偵測: {BASE_PATH} ---")
    report = {}
    
    for root, dirs, files in os.walk(BASE_PATH):
        for stage in STAGES:
            if stage.lower() in root.lower():
                for file in files:
                    if file.endswith(".py"):
                        path = os.path.join(root, file)
                        f_hash = get_file_hash(path)
                        report[path] = f_hash
    
    return report

if __name__ == "__main__":
    # 此處需觸發 Node A-D 偵測節點
    audit_results = scan_stages()
    
    for file_path, f_hash in audit_results.items():
        print(f"路徑: {file_path}")
        print(f"實體 Hash: {f_hash}")
        print("-" * 30)