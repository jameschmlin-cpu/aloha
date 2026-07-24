import os
import hashlib

def scan_genesis():
    scan_log = "Genesis_System_Fingerprint.txt"
    with open(scan_log, "w", encoding="utf-8") as f:
        f.write("=== Genesis System Environment Fingerprint ===\n")
        for root, dirs, files in os.walk(r"C:\Genesis"):
            for file in files:
                path = os.path.join(root, file)
                try:
                    # 簡單 Hash 比對確保檔案完整性
                    with open(path, "rb") as bf:
                        file_hash = hashlib.md5(bf.read()).hexdigest()
                    f.write(f"{path} | Hash: {file_hash}\n")
                except Exception as e:
                    f.write(f"{path} | Error: {e}\n")
    print(f"掃描完成。指紋清單已儲存至: {scan_log}")

if __name__ == "__main__":
    scan_genesis()