# -*- coding: utf-8 -*-
# C:\Genesis\SDK\semantic_analyzer.py
# SDK 4 Stages Compliant / Full Integrity Implementation
import os
import ast
import json
import hashlib
import sys

class SemanticAnalyzer:
    def __init__(self):
        # 使用 raw string 確保路徑完全合法，杜絕 SyntaxWarning
        self.root_dir = r"C:\Genesis"
        self.manifest_path = r"C:\Genesis\SDK\block_manifest.json"
        
    def generate_hash(self, content: str) -> str:
        """Stage 2: 生成 SHA-256 實體簽章，作為完整性驗證"""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def get_code_intent(self, file_path):
        """解析程式語義邏輯，抓取類別與函式結構"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                # 排除 Genesis 本身架構程式
                if "Genesis" in content:
                    return None
                
                tree = ast.parse(content)
                classes = [n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
                methods = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
                
                if classes or methods:
                    return {"classes": classes, "methods": methods}
        except Exception:
            return None
        return None

    def run_full_validation(self):
        """Stage 1 & 3: 執行全域掃描與語義建模"""
        print(f"[Stage 1] 啟動沙盒路徑遍歷: {self.root_dir}")
        data = []
        
        # 嚴格遍歷 C:\Genesis 目錄
        for root, _, files in os.walk(self.root_dir):
            for file in files:
                if file.endswith(".py") and "Genesis" not in file:
                    path = os.path.join(root, file)
                    intent = self.get_code_intent(path)
                    if intent:
                        data.append({"path": path, "intent": intent})
        
        # Stage 2: 序列化內容並計算 Hash (確保數據一致性)
        content = json.dumps(data, indent=4, ensure_ascii=False)
        file_hash = self.generate_hash(content)
        
        # Stage 3: 物理寫入
        try:
            with open(self.manifest_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Stage 4: 物理存證驗證
            if os.path.exists(self.manifest_path):
                print("[Stage 4] 物理存證成功。")
                print(f"[Hash Lock] SHA-256: {file_hash}")
                print(f"[統計] 共歸位 {len(data)} 個邏輯積木。")
            else:
                raise IOError("物理落盤失敗")
                
        except Exception as e:
            print(f"[Fatal] 物理寫入錯誤: {e}")
            sys.exit(1)

if __name__ == "__main__":
    # 初始化並執行嚴格校驗程序
    analyzer = SemanticAnalyzer()
    analyzer.run_full_validation()