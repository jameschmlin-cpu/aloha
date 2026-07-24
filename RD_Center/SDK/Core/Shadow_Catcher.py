# -*- coding: utf-8 -*-

import psutil




def kill_interfering_processes():

    target_path = r"C:\Genesis\Genesis_Core\Gate\WebMCP_Genesis.py"

    print(f"正在偵測干擾進程，監控路徑: {target_path} ...")

    

    for proc in psutil.process_iter(['pid', 'name', 'open_files']):

        try:

            # 檢查是否有進程鎖定目標檔案

            for file in proc.open_files():

                if target_path in file.path:

                    print(f"🚨 發現影子進程！ PID: {proc.pid}, 名稱: {proc.name()}")

                    proc.kill()

                    print(f"✅ 已強制終止干擾 PID: {proc.pid}")

        except (psutil.NoSuchProcess, psutil.AccessDenied):

            continue



if __name__ == "__main__":

    kill_interfering_processes()