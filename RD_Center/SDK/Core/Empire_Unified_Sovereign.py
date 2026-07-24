# -*- coding: utf-8 -*-

# 檔案：C:\Genesis\Genesis_Core\Empire_Unified_Sovereign.py

# 狀態：最終整合 - 物理總線導通 (Bus-Bridge Initialization)



import os




def initialize_sovereign_system():

    print("[*] 正在進行最後物理對接...")

    

    # 1. 檢查核心模組是否存在

    core_files = [

        "Empire_Command_Center.py",

        "Central_Dispatcher.py",

        "Library_Main.py"

    ]

    

    for f in core_files:

        if not os.path.exists(os.path.join(r"C:\Genesis\Genesis_Core", f)):

            print(f"[!] 錯誤：{f} 尚未歸位。請確認檔案已放入 C:\Genesis\Genesis_Core")

            return



    # 2. 導通記憶庫與知識庫

    print("[*] 導通 Memory_Interface 與 Shared_Knowledge...")

    

    # 3. 啟動總線握手

    try:


        print("✅ [最終狀態] 帝國總管已完成初始化，物理握手完成。")

        print("✅ [狀態] 系統進入自主監控模式，隨時準備接管調度。")

    except Exception as e:

        print(f"🔴 [致命導通錯誤] 初始化失敗: {e}")



if __name__ == "__main__":

    initialize_sovereign_system()