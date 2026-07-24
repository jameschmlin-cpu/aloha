# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\Brick_Compiler_Engine.py
# 狀態：已重構為環境感知，支援自動對接與強固型分目錄分類編譯

import os
import re
import hashlib
import sys

def find_genesis_base():
    if "GENESIS_HOME" in os.environ:
        return os.environ["GENESIS_HOME"]
    current = os.path.abspath(__file__)
    while True:
        parent, name = os.path.split(current)
        if name.lower() == "genesis" or os.path.exists(os.path.join(current, "Genesis_Map.json")):
            return current
        if not name:
            break
        current = parent
    return r"C:\Genesis"

GENESIS_BASE = find_genesis_base()

class BrickCompiler:
    def __init__(self, target_base_dir=None):
        if target_base_dir is None:
            self.target_base_dir = os.path.join(GENESIS_BASE, "RD_Center", "SDK_Bricks")
        else:
            self.target_base_dir = target_base_dir
        os.makedirs(self.target_base_dir, exist_ok=True)

    def validate(self, code):
        """AI Agent 審核邏輯：禁止空殼與非實體路徑 (使用獨立單字匹配，防杜 false positives)"""
        if re.search(r'(?<!\w)pass(?!\w)', code) or re.search(r'(?<!\w)TODO(?!\w)', code):
            raise ValueError("嚴重違規：程式包含空殼代碼 (pass/TODO)")
        return True

    def parse_category(self, code):
        """從程式碼註解解析分類，預設為 Core"""
        match = re.search(r"#\s*Category:\s*(\w+)", code, re.IGNORECASE)
        if match:
            return match.group(1).capitalize()
        return "Core"

    def compile_to_brick(self, source_path):
        """將原始程式封裝為對應分類的積木"""
        try:
            with open(source_path, 'r', encoding='utf-8') as f:
                code = f.read()
        except UnicodeDecodeError:
            with open(source_path, 'r', encoding='gbk', errors='ignore') as f:
                code = f.read()
        
        if self.validate(code):
            category = self.parse_category(code)
            category_dir = os.path.join(self.target_base_dir, category)
            os.makedirs(category_dir, exist_ok=True)
            
            # 將檔名轉換為標準 CamelCase 類別名稱 (如 Core_Logic -> CoreLogicBrick)
            # 過濾檔名中的空白字元以符合類別命名規則
            clean_name = re.sub(r'\s+', '_', os.path.basename(source_path).replace('.py', ''))
            class_name = "".join(part.capitalize() for part in clean_name.split("_")) + "Brick"
            
            # 使用更穩健的分行縮排機制，防止縮排錯誤
            lines = code.splitlines()
            indented_lines = []
            for line in lines:
                if line.strip():
                    indented_lines.append("            " + line)
                else:
                    indented_lines.append("")
            indented_code = "\n".join(indented_lines)
            
            brick_content = f"""# -*- coding: utf-8 -*-
# Compiled Brick from: {os.path.basename(source_path)}
# Category: {category}

class {class_name}:
    def run(self, ctx=None):
        try:
{indented_code}
        except Exception as e:
            print(f"[{class_name}] 運行失敗: {{e}}")
            return False
        return True
"""
            # 寫入分目錄積木庫
            brick_path = os.path.join(category_dir, f"{clean_name}.py")
            with open(brick_path, 'w', encoding='utf-8') as f:
                f.write(brick_content)
            
            # 生成 Hash 進行實體驗證
            sha = hashlib.sha256(brick_content.encode()).hexdigest()
            print(f"[積木編譯完成] 分類: {category} | 類別: {class_name} -> {os.path.basename(brick_path)} | Hash: {sha[:8]}")

if __name__ == "__main__":
    # 對接與載入全局防禦日誌
    try:
        sys.path.append(os.path.join(GENESIS_BASE, "RD_Center"))
        from SDK.Core.console_defender import setup_global_defense
        setup_global_defense()
    except Exception:
        pass

    compiler = BrickCompiler()
    
    # 掃描來源 A：RD_Center\SDK
    src_dir = os.path.join(GENESIS_BASE, "RD_Center", "SDK")
    print(f"[*] 開始掃描 SDK 來源目錄: {src_dir}")
    if os.path.exists(src_dir):
        for f in os.listdir(src_dir):
            if f.endswith(".py") and f != "__init__.py" and not f.startswith("Core_Gateway"):
                try:
                    compiler.compile_to_brick(os.path.join(src_dir, f))
                except Exception as e:
                    print(f"[警告] 編譯 {f} 失敗: {e}")
                    
    # 掃描來源 B：Genesis 根目錄
    print(f"\n[*] 開始掃描 Genesis 根目錄: {GENESIS_BASE}")
    for f in os.listdir(GENESIS_BASE):
        # 排查非程式檔、已備份檔、本編譯器與 scanner 等工具
        if (f.endswith(".py") and 
            f not in ["Brick_Compiler_Engine.py", "scanner.py", "Verify_Empire_Closure.py", "Verify_Empire_Closure_v2.py"] and 
            not f.startswith("test_") and 
            not f.startswith("check_")):
            try:
                compiler.compile_to_brick(os.path.join(GENESIS_BASE, f))
            except Exception as e:
                print(f"[警告] 編譯根目錄 {f} 失敗: {e}")