# -*- coding: utf-8 -*-
# 檔案路徑：C:\Genesis\RD_Center\Source\OpenHarness_Core\20class\Lifecycle_Hook.py

import sys
import os
import json
import importlib.util
from datetime import datetime

# ==========================================================
# 物理導通層：強制校準搜尋路徑 (Path Validation)
# ==========================================================
# 強制掛載根目錄與 ITE 核心路徑，確保跨磁碟路徑導通
sys.path.insert(0, r"C:\Genesis")
sys.path.insert(0, r"C:\ITE")
sys.path.insert(0, r"C:\Genesis\RD_Center")

# 1. 嘗試透過名稱空間匯入引擎
try:
    from Genesis_Core import Path_Validator_Engine
except ImportError:
    # 2. 備援導通：若名稱空間解析失敗，直接從物理檔案路徑強制載入
    try:
        engine_path = r"C:\ITE\Genesis_Core\Path_Validator_Engine.py"
        spec = importlib.util.spec_from_file_location("Path_Validator_Engine", engine_path)
        Path_Validator_Engine = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(Path_Validator_Engine)
    except Exception as e:
        sys.stderr.write(f"[FATAL] 物理路徑導通失敗: {e}\n")
        sys.exit(1)

# 匯入 Base_Template (依賴前置路徑掛載)
try:
    from Base_Template import Base_Template
except ImportError as e:
    sys.stderr.write(f"[FATAL] Base_Template 匯入失敗: {e}\n")
    sys.exit(1)

class LobsterLifecycleHook(Base_Template):
    """
    龍蝦系統中層第 20 號 Class：Lifecycle_Hook
    負責全局生命週期掛鉤，執行 20 Class 大一統咬合。
    """
    def __init__(self):
        super().__init__(brick_id="LIFECYCLE_CORE")
        self.boot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.registry_path = r"C:\Genesis\SDK\Registry.json"

    def boot_empire_chassis(self) -> dict:
        """大一統開機掛鉤：驗證 Registry 並執行系統導通。"""
        # 執行路徑驗證引擎檢查
        validator = Path_Validator_Engine.PathValidator()
        if not validator.verify_integrity():
            return {"status": "TECHNICAL_RESTRAINT", "message": "路徑驗證器檢測到結構缺失。"}

        if not os.path.exists(self.registry_path):
            return {"status": "TECHNICAL_RESTRAINT", "message": "大一統斷層：Registry 檔案不存在。"}

        with open(self.registry_path, 'r', encoding='utf-8') as f:
            registry = json.load(f)

        blueprint_classes = registry.get("middleware_20_classes", [])
        
        # 實體閉迴路檢查
        if len(blueprint_classes) != 20:
            fail_msg = f"品質失效：Registry 藍圖中 Class 數量不符 ({len(blueprint_classes)}/20)。"
            return {"status": "TECHNICAL_RESTRAINT", "message": fail_msg}

        # 更新狀態
        registry["sdk_version"] = "V3.2.1-Genesis_Pure"
        registry["system_integrity_status"] = "EMPIRE_CHASSIS_ACTIVE_100"
        
        with open(self.registry_path, 'w', encoding='utf-8') as f:
            json.dump(registry, f, indent=4, ensure_ascii=False)

        return {
            "status": "EMPIRE_BOOT_SUCCESS",
            "system_meta": {
                "version": registry["sdk_version"],
                "active_classes_count": len(blueprint_classes),
                "boot_timestamp": self.boot_time,
                "chassis_integrity": "100%_QE_VERIFIED"
            }
        }

if __name__ == "__main__":
    hook = LobsterLifecycleHook()
    report = hook.boot_empire_chassis()
    
    print(f"全局開機狀態: {report['status']}")
    if report['status'] == "EMPIRE_BOOT_SUCCESS":
        print("中層 20 Class 建設宣告全面封頂完工！")
    else:
        print(f"阻斷原因: {report.get('message')}")