# -*- coding: utf-8 -*-
import os

CORE_DIR = r"C:\Genesis\SDK\Core"
print(f"🔒 [驗證器] 正在稽核 {CORE_DIR}...")
if os.path.exists(CORE_DIR):
    print("✅ 檔案結構已確認。")
else:
    print("🚨 致命錯誤：路徑不存在，請檢查目錄名稱。")