import hashlib

def check_node_integrity(file_path, content):
    # 1. 路徑校驗 (Node A)
    if not file_path.startswith(r"C:\Genesis"):
        return False, "路徑非法，非核心 Genesis 路徑"
    
    # 2. 生成 Hash (Node B)
    file_hash = hashlib.sha256(content.encode()).hexdigest()
    
    # 3. 沙盒模擬測試 (Node C)
    # 此處可加入您的測試邏輯
    is_sandboxed = True 
    
    # 4. 最終校驗 (Node D)
    if is_sandboxed:
        return True, file_hash
    return False, "沙盒測試失敗"

# 使用方式：在執行寫入前，呼叫此函數進行比對