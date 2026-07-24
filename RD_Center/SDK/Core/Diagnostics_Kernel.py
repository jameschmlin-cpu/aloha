# 檔案：C:\Genesis\Genesis_Core\Diagnostics_Kernel.py

import subprocess

import os

import sys



def diagnose_and_boot():

    print("[DIAGNOSTIC] 開始診斷點火程序...")

    registry_path = r"C:\Genesis\Genesis_Core\System_Service_Registry.py"

    

    if not os.path.exists(registry_path):

        print(f"[ERROR] 找不到 Registry 檔案: {registry_path}")

        return



    # 強制使用系統絕對路徑執行

    try:

        print("[DIAGNOSTIC] 嘗試拉起服務...")

        # 將執行指令改為顯示詳細輸出

        process = subprocess.Popen([sys.executable, registry_path], 

                                   stdout=subprocess.PIPE, 

                                   stderr=subprocess.PIPE,

                                   text=True)

        

        # 獲取輸出，診斷是否成功

        stdout, stderr = process.communicate(timeout=5)

        

        if stdout: print(f"[SUCCESS_OUTPUT] {stdout}")

        if stderr: print(f"[CRITICAL_ERROR] {stderr}")

        print("[DIAGNOSTIC] 點火程序結束。")

        

    except Exception as e:

        print(f"[FATAL_EXCEPTION] 無法拉起服務: {e}")



if __name__ == "__main__":

    diagnose_and_boot()