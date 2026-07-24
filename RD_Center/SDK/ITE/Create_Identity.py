import os

import datetime



# 這是真正會寫入檔案的物理邏輯

target_path = r"C:\Genesis\Empire_Identity.txt"

content = f"""=== 龍蝦帝國主權驗證 ===

建立時間: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

指揮官: 林雋懋

狀態: 實體檔案寫入成功，帝國權限已確權。

執行指令: 實體確權驗證

========================

"""



try:

    # 確保目錄存在

    if not os.path.exists(r"C:\Genesis"):

        os.makedirs(r"C:\Genesis")

    

    # 執行物理寫入

    with open(target_path, "w", encoding="utf-8") as f:

        f.write(content)

    print(f"✅ 檔案已建立於: {target_path}")

except Exception as e:

    print(f"❌ 寫入失敗，錯誤代碼: {e}")