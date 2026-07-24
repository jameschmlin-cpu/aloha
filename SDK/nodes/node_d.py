# C:\Genesis\SDK\nodes\node_d.py
import hashlib
import os
import json

class NodeD_Validator:
    """閉環驗證器：對執行結果進行物理 Hash 與邏輯完整性校驗"""
    def __init__(self, registry_path=r"C:\Genesis\SDK\Registry.json"):
        self.registry_path = registry_path

    def calculate_file_hash(self, file_path):
        """計算實體檔案的 SHA-256"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def validate_integrity(self, target_file, expected_hash):
        """物理比對：若不一致則觸發異常機制"""
        if not os.path.exists(target_file):
            return False, "Target file missing."
            
        actual_hash = self.calculate_file_hash(target_file)
        if actual_hash == expected_hash:
            return True, "Integrity Verified."
        else:
            return False, f"Hash mismatch! Expected {expected_hash}, got {actual_hash}"