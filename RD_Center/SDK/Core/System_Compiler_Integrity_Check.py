# -*- coding: utf-8 -*-

# 檔案：C:\Genesis\Genesis_Core\System_Compiler_Integrity_Check.py

import py_compile

import os




class CompilerIntegrityCheck:

    def __init__(self, target_dir):

        self.target_dir = target_dir

        self.passed_list = []

        self.failed_list = []



    def run_pre_flight_check(self):

        """物理預檢：僅測試語法合法性，不實際執行邏輯"""

        print(f"[*] 啟動物理預檢引擎，目錄: {self.target_dir}")

        for root, _, files in os.walk(self.target_dir):

            for file in files:

                if file.endswith(".py"):

                    path = os.path.join(root, file)

                    try:

                        # 僅測試編譯，不執行

                        py_compile.compile(path, doraise=True)

                        self.passed_list.append(file)

                    except Exception as e:

                        self.failed_list.append((file, str(e)))

        

        self.report_status()



    def report_status(self):

        print("\n--- 測試報告 ---")

        print(f"通過: {len(self.passed_list)}")

        if self.failed_list:

            print(f"🔴 失敗: {len(self.failed_list)}")

            for f, err in self.failed_list:

                print(f"  -> {f}: {err}")

        else:

            print("✅ 全部模組編譯語法通過，風險排除。")



if __name__ == "__main__":

    tester = CompilerIntegrityCheck(r"C:\Genesis\Genesis_Core")

    tester.run_pre_flight_check()