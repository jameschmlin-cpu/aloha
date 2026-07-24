# -*- coding: utf-8 -*-

# 檔案：C:\Genesis\Genesis_Core\Library_Manager.py

# 功能：自動化掛載與管理師兄留下的分類結構



import os

import json



class LibraryManager:

    def __init__(self):

        self.lib_root = r"C:\Genesis\Library\LibrarySystem"

        self.index_file = r"C:\Genesis\Genesis_Core\Library_Index.json"



    def scan_and_index(self):

        """物理掃描分類結構，建立索引，實現系統接通"""

        catalog = {}

        for root, dirs, files in os.walk(self.lib_root):

            # 排除已封存資料夾

            if "Archive" in root: continue

            

            relative_path = os.path.relpath(root, self.lib_root)

            catalog[relative_path] = files

        

        with open(self.index_file, 'w', encoding='utf-8') as f:

            json.dump(catalog, f, indent=4, ensure_ascii=False)

        print(f"[LIBRARY] 索引建立完成：共掃描 {len(catalog)} 個分類節點。")



    def mount_category(self, category_name):

        """原子指令：掛載特定分類，實現快速存取"""

        # 僅載入您需要的分類，不載入全部

        pass



if __name__ == "__main__":

    mgr = LibraryManager()

    mgr.scan_and_index()