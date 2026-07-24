import os
import sys
import hashlib

# 物理路徑鎖定：絕不推論，絕不變更
ROOT = r"C:\Genesis"
HUB = r"C:\Genesis\Management_Hub"
SDK_BRICKS = r"C:\Genesis\Library\SDK_Bricks"
DIRECTIVE_LOG = r"C:\Genesis\Management_Hub\Core_Directive.log"

def pre_flight_check():
    print(f"[PRE-FLIGHT] 執行環境檢查 | 路徑: {ROOT}")
    
    # 檢查必要目錄
    critical_paths = [ROOT, HUB, SDK_BRICKS]
    for path in critical_paths:
        if not os.path.exists(path):
            print(f"[FATAL] 物理路徑缺失: {path}")
            sys.exit(1)
            
    # 檢查 Core_Directive.log 是否存在並載入參數
    if not os.path.exists(DIRECTIVE_LOG):
        print("[WARNING] 核心指令檔缺失，自動建立...")
        with open(DIRECTIVE_LOG, 'w', encoding='utf-8') as f:
            f.write("PATH_LOCK:C:\\Genesis\nMODE:CLOSED_LOOP\nNO_HALUCINATION:TRUE")
            
    # 掃描積木庫 integrity
    print(f"[INTEGRITY] 開始掃描積木庫: {SDK_BRICKS}")
    for brick in os.listdir(SDK_BRICKS):
        if brick.endswith(".py"):
            path = os.path.join(SDK_BRICKS, brick)
            with open(path, 'rb') as f:
                h = hashlib.sha256(f.read()).hexdigest()
                print(f"  - {brick} | Hash: {h[:16]}")
    
    print("[SUCCESS] 帝國邏輯閉環，系統就緒。")

if __name__ == "__main__":
    pre_flight_check()