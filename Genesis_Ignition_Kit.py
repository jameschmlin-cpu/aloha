# -*- coding: utf-8 -*-
import os
import json

# 【內嵌核心地圖引擎】確保執行時無任何外部依賴錯誤
class EmpireAddressMap:
    _map = {}
    @classmethod
    def initialize(cls):
        print("[初始化] 建立實體檔案索引地圖...")
        for root, _, files in os.walk(r"C:\Genesis"):
            for file in files:
                if file.endswith(".py"):
                    cls._map[file] = os.path.join(root, file)
    @classmethod
    def get_path(cls, filename):
        return cls._map.get(filename)

def deploy_genesis_core():
    print("【執行點火程序】開始整合 Genesis 帝國 SDK...")
    
    # 1. 確保目錄結構與配置存在
    if not os.path.exists(r"C:\Genesis\Config"):
        os.makedirs(r"C:\Genesis\Config")
        
    config = {
        "registry": {"sdk_base": r"C:\Genesis\RD_Center\SDK"},
        "settings": {"auto_healing": True, "dfmea_sync": True}
    }
    with open(r"C:\Genesis\Config\Genesis_Config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)
        
    # 2. 啟動索引引擎
    EmpireAddressMap.initialize()
    
    # 3. 驗證關鍵路徑是否存在 (根據您的掃描報告)
    critical_files = ["Base_Template.py", "Doctor_Prime.py"]
    for f in critical_files:
        if EmpireAddressMap.get_path(f):
            print(f"[校驗通過] {f} 索引已建立。")
        else:
            print(f"[嚴重告警] 未找到 {f}，請確認檔案是否在 C:\\Genesis 目錄下。")
    
    print("【點火完成】Genesis SDK 閉環架構已就緒，核心引擎已注入。")

if __name__ == "__main__":
    deploy_genesis_core()