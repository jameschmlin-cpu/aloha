# C:\Genesis\Management_Hub\Dependency_Inspector.py
import ast
import json
from pathlib import Path

class DependencyVisitor(ast.NodeVisitor):
    def __init__(self):
        self.imports = set()
        self.bases = set()

    def visit_ImportFrom(self, node):
        # 紀錄 import 來源 (例如：from openharness.bridge import manager)
        if node.module:
            self.imports.add(node.module)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        # 紀錄繼承關係 (例如：class Core_Gateway(OpenHarness_Base))
        for base in node.bases:
            if isinstance(base, ast.Name):
                self.bases.add(base.id)
        self.generic_visit(node)

def inspect_dependencies(target_root):
    root = Path(target_root)
    audit_data = {}

    print(f"[檢測] 開始解析 {target_root} 的相依性...")
    
    for py_file in root.rglob("*.py"):
        try:
            with open(py_file, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read())
                visitor = DependencyVisitor()
                visitor.visit(tree)
                
                # 只記錄包含繼承或依賴的檔案，過濾乾淨檔案
                if visitor.imports or visitor.bases:
                    audit_data[str(py_file.relative_to(root))] = {
                        "bases": list(visitor.bases),
                        "imports": list(visitor.imports)
                    }
        except Exception as e:
            print(f"[Error] 無法解析 {py_file}: {e}")
            
    return audit_data

if __name__ == "__main__":
    # 設定檢測根目錄
    TARGET_DIR = r"C:\Genesis"
    report = inspect_dependencies(TARGET_DIR)
    
    output_path = r"C:\Genesis\Management_Hub\Dependency_Graph.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)
        
    print(f"[分析完成] 相依圖譜已產出: {output_path}")
    print("[提示] 請檢查 S1-S4 的繼承鏈是否在 'bases' 欄位中正確反映。")