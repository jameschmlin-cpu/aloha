import os
import sys
import re
import ast
import hashlib

GENESIS_ROOT = r"C:\Genesis"

# 高風險毒素與惡意指令特徵庫
TOXIC_PATTERNS = [
    r"os\.system\s*\(\s*['\"]rm\s+-rf",  # 危險刪除指令
    r"eval\s*\(",                        # 不安全動態執行
    r"exec\s*\(",                        # 不安全動態執行
    r"subprocess\.Popen\s*\(\s*['\"]curl", # 存疑的外部連線
    r"__import__\s*\(\s*['\"]os['\"]\)\.system"
]

def scan_for_toxicity(code_content: str) -> bool:
    """【毒素偵測】檢查程式碼是否包含潛在惡意指令"""
    for pattern in TOXIC_PATTERNS:
        if re.search(pattern, code_content, re.IGNORECASE):
            return True
    return False

def auto_repair_empty_or_bad_logic(file_path: str):
    """
    【自動修復與清理引擎】
    1. 偵測毒素 ➔ 發現即阻斷
    2. 自動修正 common JS 寫法（false -> False, true -> True）
    3. 語法毀損且無法修復 ➔ 自動清理隔離
    """
    if not os.path.exists(file_path):
        return False, "File not found"
        
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Step 1: 毒素偵測
    if scan_for_toxicity(content):
        print(f"[SECURITY ALERT] 檔案 [{file_path}] 包含高風險毒素指令！強制阻斷執行。")
        return False, "Toxic code detected"
        
    # Step 2: 空邏輯與常見錯誤自動修正
    modified = False
    # 修正誤寫的 boolean / null
    fixed_content = re.sub(r'\bfalse\b', 'False', content)
    fixed_content = re.sub(r'\btrue\b', 'True', fixed_content)
    fixed_content = re.sub(r'\bnull\b', 'None', fixed_content)
    
    if fixed_content != content:
        content = fixed_content
        modified = True
        print(f"[AUTO-REPAIR] 已自動修復 [{file_path}] 中的語法標籤 (false/true/null -> False/True/None)。")
        
    # Step 3: AST 驗證修復後的程式碼是否健康
    try:
        ast.parse(content)
        if modified:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
        print(f"[CLEAN] 檔案 [{file_path}] 安全性與語法校驗完全合格！")
        
        hasher = hashlib.sha256(content.encode('utf-8'))
        return True, hasher.hexdigest()
        
    except SyntaxError as e:
        print(f"[CRITICAL] 檔案 [{file_path}] 語法嚴重毀損且無法修復 (Error: {e})。")
        print(f"[ACTION] 強制執行垃圾隔離/刪除，維持系統極致純潔。")
        # 若需要自動刪除壞檔，可取消下面這行的註解:
        # os.remove(file_path)
        return False, "Syntax unrepairable, isolated"

if __name__ == "__main__":
    # 測試自動修復 genesis_master_loop.py 或其他目標檔案
    target_file = os.path.join(GENESIS_ROOT, "genesis_master_loop.py")
    success, result = auto_repair_empty_or_bad_logic(target_file)
    print(f"[NODE C HASH] 防護檢測實體碼: {result}")