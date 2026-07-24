import os
import hashlib

# 設定
TARGET_PATHS = [
    r"C:\Genesis\RD_Center\SDK\Core",
    r"C:\Genesis\RD_Center\SDK\ITE",
    r"C:\Genesis\RD_Center\SDK\System"
]
LOG_FILE = r"C:\Genesis\Genesis_Ultimate_Audit.log"
TOXIN_KEYWORDS = ["os.remove", "shutil.rmtree", "os.system('rm", "eval(", "exec("]

def get_hash(path):
    sha256 = hashlib.sha256()
    try:
        with open(path, 'rb') as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()
    except:
        return "ERROR"

def scan_file(path):
    detected_toxins = []
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        for t in TOXIN_KEYWORDS:
            if t in content:
                detected_toxins.append(t)
    return detected_toxins

def run_ultimate_guard():
    print("[系統] 帝國安全法醫掃描啟動...")
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        f.write("--- Genesis 帝國安全與完整性審計報告 ---\n")
        
        for base_path in TARGET_PATHS:
            for root, _, files in os.walk(base_path):
                for file in files:
                    if file.endswith(".py"):
                        full_path = os.path.join(root, file)
                        
                        # 1. 安全掃描
                        toxins = scan_file(full_path)
                        status = "OK" if not toxins else f"TOXIN_DETECTED: {toxins}"
                        
                        # 2. 完整性計算
                        f_hash = get_hash(full_path)
                        
                        log_line = f"檔案: {file} | 路徑: {full_path} | 狀態: {status} | Hash: {f_hash}\n"
                        f.write(log_line)
                        if toxins:
                            print(f"[警告] 發現威脅在 {file}!")
    
    print(f"[完成] 審計報告已產出: {LOG_FILE}")

if __name__ == "__main__":
    run_ultimate_guard()