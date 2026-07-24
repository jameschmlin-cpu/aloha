# -*- coding: utf-8 -*-
import os
import sys

# 鎖定您的核心路徑結構
TARGET_ROOT = r"C:\Genesis"
STAGE_1_DIR = r"C:\Genesis\RD_Center\Source\Option\Stage_1"

def check_link():
    print("=== [系統連結稽核器] 開始檢查 ===")
    
    # 1. 檢查檔案是否存在
    doctor_path = os.path.join(STAGE_1_DIR, "Doctor_Prime.py")
    guardian_path = os.path.join(STAGE_1_DIR, "Guardian_Bot.py")
    
    files_to_check = {"Doctor_Prime": doctor_path, "Guardian_Bot": guardian_path}
    
    for name, path in files_to_check.items():
        if os.path.exists(path):
            print(f"[OK] 模組存在: {name}")
        else:
            print(f"[ERROR] 檔案遺失: {name}，預期路徑: {path}")
            return

    # 2. 測試匯入連結 (動態載入測試)
    try:
        sys.path.append(STAGE_1_DIR)
        from Doctor_Prime import Doctor_Prime
        
        print("[OK] Python 模組掛載成功。")
        
        # 3. 測試連結對接
        doc = Doctor_Prime()
        print("[OK] Doctor_Prime 實例化成功。")
        
        # 模擬呼叫測試
        if hasattr(doc, 'run_guard'):
            print("[OK] Doctor_Prime 偵測到 Guardian 閉環介面。")
        else:
            print("[WARNING] Doctor_Prime 未偵測到完整閉環介面，請檢查繼承狀況。")
            
    except Exception as e:
        print(f"[CRITICAL] 連結驗證失敗: {str(e)}")
        return

    print("=== [稽核完成] 系統連結狀態：健康 ===")

if __name__ == "__main__":
    check_link()