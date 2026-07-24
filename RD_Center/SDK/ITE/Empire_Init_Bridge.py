import os

import hashlib



# 核心路徑定義

BASE_DIR = r"C:\Genesis"

SDK_DIR = os.path.join(BASE_DIR, "SDK")

DB_PATH = r"C:\Genesis\Genesis_Core\Data\System_Core.db"



def init_empire():

    # 建立 SDK 目錄

    if not os.path.exists(SDK_DIR):

        os.makedirs(SDK_DIR)

        print(f"SDK 目錄已建立: {SDK_DIR}")

    

    # 檢查核心資料庫是否存在

    if os.path.exists(DB_PATH):

        # 計算 Hash 用於對接校驗

        with open(DB_PATH, "rb") as f:

            db_hash = hashlib.sha256(f.read()).hexdigest()

        print(f"資料庫連結成功，實體 Hash: {db_hash}")

        print("通道已打通，準備接管管理邏輯...")

    else:

        print(f"致命錯誤：找不到 System_Core.db，請確認位置: {DB_PATH}")



if __name__ == "__main__":

    init_empire()