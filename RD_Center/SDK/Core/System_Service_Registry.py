# 檔案：C:\Genesis\Genesis_Core\System_Service_Registry.py

import subprocess

import os



class ServiceRegistry:

    def __init__(self):

        self.log_dir = r"C:\Genesis\logs"

        if not os.path.exists(self.log_dir): os.makedirs(self.log_dir)

        self.services = {"Hard_Obs": r"C:\Genesis\Genesis_Core\Security\Hardware_Observer.py"}



    def spawn_all_services(self):

        for name, path in self.services.items():

            log_file = os.path.join(self.log_dir, f"{name}_debug.txt")

            # 關鍵：開啟 stdout 與 stderr，將錯誤強制導出到檔案

            with open(log_file, "w") as f:

                proc = subprocess.Popen(['python', path], stdout=f, stderr=f)

                print(f"[Registry] 服務 {name} 已啟動 (PID: {proc.pid})，詳細日誌: {log_file}")



if __name__ == "__main__":

    ServiceRegistry().spawn_all_services()