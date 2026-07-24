import os
import yaml

def auto_heal():
    target_dir = r"C:\Genesis"
    mapping_path = os.path.join(target_dir, "Database", "tasks_mapping.yaml")
    
    # 1. 自動掃描並建立真實路徑字典
    real_files = {}
    for root, _, files in os.walk(target_dir):
        for file in files:
            if file.endswith(".py"):
                real_files[file] = os.path.join(root, file)
    
    # 2. 自動重寫 Mapping 檔案，排除所有虛假路徑
    new_mapping = {"tasks_mapping": real_files}
    
    with open(mapping_path, "w", encoding="utf-8") as f:
        yaml.dump(new_mapping, f, allow_unicode=True)
    
    print(f"🟢 [自動修復] Mapping 已更新，共對接 {len(real_files)} 個實體檔案。")
    print(f"🟢 [自動修復] 系統路徑已重置至 {target_dir}")

if __name__ == "__main__":
    auto_heal()