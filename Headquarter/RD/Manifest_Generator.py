# ==============================================================================
# Manifest_Generator.py - Antigravity 2.0 SDK 4 Stages Compliant
# 功能：自動掃描 RD 目錄，執行 Hash 簽章，產出合規地圖檔
# ==============================================================================

import os
import yaml
import hashlib

class ManifestGenerator:
    def __init__(self):
        self.rd_dir = r"C:\Genesis\Headquarter\RD"
        self.manifest_path = os.path.join(self.rd_dir, "Manifest.yaml")

    def get_file_hash(self, filepath):
        """ 計算檔案的 SHA-256 Hash 值 (SDK 4 Stages 剛性規範) """
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()[:12]

    def run(self):
        print(f"[System] 正在掃描 RD 目錄: {self.rd_dir} ...")
        registry = {"Version": "2.0", "Assets": {}}
        
        for filename in os.listdir(self.rd_dir):
            # 僅掃描符合規範的格式
            if filename.endswith(('.py', '.yaml', '.yml')):
                if filename in ["Manifest_Generator.py", "Final_Rescue_Deployer.py"]:
                    continue # 略過工具本體
                
                filepath = os.path.join(self.rd_dir, filename)
                f_hash = self.get_file_hash(filepath)
                
                registry["Assets"][filename] = {
                    "path": filepath,
                    "hash": f_hash,
                    "status": "REGISTERED"
                }
                print(f"[REGISTERED] {filename} | Hash: {f_hash}")

        with open(self.manifest_path, 'w', encoding='utf-8') as f:
            yaml.dump(registry, f, sort_keys=False)
            
        print(f"[SUCCESS] 地圖檔已寫入: {self.manifest_path}")

if __name__ == "__main__":
    generator = ManifestGenerator()
    generator.run()