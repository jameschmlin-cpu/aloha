# -*- coding: utf-8 -*-
import os

# 1. 自動修正路徑索引 (不依賴任何外部檔案)
class SelfContainedIndexer:
    _map = {}
    @staticmethod
    def scan_and_register():
        print("[系統] 正在進行全域地圖掃描...")
        for root, _, files in os.walk(r"C:\Genesis"):
            for file in files:
                if file.endswith(".py"):
                    SelfContainedIndexer._map[file] = os.path.join(root, file)
        return SelfContainedIndexer._map

# 2. 自動處理執行順序
def main():
    print("[點火] 啟動帝國 SDK 整合程序...")
    try:
        registry = SelfContainedIndexer.scan_and_register()
        if "Base_Template.py" not in registry:
            print("[嚴重告警] 找不到核心 Base_Template.py，請確認檔案位置。")
            return
        
        print(f"[成功] 核心模組已對接，共索引 {len(registry)} 個檔案。")
        print("[下一步] 準備進行積木化掛載與 DFMEA 同步。")
        
    except Exception as e:
        print(f"[系統錯誤] 啟動失敗: {e}")

if __name__ == "__main__":
    main()