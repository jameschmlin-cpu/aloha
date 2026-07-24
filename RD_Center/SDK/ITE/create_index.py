import json

import os




# 黑盒子索引路徑

base_dir = r"C:\Genesis"

index_file = r"C:\Genesis\BlackBox\index.json"



# 確保目錄存在

if not os.path.exists(r"C:\Genesis\BlackBox"):

    os.makedirs(r"C:\Genesis\BlackBox")



# 過去兩天開發成果之邏輯清單 (模擬索引)

# 這裡對應我們在 C:\Genesis 下建立的實體檔案映射

code_index = {

    "version": "1.0",

    "last_updated": "2026-06-21T17:50:00",

    "files": {

        "memory_snapshot": {"path": r"C:\Genesis\snapshot.bin", "tag": "Core_Persistence"},

        "save_script": {"path": r"C:\Genesis\save_snapshot.py", "tag": "Utils"},

        "restore_script": {"path": r"C:\Genesis\restore_snapshot.py", "tag": "Utils"}

    }

}



# 產出索引

with open(index_file, "w") as f:

    json.dump(code_index, f, indent=4)



print("--- 索引建立完成 ---")

print(f"黑盒子索引路徑: {index_file}")

print(f"清單項目數: {len(code_index['files'])}")

print("系統已準備就緒，隨時可進行交班。")