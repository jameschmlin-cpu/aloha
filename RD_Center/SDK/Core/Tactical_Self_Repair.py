# 檔案：C:\Genesis\Genesis_Core\Tactical_Self_Repair.py

import subprocess
import signal
import psutil
import time



def tactical_repair():

    print("[TACTICAL] 開始系統自動診斷與修補...")

    port = 5000

    

    # 1. 殺掉所有佔用 5000 埠的程序

    for proc in psutil.process_iter(['pid', 'name']):

        try:

            for conns in proc.connections(kind='inet'):

                if conns.laddr.port == port:

                    print(f"[FIX] 偵測到埠口佔用，終止程序 PID: {proc.pid}")

                    proc.send_signal(signal.SIGTERM)

        except: continue



    # 2. 啟動 Interface_Controller 並保持監控

    ctrl_path = r"C:\Genesis\Genesis_Core\Interface_Controller.py"

    print(f"[RUN] 強制拉起控制器: {ctrl_path}")

    proc = subprocess.Popen(['python', ctrl_path])

    

    # 3. 延遲驗證

    time.sleep(3)

    if proc.poll() is None:

        print(f"[SUCCESS] 系統已成功重啟並運行 (PID: {proc.pid})")

    else:

        print("[FAIL] 系統啟動失敗，請查看 C:\Genesis\logs\interface_error.log")



if __name__ == "__main__":

    tactical_repair()