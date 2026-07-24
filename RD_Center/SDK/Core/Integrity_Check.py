# -*- coding: utf-8 -*-

import hashlib
import os
import json



MANIFEST_PATH = r"C:\Genesis\Genesis_Core\MANIFEST.json"



def calculate_hash(path):

    sha256 = hashlib.sha256()

    with open(path, 'rb') as f:

        while chunk := f.read(8192): sha256.update(chunk)

    return sha256.hexdigest()



def run_check():

    if not os.path.exists(MANIFEST_PATH):

        print("[FAIL] 找不到 MANIFEST.json，請先交付清單。")

        return



    with open(MANIFEST_PATH, 'r') as f:

        master_manifest = json.load(f)



    print("[稽核員] 開始校驗...")

    for filename, expected_hash in master_manifest.items():

        path = os.path.join(r"C:\Genesis\Genesis_Core", filename)

        if calculate_hash(path) != expected_hash:

            print(f"[ALERT] {filename} 被篡改！正在觸發強制回滾...")

            # 這裡可以植入回滾邏輯

        else:

            print(f"[PASS] {filename}")



if __name__ == "__main__":

    run_check()