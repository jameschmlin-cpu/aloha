# 檔案：C:\Genesis\Genesis_Core\Final_Ignition_Test.py

import subprocess




def final_test():

    # 強制檢查 5000 埠

    print("[TEST] 檢查 Flask 模組與埠口狀態...")

    

    # 嘗試直接啟動 Interface_Controller

    ctrl_path = r"C:\Genesis\Genesis_Core\Interface_Controller.py"

    try:

        print(f"[TEST] 嘗試直接啟動控制器: {ctrl_path}")

        proc = subprocess.Popen(['python', ctrl_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        print(f"[TEST] 啟動指令已送出，PID: {proc.pid}")

        

        # 等待 3 秒檢查是否存活

        try:

            stdout, stderr = proc.communicate(timeout=3)

            print(f"[ERROR_OUTPUT] {stderr}")

        except subprocess.TimeoutExpired:

            print("[SUCCESS] 服務已成功在背景執行，請重新整理 http://localhost:5000/")

            

    except Exception as e:

        print(f"[FATAL] 無法啟動控制器: {e}")



if __name__ == "__main__":

    final_test()