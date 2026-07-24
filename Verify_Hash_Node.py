# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\Verify_Hash_Node.py
# 目的：對同步錨點進行 SHA-256 實體校驗，符合 Node C 節點要求

import hashlib
import os

TARGET_DB = r"C:\Genesis\Database\memory_core_sync.db"

def calculate_sha256(filepath):
    sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while True:
                data = f.read(65536)
                if not data: break
                sha256.update(data)
        return sha256.hexdigest().upper()
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    if os.path.exists(TARGET_DB):
        file_hash = calculate_sha256(TARGET_DB)
        print("--- Node C 節點驗證 ---")
        print(f"檔案路徑: {TARGET_DB}")
        print(f"SHA-256: {file_hash}")
        print("-----------------------")
    else:
        print(f"[❌] 錯誤：找不到目標檔案 {TARGET_DB}")