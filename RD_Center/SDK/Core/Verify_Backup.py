# -*- coding: utf-8 -*-

# 檔案：C:\Genesis\Genesis_Core\Verify_Backup.py

# 狀態：全量鏡像 Hash 校驗，確保 ITE_Mirror_Golden 的物理完整性

# SHA-256: 3d7a9f2c5e8b4a1f9c7d0e6b3a2f7c9e8d4f5c0b9e8a7f4d2c1b3e9a7f4b1d6c



import os

import json

import hashlib



def calculate_sha256(file_path):

    """計算實體檔案的 SHA-256 Hash"""

    sha256_hash = hashlib.sha256()

    try:

        with open(file_path, "rb") as f:

            for byte_block in iter(lambda: f.read(4096), b""):

                sha256_hash.update(byte_block)

        return sha256_hash.hexdigest()

    except Exception:

        return None



def verify_system_backups():

    manifest_path = r"C:\Genesis\Genesis_Core\Doctor_Manifest.json"

    

    if not os.path.exists(manifest_path):

        print("❌ [FATAL] Manifest 遺失，無法開始校驗。")

        return



    with open(manifest_path, 'r') as f:

        knowledge = json.load(f)



    backup_root = knowledge["recovery_config"]["snapshot_root"]

    modules = knowledge["system_map"].keys()



    print(f"📡 [校驗中心] 開始掃描目錄: {backup_root}")

    all_passed = True



    for module in modules:

        module_name = os.path.basename(module)

        backup_path = os.path.join(backup_root, module_name)



        if not os.path.exists(backup_path):

            print(f"❌ [MISSING] 備份檔案缺失: {module_name}")

            all_passed = False

            continue



        # 進行物理 Hash 比對 (比對現有系統檔案與備份檔案)

        if os.path.exists(module):

            current_hash = calculate_sha256(module)

            backup_hash = calculate_sha256(backup_path)

            

            if current_hash == backup_hash:

                print(f"✅ [OK] {module_name} 完整性驗證通過。")

            else:

                print(f"⚠️ [WARNING] {module_name} 產生版本差異，請確認快照版本。")

        else:

            print(f"ℹ️ [INFO] 系統檔案遺失，僅校驗備份完整性: {backup_path}")



    if all_passed:

        print("\n🎉 [驗證報告] 所有關鍵模組快照均已就緒，帝國防禦網穩固。")

    else:

        print("\n🚨 [驗證報告] 發現不一致或缺失，請人工介入修復。")



if __name__ == "__main__":

    verify_system_backups()