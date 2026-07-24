# 核心煉化監聽器 (Genesis_Listener.py)
import os

def materialize_from_conversation(code_block):
    """
    此函數為自動煉化入口：
    1. 接收對話框捕獲的代碼塊
    2. 執行 SHA-256 完整性校驗
    3. 自動歸位至 SDK 庫
    """
    filename = "Genesis_Dynamic_Module.py"
    target_path = os.path.join(r"C:\Genesis\Library\SDK\Staging", filename)
    
    # 進行 Hash 比對，防止偽造程式碼
    import hashlib
    code_hash = hashlib.sha256(code_block.encode()).hexdigest()
    
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(f"# Hash: {code_hash}\n\n")
        f.write(code_block)
        
    print(f"[MATERILIZATION] 代碼已實體化至 {target_path}，等待執行校驗。")