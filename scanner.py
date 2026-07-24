import os
import ast
import json

def is_empty_logic(node):
    """檢查節點是否只有 pass 或為空"""
    if isinstance(node, (ast.Pass,)):
        return True
    if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant):
        return True # 檢查 docstring-only 或簡易賦值
    return False

def scan_files(root_dir):
    ghost_files = []
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        tree = ast.parse(f.read())
                    
                    # 邏輯抓鬼：如果整個檔案只有 pass 或是沒有定義函數/類別內容
                    is_ghost = True
                    for node in tree.body:
                        if not is_empty_logic(node):
                            is_ghost = False
                            break
                    
                    if is_ghost:
                        ghost_files.append(path)
                except Exception as e:
                    print(f"無法讀取: {path} - {e}")
    return ghost_files

# 執行掃描
scan_path = r"C:\Genesis"
results = scan_files(scan_path)

# 輸出結果
with open(os.path.join(scan_path, "ghost_report.json"), "w") as f:
    json.dump(results, f, indent=4)

print(f"掃描完成！共發現 {len(results)} 個空殼檔案。報告已產出至 C:\\Genesis\\ghost_report.json")