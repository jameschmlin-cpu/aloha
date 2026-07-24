# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\Genesis_Core\Core\Registry_Manager.py
# 狀態：完整封裝，憲法鎖定 + 秘書模組自動化掛載

import json
import os
import sys
import importlib.util

class RegistryManager:
    def __init__(self):
        self.BASE_PATH = r"C:\Genesis"
        self.REGISTRY_FILE = os.path.join(self.BASE_PATH, "Genesis_Core", "Data", "Registry.json")
        self.MODULES_PATH = os.path.join(self.BASE_PATH, "Genesis_Core", "Modules")
        self.active_components = {}
        
        # 初始化核心架構
        self._initialize_sdk_architecture()

    def _initialize_sdk_architecture(self):
        """系統初始化：載入核心藍圖並自動啟動秘書模組"""
        self._enforce_keep_blueprint()
        
        # 自動掛載核心模組：秘書模組與監控器
        required_modules = ["Secretary_Module"]
        for mod in required_modules:
            self._load_module_from_library(mod)

    def _load_module_from_library(self, module_name):
        """從 Modules 目錄動態載入並掛載"""
        module_path = os.path.join(self.MODULES_PATH, f"{module_name}.py")
        if os.path.exists(module_path):
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            self.active_components[module_name] = mod
            sys.stdout.write(f"[系統] 模組 {module_name} 已實體掛載。 [OK]\n")
        else:
            sys.stderr.write(f"[!] 錯誤：無法找到模組 {module_name}，路徑: {module_path}\n")

    def _enforce_keep_blueprint(self):
        """更新憲法藍圖，確保狀態可追溯"""
        blueprint = {
            "version": "V3.2.2-Keep_Master_Final",
            "active_components": ["Secretary_Module"],
            "storage_mode": "LIBRARY_ON_DEMAND",
            "last_check": "2026-06-21T18:45:00"
        }
        os.makedirs(os.path.dirname(self.REGISTRY_FILE), exist_ok=True)
        with open(self.REGISTRY_FILE, 'w', encoding='utf-8') as f:
            json.dump(blueprint, f, indent=4)
        sys.stdout.write("[憲法] 憲法拓撲已同步更新。\n")

# 實體化掛載
if __name__ == "__main__":
    registry_manager = RegistryManager()
    print("--- RegistryManager 啟動完畢 ---")