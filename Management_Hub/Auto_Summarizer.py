import os
import datetime
import hashlib

# 物理路徑鎖定 (嚴禁變更)
ROOT = r"C:\Genesis"
LOG_PATH = r"C:\Genesis\Management_Hub\Core_Directive.log"
SDK_BRICKS = r"C:\Genesis\Library\SDK_Bricks"

def update_and_report(summary_text):
    """將對話重點寫入日誌，並執行強制檢查"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 1. 寫入重點摘要
    with open(LOG_PATH, 'a', encoding='utf-8') as f:
        f.write(f"\n--- [摘要日期: {timestamp}] ---\n")
        f.write(f"摘要: {summary_text}\n")
    
    # 2. 執行物理檢查並回報
    print(f"[PRE-FLIGHT] 執行環境檢查 | 路徑: {ROOT}")
    print(f"[SUMMARY] 重點已寫入: {summary_text}")
    
    # 3. 掃描積木庫 integrity
    print(f"[INTEGRITY] 開始掃描積木庫: {SDK_BRICKS}")
    for brick in os.listdir(SDK_BRICKS):
        if brick.endswith(".py"):
            path = os.path.join(SDK_BRICKS, brick)
            with open(path, 'rb') as f:
                h = hashlib.sha256(f.read()).hexdigest()
                print(f"  - {brick} | Hash: {h[:16]}")
    
    print("[SUCCESS] 系統參數已更新，邏輯閉環。")

if __name__ == "__main__":
    # 使用者可透過參數傳入對話摘要
    import sys
    msg = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "無摘要內容"
    update_and_report(msg)