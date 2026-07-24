# -*- coding: utf-8 -*-

# 檔案：C:\Genesis\Genesis_Core\Path_Validator_Engine.py

# 狀態：最終乾淨版 - 移除所有可能導致轉義警示的字元



import os

import sys



class PathValidator:

    def __init__(self):

        # 使用原始字串格式，確保反斜線不被轉義

        self.locked_root = r"C:\Genesis"



    def get_locked_root(self):

        return self.locked_root

    def check_path(self, path):

        return os.path.exists(path)



    def verify_integrity(self):

        """

        物理驗證：檢查 C 槽下的 ITE 核心路徑是否存在

        """

        required_paths = [

            self.locked_root,

            os.path.join(self.locked_root, r"Genesis_Core"),

            os.path.join(self.locked_root, r"Genesis_Core", r"Data"),

            os.path.join(self.locked_root, r"Genesis_Core", r"logs")

        ]

        

        for path in required_paths:

            if not os.path.exists(path):

                sys.stderr.write(f"!!! [PATH_VALIDATOR] 偵測到路徑缺失: {path}\n")

                return False

        return True



if __name__ == "__main__":

    validator = PathValidator()

    if validator.verify_integrity():

        sys.stdout.write(">>> [PATH_VALIDATOR] 路徑結構完整，狀態正常。\n")

    else:

        sys.exit(1)