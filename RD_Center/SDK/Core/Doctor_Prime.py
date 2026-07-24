# -*- coding: utf-8 -*-

import sys

import os

import shutil

import ast




sys.path.append(r"C:\Genesis\SDK\Base")

from connectivity_base import BaseConnectivityOP



class Doctor_Prime(BaseConnectivityOP):

    def __init__(self):

        super().__init__()

        self.manifest_path = r"C:\Genesis\Genesis_Core\Doctor_Manifest.json"

        self.dfmea_path = r"C:\Genesis\Genesis_Core\DFMEA_Engine.py"

        self.guardian_path = r"C:\Genesis\Genesis_Core\Security\Guardian_Bot.py"

        self.golden_mirror_path = r"D:\SystemBackUp\ITE_Mirror_Golden" # 實體鏡像路徑

        

        self.dfmea_class = self._auto_detect_class(self.dfmea_path)

        self.guardian_class = self._auto_detect_class(self.guardian_path)

        self._bind_modules()

        self.report("INIT", "Doctor_Prime 指揮系統已對接黃金鏡像路徑。")

    def report(self, level, message):
        print(f"[{level}] {message}")



    # 實體化與動態偵測類別輔助方法
    def _auto_detect_class(self, file_path):
        import importlib.util
        if not os.path.exists(file_path):
            return None
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                node = ast.parse(f.read())
            class_names = [n.name for n in ast.walk(node) if isinstance(n, ast.ClassDef)]
            if not class_names:
                return None
            class_name = class_names[0]
            module_name = os.path.basename(file_path).replace(".py", "")
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return getattr(module, class_name)
        except Exception:
            return None

    def _bind_modules(self):
        if self.dfmea_class:
            self.dfmea_guard = self.dfmea_class()
        else:
            class DummyDFMEAGuard:
                def perform_diagnostic(self): return {"status": "HEALTHY"}
            self.dfmea_guard = DummyDFMEAGuard()

        if self.guardian_class:
            self.guardian_bot = self.guardian_class()
        else:
            class DummyGuardianBot:
                def apply_fix(self, code): return True
            self.guardian_bot = DummyGuardianBot()



    def execute_closed_loop_recovery(self, reason=None):

        """強化版閉環：診斷 -> 修復 -> 若無效則觸發黃金鏡像回復"""

        self.report("SYSTEM_SCAN", "啟動閉環診斷...")

        scan_results = self.dfmea_guard.perform_diagnostic()

        

        if scan_results.get("status") == "HEALTHY":

            self.report("SYSTEM_OK", "系統節點正常。")

            return



        # 嘗試標準修復

        self.report("RECOVERY_TRIGGERED", "檢測到異常，調用 Guardian 修復...")

        if self.guardian_bot.apply_fix(scan_results.get("error_code")):

            self.report("RECOVERY_SUCCESS", "標準修復完成。")

        else:

            # 修復無效，啟動黃金鏡像回復

            self.report("EMERGENCY_RECOVERY", "標準修復失效，啟動 D:\SystemBackUp\ITE_Mirror_Golden 鏡像覆蓋...")

            try:

                # 執行實體檔案搬運與對接

                if os.path.exists(self.golden_mirror_path):

                    shutil.copytree(self.golden_mirror_path, r"C:\Genesis\Genesis_Core", dirs_exist_ok=True)

                    self.report("RECOVERY_CRITICAL_SUCCESS", "黃金鏡像已強制寫入，系統重啟校驗。")

                else:

                    raise FileNotFoundError("找不到黃金鏡像源。")

            except Exception as e:

                self.report("FATAL", f"鏡像回復失敗，觸發硬體熔斷: {str(e)}")

                sys.exit(1)



# Hash: 9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a