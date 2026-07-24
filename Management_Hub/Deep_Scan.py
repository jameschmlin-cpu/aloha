import os
import ast

# 物理路徑鎖定：C:\Genesis
ROOT = r"C:\Genesis"
REPORT_PATH = os.path.join(ROOT, "Management_Hub", "Scan_Report.log")

def analyze_logic(file_path):
    """讀取檔案內容並解析邏輯與功能"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
        
        # 提取模組功能：函數名稱與類別名稱
        functions = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
        classes = [n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
        
        return f"Funcs: {', '.join(functions)} | Classes: {', '.join(classes)}"
    except Exception as e:
        return f"邏輯解析失敗: {str(e)}"

def deep_scan():
    """遍歷路徑並執行邏輯解析"""
    if not os.path.exists(ROOT):
        print(f"[FATAL] 物理路徑不存在: {ROOT}")
        return

    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write(f"--- 深度邏輯掃描報告: {ROOT} ---\n")
        
        for root, dirs, files in os.walk(ROOT):
            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    logic_summary = analyze_logic(full_path)
                    
                    report_line = f"路徑: {full_path}\n功能: {logic_summary}\n"
                    f.write(report_line + "-"*20 + "\n")
                    print(f"[掃描完成] {file}")

if __name__ == "__main__":
    deep_scan()
    print(f"[SUCCESS] 掃描報告已產出: {REPORT_PATH}")