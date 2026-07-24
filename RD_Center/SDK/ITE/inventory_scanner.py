import os

import hashlib



# 核心路徑鎖定

TARGET_DIR = r"C:\Genesis"

OUTPUT_FILE = r"C:\Genesis\system_inventory.txt"



def get_file_function(file_path):

    """讀取檔案前三行作為功能簡述"""

    try:

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:

            lines = [f.readline().strip() for _ in range(3)]

            return " | ".join([l for l in lines if l])

    except:

        return "無法讀取功能"



def scan_system():

    inventory = []

    for root, dirs, files in os.walk(TARGET_DIR):

        for file in files:

            if file.endswith(('.py', '.bat', '.sh')): # 針對程式碼檔案進行索引

                path = os.path.join(root, file)

                func = get_file_function(path)

                inventory.append(f"檔案: {file} | 路徑: {path} | 註解: {func}")

    

    # 寫入清單

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:

        f.write("\n".join(inventory))

    return OUTPUT_FILE



# 執行與 Hash 簽署

if __name__ == "__main__":

    if os.path.exists(TARGET_DIR):

        report_path = scan_system()

        print(f"掃描完成。清單已輸出至: {report_path}")

        

        # 產出該程式本身的 Hash 以供驗證

        with open(__file__, 'rb') as f:

            file_hash = hashlib.sha256(f.read()).hexdigest()

            print(f"本程式實體 Hash: {file_hash}")

    else:

        print("權限阻斷: 找不到 C:\Genesis 路徑")