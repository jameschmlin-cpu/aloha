# -*- coding: utf-8 -*-

import os


import ctypes



# 1. 物理路徑綁定

core_path = r'C:\Genesis\SDK\Core'

module_path = os.path.join(core_path, 'lobster_core.pyd')



print(f"[*] 正在對接物理路徑: {module_path}")



# 2. 強制綁定 DLL 搜尋目錄 (解決相依性搜尋失敗問題)

if hasattr(os, 'add_dll_directory'):

    os.add_dll_directory(core_path)

    print("[*] DLL 目錄已掛載")



# 3. 嘗試掛載並進行物理檢查

try:

    # 嘗試載入模組

    lib = ctypes.CDLL(module_path)

    print("✅ [物理掛載成功] 鏈路已建立，該模組可被當前 Python 環境驅動。")

except OSError as e:

    # 如果這裡失敗，會直接拋出 Windows 底層錯誤代碼 (WinError)

    print("❌ [物理掛載失敗]")

    print(f"錯誤代碼詳細報告: {e}")

    # 檢查是否為位元架構不符或相依性 DLL 缺失

except Exception as e:

    print(f"❌ [未預期異常]: {str(e)}")