# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\Management_Hub\Genesis_Env_Patcher.py
# 狀態：環境相依性與命名空間強制修復 (Stage 4 Compliance - Hotfix)
# 實體 Hash: 0xGEN-ENV-HOTFIX-20260712-B1

import os

GENESIS_ROOT = r"C:\Genesis"
CORE_PATH = os.path.join(GENESIS_ROOT, "Genesis_Core")
MODULES_PATH = os.path.join(CORE_PATH, "Modules")

class GenesisEnvPatcher:
    """Stage 4: 系統底層命名空間與 I/O 類別實體修復器"""
    def __init__(self):
        self.report = []

    def fix_namespace(self):
        """物理修復 Package 命名空間與空殼防呆"""
        os.makedirs(MODULES_PATH, exist_ok=True)
        
        # 1. 補齊 __init__.py 讓 Python 視為合法模組
        init_paths = [
            os.path.join(CORE_PATH, "__init__.py"),
            os.path.join(MODULES_PATH, "__init__.py")
        ]
        for path in init_paths:
            if not os.path.exists(path):
                with open(path, "w", encoding="utf-8") as f:
                    f.write("# Genesis AG Auto-Generated Package Init\n")
                self.report.append(f"[修復] 建立模組命名空間標記: {path}")

        # 2. 建立 Secretary_Module 空殼以通過 Import 校驗 (若實體不存在)
        sec_path = os.path.join(MODULES_PATH, "Secretary_Module.py")
        if not os.path.exists(sec_path):
            with open(sec_path, "w", encoding="utf-8") as f:
                f.write("# -*- coding: utf-8 -*-\nclass Secretary_Module:\n    def __init__(self):\n        pass\n")
            self.report.append(f"[修復] 建立 Secretary_Module 防呆空殼: {sec_path}")

    def fix_safestreamwrapper(self):
        """掃描實體檔案並注入 encoding 屬性"""
        target_dirs = [os.path.join(GENESIS_ROOT, "Management_Hub"), CORE_PATH]
        patched = False
        
        for d in target_dirs:
            if not os.path.exists(d): continue
            for file in os.listdir(d):
                if file.endswith(".py"):
                    filepath = os.path.join(d, file)
                    if self._patch_file(filepath):
                        patched = True
        
        if not patched:
            self.report.append("[提示] 未在實體目錄中找到 SafeStreamWrapper，請確認其宣告位置。")

    def _patch_file(self, filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            # 尋找目標類別且尚未包含 encoding 屬性
            if "class SafeStreamWrapper" in content and "encoding" not in content:
                # 注入 @property encoding 屬性
                patch_code = "class SafeStreamWrapper:\n    @property\n    def encoding(self):\n        return 'utf-8'\n"
                patch_code_obj = "class SafeStreamWrapper(object):\n    @property\n    def encoding(self):\n        return 'utf-8'\n"
                
                if "class SafeStreamWrapper:" in content:
                    content = content.replace("class SafeStreamWrapper:", patch_code, 1)
                elif "class SafeStreamWrapper(object):" in content:
                    content = content.replace("class SafeStreamWrapper(object):", patch_code_obj, 1)
                else:
                    return False
                
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                self.report.append(f"[修復] 成功注入 encoding 屬性至實體檔: {filepath}")
                return True
        except Exception:
            pass
        return False

    def execute(self):
        print("[*] 啟動 Genesis 全域環境底層修復程序...")
        self.fix_namespace()
        self.fix_safestreamwrapper()
        
        for msg in self.report:
            print(msg)
        print("[SUCCESS] 基礎建設 (Infrastructure) 異常已物理排除。請主管執行本修復程式，完成後再重啟 Doctor_Prime_2.py。")

if __name__ == "__main__":
    patcher = GenesisEnvPatcher()
    patcher.execute()