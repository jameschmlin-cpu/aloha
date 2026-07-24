# -*- coding: utf-8 -*-

# 檔案：C:\Genesis\Path_Fixer.py

# 狀態：最終自動化對齊程式 (直接執行即可)



import os

import re



def fix_all_paths():

    # 修正清單：從錯誤路徑對齊至系統權威路徑

    fix_map = {

        r"D:\\SystemBackUp\\.*?": r"C:\\ITE\\Genesis_Core\\Data",

        r"C:\\ITE\\Genesis_Core\\logs": r"C:\\ITE\\Genesis_Core\\logs",

        r"C:\\ITE\\Database\\EMPIRE_CORE.db": r"C:\\ITE\\Genesis_Core\\Data\\Unified_Empire_Memory.db"

    }

    

    target_dir = r"C:\Genesis\Genesis_Core"

    print("[*] 開始物理路徑強制對齊...")

    

    for root, _, files in os.walk(target_dir):

        for file in files:

            if file.endswith(".py"):

                path = os.path.join(root, file)

                with open(path, 'r', encoding='utf-8', errors='ignore') as f:

                    content = f.read()

                

                new_content = content

                for old_p, new_p in fix_map.items():

                    new_content = re.sub(old_p, new_p, new_content)

                

                if new_content != content:

                    with open(path, 'w', encoding='utf-8') as f:

                        f.write(new_content)

                    print(f"[✅] 已修正: {file}")



if __name__ == "__main__":

    fix_all_paths()

    print("[*] 所有路徑已自動歸一至權威資料庫，請重啟系統。")