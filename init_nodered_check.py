import os
import sys
import hashlib
import subprocess

try:
    import psutil
except ImportError:
    print("[ERROR] 系統未安裝 psutil，請先執行 pip install psutil")
    sys.exit(1)

GENESIS_ROOT = r"C:\Genesis"

def verify_nodered_installation():
    """檢查 Node-RED 是否安裝成功"""
    print("[INFO] 正在檢查 Node-RED 儀表板與遙控層狀態...")
    try:
        # 透過 psutil 檢測 node-red 指令是否存在
        result = subprocess.run(
            ["node-red", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            shell=True
        )
        
        if result.returncode == 0:
            print(f"[SUCCESS] Node-RED 版本資訊:\n{result.stdout.strip()}")
            # 產生 Node C 實體 Hash
            hasher = hashlib.sha256(result.stdout.encode('utf-8'))
            entity_hash = hasher.hexdigest()
            print(f"[NODE C HASH] Node-RED 實體校驗代碼: {entity_hash}")
            return True, entity_hash
        else:
            print(f"[ERROR] Node-RED 檢查失敗: {result.stderr}")
            return False, None
            
    except Exception as e:
        print(f"[CRITICAL] 執行過程發生異常: {str(e)}")
        return False, None

if __name__ == "__main__":
    success, h_val = verify_nodered_installation()
    if not success:
        sys.exit(1)