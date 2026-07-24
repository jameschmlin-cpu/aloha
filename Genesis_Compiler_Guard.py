import os
import hashlib
import ast
from genesis_gateway import GenesisGateway

def compile_and_lock(file_path):
    gateway = GenesisGateway()
    
    # 1. 檢查是否繼承 GenesisBase
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())
    
    is_inherited = any(isinstance(node, ast.ClassDef) and 
                       any(base.id == "GenesisBase" for base in node.bases) 
                       for node in tree.body)
    
    if not is_inherited:
        print(f"[FAIL] 嚴格拒絕: {os.path.basename(file_path)} 未繼承 GenesisBase")
        return False

    # 2. 自動編譯 (檢查語法)
    try:
        compile(open(file_path).read(), file_path, 'exec')
    except SyntaxError as e:
        print(f"[FAIL] 編譯失敗: {e}")
        return False

    # 3. 計算並寫入 Hash 到 DFMEA DB
    sha256 = hashlib.sha256(open(file_path, "rb").read()).hexdigest()
    gateway.log("dfmea_db", f"FILE: {file_path} | HASH: {sha256}")
    
    print(f"[PASS] 強制繼承已驗證，Hash 已註冊: {sha256[:16]}")
    return True

if __name__ == "__main__":
    # 使用範例：python Genesis_Compiler_Guard.py <目標檔案>
    import sys
    compile_and_lock(sys.argv[1])