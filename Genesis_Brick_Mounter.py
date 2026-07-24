# -*- coding: utf-8 -*-
# 執行此程式將所有舊程式歸位並註冊為積木
import os
from EmpireAddressMap import EmpireAddressMap

def mount_all_bricks():
    print("【積木歸位】開始將精華程式進行自動化註冊...")
    target_dirs = [r"C:\Genesis\RD_Center\SDK\Core", 
                   r"C:\Genesis\RD_Center\SDK\ITE", 
                   r"C:\Genesis\RD_Center\SDK\System"]
    
    for directory in target_dirs:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".py"):
                    # 註冊到地圖，確保 SDK 能隨時呼叫
                    EmpireAddressMap.add_path(file, os.path.join(root, file))
                    print(f"[已註冊積木] {file}")
    
    print("【積木歸位完成】300+ 個精華程式已納入 SDK 管理。")

if __name__ == "__main__":
    mount_all_bricks()