# C:\Genesis\MCP_OneStop_Test.py
import hashlib

def run_one_stop_test():
    # 1. 檢測 MCP 執行狀態 (Channel check)
    target_file = r"C:\Genesis\TEST_CONNECTION.txt"
    try:
        # 測試寫入能力 (僅限 Stage 1/2 允許的暫存區)
        with open(target_file, "w", encoding="utf-8") as f:
            f.write("CONNECTION_TEST_SUCCESS_VERIFIED")
        
        # 2. 生成實體 Hash 供總管校驗
        sha256_hash = hashlib.sha256()
        with open(target_file, "rb") as f:
            sha256_hash.update(f.read())
        
        result_hash = sha256_hash.hexdigest()
        
        print("[STAGE 1-2 SUCCESS] 通道通暢，檔案已生成。")
        print(f"[FILE_HASH] {result_hash}")
        
    except Exception as e:
        print(f"[STAGE 1-2 ERROR] 寫入遭攔截: {str(e)}")

if __name__ == "__main__":
    run_one_stop_test()