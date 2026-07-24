import os
import csv

# 設定路徑：針對 LibOption 進行盤點
TARGET_DIR = r"C:\Genesis\Library\LibOption"
REPORT_CSV = r"C:\Genesis\SDK_Inventory_Report.csv"

def classify_sdk(folder_name):
    """根據 SDK 功能進行分類歸納"""
    if "google" in folder_name.lower() or "cloud" in folder_name.lower():
        return "系統層_雲端積木 (Base_Cloud)"
    elif "crypto" in folder_name.lower() or "charset" in folder_name.lower():
        return "系統層_底層積木 (Base_Core)"
    elif "click" in folder_name.lower() or "colorama" in folder_name.lower():
        return "產品層_互動積木 (App_UI)"
    elif "LibrarySystem" in folder_name:
        return "帝國層_知識積木 (Core_Knowledge)"
    else:
        return "產品層_通用積木 (General_App)"

def scan_sdk_inventory():
    print(f"[系統啟動] 開始盤點路徑: {TARGET_DIR} ...")
    inventory = []
    
    if not os.path.exists(TARGET_DIR):
        return f"[系統中斷] 路徑 {TARGET_DIR} 不存在，請確認該目錄是否已掛載。"

    for item in os.listdir(TARGET_DIR):
        item_path = os.path.join(TARGET_DIR, item)
        if os.path.isdir(item_path):
            category = classify_sdk(item)
            # 檢查是否存在舊路徑殘留 (簡單的目錄結構檢查)
            path_status = "OK" if "Genesis" in item_path else "需重構路徑"
            
            inventory.append({
                "SDK_Name": item,
                "Category": category,
                "Path_Status": path_status,
                "Full_Path": item_path
            })
            print(f"[盤點] {item} -> 分類: {category}")

    # 輸出為 CSV 供您管理
    with open(REPORT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["SDK_Name", "Category", "Path_Status", "Full_Path"])
        writer.writeheader()
        writer.writerows(inventory)
        
    return (f"\n[執行成功] SDK 盤點已完成。\n"
            f"[報告位置] {REPORT_CSV}\n"
            f"[下一步驟] 請檢視 CSV 分類，確認分類無誤後，即可執行對接指令。")

if __name__ == "__main__":
    print(scan_sdk_inventory())