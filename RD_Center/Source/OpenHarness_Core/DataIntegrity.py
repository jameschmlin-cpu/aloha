# -*- coding: utf-8 -*-
import hashlib
import os

class DataIntegrity:
    '''SDK 核心：負責所有檔案的實體 Hash 校驗與完整性監控'''
    def __init__(self, base_path=r"C:\\ITE"):
        self.base_path = base_path

    def calculate_hash(self, file_path):
        if not os.path.exists(file_path): return None
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def verify_and_lock(self, file_path, expected_hash):
        current_hash = self.calculate_hash(file_path)
        return current_hash == expected_hash
