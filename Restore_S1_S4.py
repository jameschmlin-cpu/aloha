import zipfile
import os

# 物理路徑鎖定：絕不更動現有 RD_Center 目錄
TARGET_DIR = r"C:\Genesis\RD_Center\Source\OpenHarness"
SOURCE_ZIP = r"C:\Genesis\RD_Center\Source\OpenHarness.zip" # 請確認您的原始 zip 檔名是否為此

def restore_logic():
    # 建立乾淨的隔離區
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)
        print(f"[系統] 已建立隔離區: {TARGET_DIR}")
    else:
        print("[系統] 隔離區已存在，準備解壓...")

    # 執行解壓 (由您授權執行)
    try:
        with zipfile.ZipFile(SOURCE_ZIP, 'r') as zip_ref:
            zip_ref.extractall(TARGET_DIR)
            print(f"[成功] S1-S4 原始檔案已還原至: {TARGET_DIR}")
            print("[警告] 請確認 RD_Center 目錄保持原狀，切勿進行任何移動。")
    except Exception as e:
        print(f"[錯誤] 檔案操作失敗: {e}")
        print("請確認原始 zip 檔名與路徑是否正確。")

if __name__ == "__main__":
    restore_logic()