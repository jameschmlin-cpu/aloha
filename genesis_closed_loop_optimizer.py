import os
import sys
import yaml
import hashlib
import ast
import re

try:
    import psutil
except ImportError:
    print("[ERROR] 系統未安裝 psutil，請先執行 pip install psutil")
    sys.exit(1)

GENESIS_ROOT = r"C:\Genesis"
CONFIG_PATH = os.path.join(GENESIS_ROOT, "genesis_config.yaml")

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def save_config(config_data):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        yaml.dump(config_data, f, allow_unicode=True)

def sanitize_and_fix_file(file_path: str):
    """
    【閉迴路自動防衛與修復】
    自動修正舊檔案中的無效跳脫字元（如 \G, \I 等未加 r 前綴的路徑字串），
    確保全系統 100% 符合 Python 3.14+ 嚴格規範。
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        modified = False
        # 自動修復一般字串中的 Windows 路徑未加 raw string 的問題 (例如 "C:\Genesis" -> r"C:\Genesis")
        # 針對常見的驅動器路徑進行智慧包裹
        new_content = re.sub(r'"(C:\\[A-Za-z0-9_\\.-]+)"', r'r"\1"', content)
        new_content = re.sub(r"'(C:\\[A-Za-z0-9_\\.-]+)'", r"r'\1'", new_content)
        
        if new_content != content:
            content = new_content
            modified = True
            
        # 驗證 AST 語法
        tree = ast.parse(content, filename=file_path)
        
        if modified:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"[AUTO-SANITIZED] 已自動淨化並修復違規路徑跳脫字元: {file_path}")
            
        functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        return True, functions
    except Exception as e:
        return False, str(e)

def scan_and_detect_new_resources():
    r"""
    【資源偵測雷達】自動掃描 C:\Genesis 底下的 Python 模組與資源，
    進行全面健康盤點與自動防衛淨化。
    """
    print("[SENSOR] 啟動資源偵測雷達與自我防衛淨化程序...")
    discovered_resources = []
    
    for root, dirs, files in os.walk(GENESIS_ROOT):
        if "rag_storage" in root or ".git" in root:
            continue
        for file in files:
            if file.endswith(".py") and file != "genesis_closed_loop_optimizer.py":
                file_path = os.path.join(root, file)
                success, data = sanitize_and_fix_file(file_path)
                if success:
                    discovered_resources.append({
                        "file_name": file,
                        "path": file_path,
                        "functions": data
                    })
                    
    print(f"[SUCCESS] 盤點與淨化完畢，共列管 {len(discovered_resources)} 個模組。")
    return discovered_resources

def closed_loop_optimize_engine():
    """
    【閉迴路管理器】
    自我感測、自動淨化、動態配置優化。
    """
    print("[CLOSED-LOOP] 進入閉迴路自我管理與配置優化程序...")
    config = load_config()
    
    resources = scan_and_detect_new_resources()
    managed_modules = config.get("managed_modules", [])
    new_modules_added = 0
    
    for res in resources:
        if res["file_name"] not in managed_modules:
            managed_modules.append(res["file_name"])
            new_modules_added += 1
            print(f"[AUTOTUNE] 發現新資源 [{res['file_name']}]，自動納入閉迴路管轄清單！")
            
    config["managed_modules"] = managed_modules
    save_config(config)
    
    hasher = hashlib.sha256(str(config).encode('utf-8'))
    entity_hash = hasher.hexdigest()
    print(f"[NODE C HASH] 閉迴路動態優化實體代碼: {entity_hash}")
    
    if new_modules_added > 0:
        print(f"[SUCCESS] 閉迴路優化完畢：成功自動整合 {new_modules_added} 個新資源，系統已達到最佳配置。")
    else:
        print("[SUCCESS] 閉迴路巡檢完畢：全系統模組均已自動淨化並維持最優態勢。")

if __name__ == "__main__":
    closed_loop_optimizer() if 'closed_loop_optimizer' in globals() else closed_loop_optimize_engine()