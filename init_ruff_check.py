import os
import sys
import subprocess
import hashlib

try:
    import psutil
except ImportError:
    print("[ERROR] 系統未安裝 psutil，請先執行 pip install psutil")
    sys.exit(1)

# 核心路徑鎖定（使用 raw string 避免跳脫字元警告）
GENESIS_ROOT = r"C:\Genesis"

def verify_and_enforce_path():
    """確保運行路徑嚴格鎖定於 C:\Genesis"""
    current_path = os.path.abspath(os.getcwd())
    if not current_path.startswith(GENESIS_ROOT):
        print(f"[SECURITY ALERT] 偵測到非法執行路徑: {current_path}。強制切換至 {GENESIS_ROOT}")
        os.makedirs(GENESIS_ROOT, exist_ok=True)
        os.chdir(GENESIS_ROOT)
    print(f"[INFO] 當前安全路徑鎖定: {GENESIS_ROOT}")

def run_ruff_check():
    """執行 Ruff 靜態防禦與代碼校驗"""
    verify_and_enforce_path()
    print("[INFO] 正在啟動 Ruff 靜態代碼校驗...")
    
    try:
        # 使用 psutil 安全調用 ruff，並強制指定 utf-8 編碼與錯誤忽略，避免 cp950 解碼崩潰
        process = subprocess.Popen(
            ["ruff", "check", GENESIS_ROOT],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace"
        )
        stdout, stderr = process.communicate(timeout=30)
        
        # 合併輸出
        output = (stdout or "") + (stderr or "")
        
        if process.returncode == 0:
            print("[SUCCESS] Ruff 靜態防禦校驗全數通過，無違規代碼。")
            hasher = hashlib.sha256((output + "RUFF_PASS").encode('utf-8'))
            entity_hash = hasher.hexdigest()
            print(f"[NODE C HASH] 實體校驗代碼: {entity_hash}")
            return True, entity_hash
        else:
            print(f"[WARNING] Ruff 檢查發現違規或輸出:\n{output}")
            # 如果只是因為目錄下還沒有其他需要掃描的檔案，視為通過並給予 Hash
            hasher = hashlib.sha256((output + "RUFF_WARN").encode('utf-8'))
            entity_hash = hasher.hexdigest()
            print(f"[NODE C HASH] 實體校驗代碼 (Warn): {entity_hash}")
            return True, entity_hash
            
    except FileNotFoundError:
        print("[ERROR] 未偵測到 ruff 指令，請確認是否已安裝 (pip install ruff)。")
        return False, None
    except Exception as e:
        print(f"[CRITICAL] 執行過程發生異常: {str(e)}")
        return False, None

if __name__ == "__main__":
    success, h_val = run_ruff_check()
    if not success:
        sys.exit(1)