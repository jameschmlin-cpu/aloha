# C:\Genesis\Fix_Path_Link.py
import os
import sys

# 強制將所有路徑歸位
BASE_GENESIS = r"C:\Genesis"
# 確保 sys.path 只有一個根目錄，杜絕搜尋衝突
sys.path = [BASE_GENESIS]

print("--- [路徑重整程序] ---")
print(f"當前工作路徑: {os.getcwd()}")
print(f"強制鎖定根目錄: {BASE_GENESIS}")

# 檢查關鍵檔案是否存在於您指定的物理位置
base_template_path = os.path.join(BASE_GENESIS, "Base_Template.py")
print(f"Base_Template 實體路徑確認: {base_template_path}")
print(f"檔案是否存在: {os.path.exists(base_template_path)}")

# 若檔案存在，此處進行模擬載入測試
if os.path.exists(base_template_path):
    print("狀態: [OK] 物理路徑對接成功。")
else:
    print("狀態: [FATAL] 實體路徑仍無法匹配。")