import os
import json

class GenesisArchitect:
    def __init__(self, root=r"C:\Genesis"):
        self.root = root
        self.config = {
            "path_structure": {},
            "dependencies": {}
        }

    def run_full_scan(self):
        # 自動遍歷，建立完整路徑與資源映射
        for root, dirs, files in os.walk(self.root):
            # 忽略大型緩存目錄
            if "__pycache__" in dirs: dirs.remove("__pycache__")
            if "node_modules" in dirs: dirs.remove("node_modules")
            
            relative_path = os.path.relpath(root, self.root)
            self.config["path_structure"][relative_path] = files
            
            # 搜尋關鍵配置文件以偵測配搭程式
            for f in files:
                if f in ["package.json", "requirements.txt", "pyproject.toml"]:
                    self.config["dependencies"][relative_path] = f
        
        # 直接產出配置檔案
        config_path = os.path.join(self.root, "system_runtime_config.json")
        with open(config_path, "w") as f:
            json.dump(self.config, f, indent=4)
        return config_path

if __name__ == "__main__":
    architect = GenesisArchitect()
    output = architect.run_full_scan()
    print(f"系統配置已自動生成於: {output}")