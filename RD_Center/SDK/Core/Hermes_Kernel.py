# -*- coding: utf-8 -*-

# 檔案：C:\Genesis\Genesis_Core\Hermes_Kernel.py



import os

import time

import datetime

import importlib


import Auto_File_Manager




class Hermes_Kernel:

    def __init__(self, command_center):

        self.base_path = r"C:\Genesis\Genesis_Core"

        self.log_path = os.path.join(self.base_path, "logs", "kernel_status.log")

        self.command_center = command_center # 注入指揮中心實例

        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)

        print(f"[*] Hermes_Kernel 整合就緒，路徑: {self.base_path}")



    def log_event(self, message):

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(self.log_path, "a", encoding="utf-8") as f:

            f.write(f"[{timestamp}] {message}\n")



    def schedule_task(self):

        """執行歸檔，包含維護模式握手與鏡像回復閉環"""

        print("[*] 進入閉環排程監控循環...")

        while True:

            now = datetime.datetime.now()

            if now.hour == 15 and now.minute == 0:

                try:

                    # 1. 進入維護模式：向指揮中心申請豁免

                    self.log_event("申請系統維護豁免...")

                    # 假設指揮中心有 set_maintenance_mode 方法

                    self.command_center.set_maintenance_mode(True)

                    

                    # 2. 執行歸檔

                    importlib.reload(Auto_File_Manager)

                    Auto_File_Manager.execute_daily_archive()

                    self.log_event("自動歸檔任務執行成功")

                    

                except Exception as e:

                    # 3. 故障閉環：直接觸發鏡像回復 (不依賴主管)

                    error_msg = f"任務執行失敗: {str(e)}"

                    self.log_event(error_msg)

                    print(f"[!] {error_msg}，啟動自主鏡像回復...")

                    self.command_center.trigger_mirror_recovery()

                finally:

                    # 4. 恢復監控模式

                    self.command_center.set_maintenance_mode(False)

                    time.sleep(61)

            else:

                time.sleep(60)



if __name__ == "__main__":

    # 初始化順序：Dispatcher -> SDK -> Empire_Command_Center -> Hermes_Kernel

    kernel = Hermes_Kernel(command_center=None) # 實際部署時請注入實例

    kernel.schedule_task()