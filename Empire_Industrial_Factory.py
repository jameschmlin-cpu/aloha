import os
import hashlib

# 核心路徑鎖定 (嚴格遵守 C:\Genesis)
# 確保所有建設節點與生產資料夾均在此路徑下運作
ROOT = r"C:\Genesis"
SDK_SRC = os.path.join(ROOT, "Library", "SDK")
BRICK_LIB = os.path.join(ROOT, "Library", "SDK_Bricks")
LOG_PATH = os.path.join(ROOT, "Logs", "factory_log.log")

def build_factory():
    # 物理路徑完整性驗證
    if not os.path.exists(SDK_SRC):
        print(f"[ERROR] 研發邏輯來源路徑不存在: {SDK_SRC}")
        return

    os.makedirs(BRICK_LIB, exist_ok=True)
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    
    for file in os.listdir(SDK_SRC):
        if not file.endswith(".py"): continue
        
        src = os.path.join(SDK_SRC, file)
        with open(src, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Agent 研發審核 (嚴格攔截空殼代碼)
        if "pass" in code or "TODO" in code:
            with open(LOG_PATH, 'a') as l:
                l.write(f"[研發拒絕] {file} 含有非法空殼邏輯\n")
            continue
            
        class_name = file.replace('.py', '_Brick').capitalize()
        brick_code = f"""
class {class_name}:
    def run(self):
        {code.replace(chr(10), chr(10) + '        ')}
"""
        # 實體寫入 C:\Genesis\Library\SDK_Bricks
        brick_path = os.path.join(BRICK_LIB, file)
        with open(brick_path, 'w', encoding='utf-8') as f:
            f.write(brick_code)
            
        brick_hash = hashlib.sha256(brick_code.encode()).hexdigest()
        with open(LOG_PATH, 'a') as l:
            l.write(f"[積木生產] {file} | Hash: {brick_hash[:16]}\n")
            
    print(f"[SYSTEM] 帝國工業生產線運行完畢，路徑鎖定於 {ROOT}")

if __name__ == "__main__":
    build_factory()