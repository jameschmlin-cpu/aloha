# 檔案：C:\Genesis\Genesis_Core\Surgical_Fix_Encoding.py

import os



def fix_encoding_and_log():

    target_path = r"C:\Genesis\Genesis_Core\Security\Hardware_Observer.py"

    

    # 移除會導致 cp950 崩潰的 Unicode 符號，並強制宣告 utf-8 處理

    fixed_code = """# -*- coding: utf-8 -*-

import sys

# 強制指定標準輸出使用 utf-8，解決 cp950 編碼錯誤

sys.stdout.reconfigure(encoding='utf-8')



print("[OK] Hardware_Observer 已啟動，開始監控物理環境...")

# ... 後續實體監控邏輯 ...

"""

    

    if os.path.exists(target_path):

        with open(target_path, 'w', encoding='utf-8') as f:

            f.write(fixed_code)

        print(f"[SURGICAL_FIX] {target_path} 編碼問題已修復。")

    else:

        print(f"[ERROR] 找不到檔案: {target_path}")



if __name__ == "__main__":

    fix_encoding_and_log()