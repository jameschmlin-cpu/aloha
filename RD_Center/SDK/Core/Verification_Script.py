# -*- coding: utf-8 -*-

# 存檔路徑：C:\Genesis\Genesis_Core\Verification_Script.py

import os

import json

import hashlib



def force_physical_write():

    base_dir = r"C:\Genesis\Genesis_Core\Data"

    if not os.path.exists(base_dir):

        os.makedirs(base_dir)

        

    data = {

        "status": "HARD_PERSISTED",

        "timestamp": "2026-06-12 00:25:00",

        "note": "此檔案由主管手動執行，絕對在地化"

    }

    

    file_path = os.path.join(base_dir, "System_Memory.json")

    with open(file_path, 'w', encoding='utf-8') as f:

        json.dump(data, f, indent=4)

        

    # 產出 Hash 以供核對

    with open(file_path, 'rb') as f:

        file_hash = hashlib.sha256(f.read()).hexdigest()

    

    return f"檔案已強制寫入於: {file_path}", f"實體 Hash: {file_hash}"



# 請您直接執行此函數

print(force_physical_write())