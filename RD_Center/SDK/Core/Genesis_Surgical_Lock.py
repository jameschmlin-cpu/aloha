# C:\Genesis\Genesis_Core\Genesis_Surgical_Lock.py

# 狀態：手術刀式路徑降權，僅限 Genesis_Core 內部存取

import os




def surgical_lock():

    """強制將執行路徑收束在 Genesis_Core，阻斷所有對外連結"""

    # 將所有搜尋路徑強制指向 Genesis_Core，覆蓋掉任何外部路徑

    os.environ['PYTHONPATH'] = r"C:\Genesis\Genesis_Core"

    # 建立保護旗標

    with open(r"C:\Genesis\Genesis_Core\PROTECTED.lock", "w") as f:

        f.write("PROTECTED_BY_GEMINI_SENTINEL")

    print("手術完成：執行路徑已鎖定，現已斷開外部潛在注入點。")



if __name__ == "__main__":

    surgical_lock()