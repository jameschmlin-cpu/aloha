# -*- coding: utf-8 -*-

# 檔案：C:\Genesis\Genesis_Core\Kernel_Orchestrator.py

# 狀態：語法修正版 (已修復 self.services 定義符號)



import subprocess

import time

import logging

import os

import sys



# 物理路徑強制對接

sys.path.insert(0, r"C:\Genesis\Genesis_Core")



from Security.Guardian_Bot import GuardianEngine as GuardianBot



class Orchestrator:

    def __init__(self):

        # 【修正】：移除多餘的 ] 符號

        self.services = {

            "Ollama": ["ollama", "serve"],

            

        }

        self.processes = {}

        self.heartbeat_file = r"C:\Genesis\logs\secretary.heartbeat"

        self.log_dir = r'C:\Genesis\logs'

        

        self.guardian = GuardianBot()

        self._initialize_environment()



    def _initialize_environment(self):

        if not os.path.exists(self.log_dir): os.makedirs(self.log_dir)

        logging.basicConfig(filename=os.path.join(self.log_dir, 'kernel_orch.log'), 

                            level=logging.INFO, 

                            format='%(asctime)s - %(levelname)s - %(message)s')



    def launch_services(self):

        print("[*] 啟動防禦節點: Guardian_Bot (Engine) | 掛載狀態: [OK]")

        for name, cmd in self.services.items():

            debug_path = os.path.join(self.log_dir, f"{name}_debug.log")

            log_file = open(debug_path, "w") if name != "Ollama" else subprocess.DEVNULL

            

            print(f"[*] 啟動服務: {name}")

            self.processes[name] = subprocess.Popen(cmd, stdout=log_file, stderr=subprocess.STDOUT)

            time.sleep(3)

            logging.info(f"服務已啟動: {name}")



    def monitor_loop(self):

        print("[*] 系統核心已啟動，監控中。")

        while True:

            for name, proc in self.processes.items():

                if proc.poll() is not None:

                    logging.warning(f"!!! [{name}] 偵測到掛起，執行重啟...")

                    self.processes[name] = subprocess.Popen(self.services[name], 

                                                          stdout=open(os.path.join(self.log_dir, f"{name}_debug.log"), "w"), 

                                                          stderr=subprocess.STDOUT)

            

            # 防禦節點掃描

            try:

                self.guardian.scan_and_remediate()

            except Exception as e:

                logging.error(f"物理防禦節點異常: {e}")

            

            time.sleep(10)



if __name__ == "__main__":

    orch = Orchestrator()

    orch.launch_services()

    orch.monitor_loop()