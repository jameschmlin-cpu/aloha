# C:\Genesis\Management_Hub\Genesis_Sanitizer.py
import re
from pathlib import Path

def sanitize_file(file_path):
    """移除 BOM 並修復常見的 UnicodeEscape 轉義錯誤"""
    try:
        # 1. 讀取原始二進位數據
        with open(file_path, 'rb') as f:
            content = f.read()

        # 2. 移除 UTF-8 BOM (EF BB BF)
        if content.startswith(b'\xef\xbb\xbf'):
            content = content[3:]
        
        # 3. 轉回字串並修復路徑轉義 (將反斜線轉為原始字串兼容格式)
        text = content.decode('utf-8', errors='ignore')
        
        # 處理截斷的 \U 轉義錯誤 (將不完整的轉義序列轉為安全字元)
        text = re.sub(r'\\U([a-fA-F0-9]{1,7})(?![a-fA-F0-9])', r'\\\\U\1', text)

        # 4. 寫回乾淨檔案
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)
            
        return True
    except Exception as e:
        print(f"[失敗] 無法清理 {file_path}: {e}")
        return False

def run_sanitization():
    root = Path(r"C:\Genesis")
    print("[執行] 開始聖潔化程序...")
    
    # 針對報錯過的特定目錄進行優先修復
    target_dirs = [root / "RD_Center" / "SDK" / "ITE", root / "RD_Center" / "SDK" / "Core"]
    
    for folder in target_dirs:
        for py_file in folder.rglob("*.py"):
            if sanitize_file(py_file):
                print(f"[成功] 已聖潔化: {py_file.name}")

if __name__ == "__main__":
    run_sanitization()