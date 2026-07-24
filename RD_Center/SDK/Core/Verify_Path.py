# 檔案：C:\Genesis\Genesis_Core\Verify_Path.py

import sqlite3

import os



def get_path(key):

    # 連接剛剛建立的權威資料庫

    conn = sqlite3.connect(r"C:\Genesis\Config\System_Paths.db")

    cursor = conn.cursor()

    cursor.execute("SELECT path FROM paths WHERE key=?", (key,))

    result = cursor.fetchone()

    conn.close()

    return result[0] if result else None



# 驗證邏輯

if __name__ == "__main__":

    gate_path = get_path("GATE_DIR")

    print(f"從資料庫讀取的 GATE 路徑為: {gate_path}")

    

    if gate_path and os.path.exists(gate_path):

        print("🟢 物理路徑驗證成功，路徑存在。")

    else:

        print("🔴 物理路徑驗證失敗，請檢查資料庫內容。")