# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\Management_Hub\Gemini_Command_Center_3.py
# 狀態：終極強固版 (已移除權限競爭機制，導入絕對路徑錨定)

import sys
import os
import time

# 鎖定絕對路徑，確保繼承鏈可見性
BASE_DIR = r"C:\Genesis"
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# 確保子目錄亦在搜尋路徑內，防止 ModuleNotFoundError
MANAGEMENT_HUB = os.path.join(BASE_DIR, "Management_Hub")
if MANAGEMENT_HUB not in sys.path:
    sys.path.insert(0, MANAGEMENT_HUB)

from Genesis_Core.Base_Temple import Base_Temple
from Genesis_Core.Core_Gateway import Core_Gateway

class Gemini_Command_Center_3(Base_Temple, Core_Gateway):
    def __init__(self):
        # 物理強制初始化，確保繼承鏈正常觸發且不觸發權限競爭
        try:
            Base_Temple.__init__(self)
            Core_Gateway.__init__(self)
            print("[狀態] 實體引擎初始化完成。")
        except Exception as e:
            print(f"[致命權限錯誤] 初始化失敗: {e}")
            sys.exit(1)

    def run(self):
        # [物理修正] 改採「常駐模式」而非單次任務模式
        # 防止 startup_manager 因進程結束而誤判為紅點並發動重啟
        print("[狀態] 進入常駐守護迴圈...")
        while True:
            time.sleep(60)

if __name__ == "__main__":
    try:
        # 實例化並建立常駐進程
        cc = Gemini_Command_Center_3()
        cc.run()
    except KeyboardInterrupt:
        print("[狀態] 服務已接收終止訊號。")
        sys.exit(0)
    except Exception as e:
        print(f"[致命錯誤] 運行中斷: {e}")
        sys.exit(1)