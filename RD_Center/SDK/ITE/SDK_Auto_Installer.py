# -*- coding: utf-8 -*-

import os

import hashlib



def auto_deploy():

    print("="*60)

    print(" 🚀 龍蝦帝國 SDK 實體部署補救程序 ")

    print("="*60)



    # 1. 定義要補齊的 DataIntegrity.py 核心邏輯

    data_integrity_content = """# -*- coding: utf-8 -*-

import hashlib

import os



class DataIntegrity:

    '''SDK 核心：負責所有檔案的實體 Hash 校驗與完整性監控'''

    def __init__(self, base_path="C:\\\\ITE"):

        self.base_path = base_path



    def calculate_hash(self, file_path):

        if not os.path.exists(file_path): return None

        sha256_hash = hashlib.sha256()

        with open(file_path, "rb") as f:

            for byte_block in iter(lambda: f.read(4096), b""):

                sha256_hash.update(byte_block)

        return sha256_hash.hexdigest()



    def verify_and_lock(self, file_path, expected_hash):

        current_hash = self.calculate_hash(file_path)

        return current_hash == expected_hash

"""



    target_path = r"C:\Genesis\SDK\Core\DataIntegrity.py"

    target_dir = os.path.dirname(target_path)



    try:

        # 2. 強制建立路徑

        if not os.path.exists(target_dir):

            os.makedirs(target_dir)

            print(f" -> 已建立目錄: {target_dir}")



        # 3. 實體寫入

        with open(target_path, "w", encoding="utf-8") as f:

            f.write(data_integrity_content)

        

        # 4. 閉迴路校驗

        file_hash = hashlib.sha256(data_integrity_content.encode('utf-8')).hexdigest()

        print(f" ✅ 實體寫入成功: {target_path}")

        print(f" 🛡️  驗證 Hash: {file_hash}")



    except Exception as e:

        print(f" ❌ 部署失敗: {str(e)}")



if __name__ == "__main__":

    auto_deploy()