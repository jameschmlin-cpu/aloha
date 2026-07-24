import sys


print("1. 開始載入路徑...")

sys.path.append(r"C:\Genesis\Genesis_Core")

try:

    print("2. 嘗試匯入 DFMEA_Engine...")

    from DFMEA_Engine import DFMEAEngine

    print("3. DFMEA_Engine 匯入成功。")

    print("4. 測試實例化...")

    engine = DFMEAEngine()

    print("5. 實例化完成。")

except Exception as e:

    print(f"!!! 發生嚴重錯誤: {e}")