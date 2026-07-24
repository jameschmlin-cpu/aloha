# C:\Genesis\Management_Hub\DB_Path_Validator.py
import os

target_dir = r"C:\Genesis\RD_Center\Source\OpenHarness_Core\20class"
new_db_path = r"C:\Genesis\Database\Lobster_Connectivity.db"

def validate_db_paths():
    for root, _, files in os.walk(target_dir):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if "C:\\ITE\\Database\\Lobster_Connectivity.db" in content:
                        print(f"[CRITICAL] 類別 {file} 尚未更換資料庫路徑。")
                    elif new_db_path in content:
                        continue
    print("[STATUS] 20 個 Class 資料庫路徑核驗完畢。")

if __name__ == "__main__":
    validate_db_paths()