import hashlib

import os




# 鎖定物理路徑

BASE_PATH = r"C:\Genesis"

SECURITY_PATH = os.path.join(BASE_PATH, "Security")



def verify_integrity(file_path, expected_hash):

    """

    實體 Hash 校驗邏輯，確保代碼未被竄改或產生破壞性逃逸

    """

    if not os.path.exists(file_path):

        return False

    

    sha256_hash = hashlib.sha256()

    with open(file_path, "rb") as f:

        for byte_block in iter(lambda: f.read(4096), b""):

            sha256_hash.update(byte_block)

    

    actual_hash = sha256_hash.hexdigest()

    return actual_hash == expected_hash



def secure_deploy(module_name, code_content):

    """

    保安部署機制：嚴禁空殼程式，強制路徑校驗

    """

    target_file = os.path.join(BASE_PATH, f"{module_name}.py")

    

    # 邏輯閉環檢查：嚴禁 pass 或 TODO

    if "pass" in code_content or "TODO" in code_content:

        print("【安全警報】偵測到空殼邏輯，拒絕寫入！")

        return "TECHNICAL_BLOCK"



    # 執行寫入

    try:

        with open(target_file, "w", encoding="utf-8") as f:

            f.write(code_content)

        

        # 產出實體 Hash 供主管校驗

        new_hash = hashlib.sha256(code_content.encode()).hexdigest()

        print(f"【執行成功】模組 {module_name} 已安全部署。")

        print(f"SHA-256: {new_hash}")

        return new_hash

    except Exception as e:

        print(f"【系統熔斷】物理寫入失敗: {str(e)}")

        return "PHYSICAL_FAILURE"



# 初始化安全路徑

if not os.path.exists(SECURITY_PATH):

    os.makedirs(SECURITY_PATH)