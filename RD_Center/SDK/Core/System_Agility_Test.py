import os

import shutil

import subprocess



def test_agility():

    # 測試對象：模擬一個需要被SDK整合的模組

    source = r"C:\Genesis\Genesis_Core\Test_Module.py"

    target = r"C:\Genesis\Genesis_Core\Modules\Test_Module_Integrated.py"

    

    print("--- 物理手腳靈活度測試 ---")

    

    # 1. 測試建立檔案能力

    with open(source, "w") as f: f.write("print('Test')")

    

    # 2. 測試移動/封裝能力 (模擬 SDK 將模組移入正確路徑)

    try:

        if not os.path.exists(r"C:\Genesis\Genesis_Core\Modules"):

            os.makedirs(r"C:\Genesis\Genesis_Core\Modules")

        shutil.move(source, target)

        print(f"[OK] 物理搬運成功: {target}")

    except Exception as e:

        print(f"[FAIL] 搬運失敗: {e}")

        return



    # 3. 測試編譯/執行能力 (模擬 SDK 的觸發邏輯)

    try:

        result = subprocess.run(["python", target], capture_output=True, text=True)

        if result.returncode == 0:

            print("[OK] SDK 觸發編譯與執行成功")

        else:

            print(f"[FAIL] 執行失敗: {result.stderr}")

    except Exception as e:

        print(f"[FAIL] 系統呼叫失敗: {e}")



if __name__ == "__main__":

    test_agility()