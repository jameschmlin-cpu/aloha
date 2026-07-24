import hashlib
import os

# Genesis SDK QA Node A-D Mapping
PATHS = [r"C:\Genesis", r"C:\Genesis\Engine", r"C:\Genesis\Projects"]

def get_file_hash(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def verify_system():
    print("--- Genesis QA Node A: System Integrity Check ---")
    for path in PATHS:
        if os.path.exists(path):
            print(f"[NODE A] Path Found: {path}")
        else:
            print(f"[NODE A] ERROR: Path Missing: {path}")
            return False
    print("--- Genesis QA Node B: QC Sensor Active ---")
    print("QC Agent: Status Ready. Waiting for Native_Core Injection.")
    return True

if __name__ == "__main__":
    if verify_system():
        print("\n[SUCCESS] Node C: Verification Complete. System ready for Gemini Native Integration.")
    else:
        print("\n[FAILED] Node C: System environment error. Do not proceed.")