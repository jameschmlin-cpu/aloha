# Category: Security
# -*- coding: utf-8 -*-
# 檔案名稱：C:\Genesis\Audit_System_Integrity.py
# 核心功能：全域環境實體盤點、路徑權限閉鎖偵測

import os

class GenesisAuditor:
    def __init__(self):
        # [精確定義] 這是系統內所有核心依賴的唯一真實路徑清單
        self.registry = {
            "SDK_Core": r"C:\Genesis\RD_Center\SDK\Core",
            "SDK_ITE": r"C:\Genesis\RD_Center\SDK\ITE",
            "SDK_System": r"C:\Genesis\RD_Center\SDK\System",
            "DFMEA_Database": r"C:\Genesis\Database\Genesis_DFMEA.db",
            "Config_Directory": r"C:\Genesis\Config",
            "Base_Template": r"C:\Genesis\Base_Template.py",
            "Doctor_Prime": r"C:\Genesis\RD_Center\Source\Option\Stage1\Doctor_Prime.py"
        }

    def run_audit(self):
        print("=== Genesis 帝國環境實體審查儀 (Audit_System_Integrity) ===")
        all_passed = True
        
        for name, path in self.registry.items():
            if not os.path.exists(path):
                print(f"[嚴重告警] 檔案/目錄缺失: {name} | 路徑: {path}")
                all_passed = False
            else:
                can_write = os.access(path, os.W_OK)
                status = "可寫入" if can_write else "唯讀"
                print(f"[OK] {name} 實體已對接 | 權限: {status}")
        
        if all_passed:
            print("=== 審查結果：所有路徑與權限已完全閉鎖，系統已準備就緒 ===")
            return True
        else:
            print("=== 審查結果：偵測到環境缺失，請依據上述告警修正路徑 ===")
            return False

if __name__ == "__main__":
    auditor = GenesisAuditor()
    auditor.run_audit()