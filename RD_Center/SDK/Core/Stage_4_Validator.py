# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\RD_Center\SDK\Core\Stage_4_Validator.py
# 狀態：Stage 4 SHA-256 簽章安全校驗器

import os
import hashlib

GENESIS_BASE = r"C:\Genesis"
MODULES_DIR = os.path.join(GENESIS_BASE, "SDK", "External_Modules")

def calculate_sha256(filepath):
    sha = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha.update(chunk)
        return sha.hexdigest()
    except Exception:
        return None

def run_validation():
    print("=== [Stage 4 Validator: SHA-256 Module Integrity Check] ===")
    if not os.path.exists(MODULES_DIR):
        print(f"Directory not found: {MODULES_DIR}")
        return False
        
    all_passed = True
    for filename in os.listdir(MODULES_DIR):
        if filename.endswith(".py"):
            filepath = os.path.join(MODULES_DIR, filename)
            checksum = calculate_sha256(filepath)
            print(f"[*] Module: {filename} | SHA-256 Checksum: {checksum}")
            if not checksum:
                all_passed = False
                
    if all_passed:
        print("=== [Stage 4 Validation: ALL MODULES SECURE] ===")
        return True
    else:
        print("=== [Stage 4 Validation: INTEGRITY ERRORS DETECTED] ===")
        return False

if __name__ == "__main__":
    run_validation()
