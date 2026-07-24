# -*- coding: utf-8 -*-

# 檔案：C:\Genesis\\Genesis_Core\DFMEA_Memory_Sync.py

# 狀態：物理路徑已修正至 C:\Genesis\Genesis_Core\Vault\DFMEA_Rules.db



import sqlite3

import os



def find_genesis_base():
    if "GENESIS_HOME" in os.environ:
        return os.environ["GENESIS_HOME"]
    current = os.path.abspath(__file__)
    while True:
        parent, name = os.path.split(current)
        if name.lower() == "genesis" or os.path.exists(os.path.join(current, "Genesis_Map.json")):
            return current
        if not name:
            break
        current = parent
    return r"C:\Genesis"

def sync_dfmea_rules():

    # 物理路徑修正

    genesis_base = find_genesis_base()

    db_dir = os.path.join(genesis_base, "Database")

    db_path = os.path.join(db_dir, "Genesis_DFMEA.db")

    

    # 確保資料夾存在

    if not os.path.exists(db_dir):

        os.makedirs(db_dir)

        

    # 增加 timeout=10.0 以處理併發鎖定，並使用 WAL 模式
    conn = sqlite3.connect(db_path, timeout=10.0)
    conn.execute("PRAGMA journal_mode=WAL;")

    cursor = conn.cursor()

    

    # 建立規則表結構

    cursor.execute('''CREATE TABLE IF NOT EXISTS Failure_Mode_Library 

                      (err_id TEXT PRIMARY KEY, mode TEXT, root_cause TEXT, prevention TEXT)''')

    

    # 本次寫入的防禦規則 (包含防止低級錯誤的記憶條目)

    rules = [

        ('ERR_001', 'LOGIC_OVERWRITE', '未讀取舊檔直接覆寫檔案內容，導致舊功能遺失', '寫入前必讀取舊檔，比對關鍵區塊 Function 定義，禁止覆蓋'),

        ('ERR_002', 'INHERITANCE_LOSS', '子類別繼承鏈中斷，未呼叫父類別 S3 熔斷機制', '強制驗證所有 Central_Dispatcher 繼承關係，缺 S3 則拒絕發送'),

        ('ERR_003', 'CALLBACK_MISSING', '閉環管理任務未回傳旗標給父單元', '任何任務執行邏輯，必須在 finally 區塊中掛載回傳旗標機制')

    ]

    

    for rule in rules:

        cursor.execute("INSERT OR REPLACE INTO Failure_Mode_Library VALUES (?,?,?,?)", rule)

    

    conn.commit()

    conn.close()

    print(f"[OK] [記憶落實] DFMEA 規則已成功存入: {db_path}")



if __name__ == '__main__':

    sync_dfmea_rules()