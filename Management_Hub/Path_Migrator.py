# C:\Genesis\Management_Hub\Path_Migrator.py
import os
import hashlib

# 定義遷移參數
SOURCE_DIR = r"C:\Genesis\RD_Center\Source\OpenHarness_Core\20class"
TARGET_PATH = r"C:\Genesis"
OLD_PATH = r"C:\ITE"

class Path_Migrator:
    """
    執行全局路徑遷徙：強制將所有 20 個類別的路徑定錨從 C:\ITE 轉移至 C:\Genesis。
    """
    def __init__(self):
        self.files_processed = 0

    def get_file_hash(self, file_path):
        """計算檔案 Hash 以確保遷移前後內容無損"""
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()

    def migrate(self):
        print(f"[STATUS] 開始路徑遷移: {SOURCE_DIR} -> {TARGET_PATH}")
        for root, _, files in os.walk(SOURCE_DIR):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    self.process_file(file_path)
                    self.files_processed += 1
        print(f"[STATUS] 遷移完成，共處理 {self.files_processed} 個類別檔案。")

    def process_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 進行剛性路徑替換
        if OLD_PATH in content:
            new_content = content.replace(OLD_PATH, TARGET_PATH)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  [FIXED] {os.path.basename(file_path)}")

if __name__ == "__main__":
    migrator = Path_Migrator()
    migrator.migrate()