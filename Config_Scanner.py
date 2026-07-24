# Category: Data
import os
import subprocess

def scan_resources_and_print():
    root_path = r"C:\Genesis"
    
    print("--- [開始偵測資源] ---")
    
    # 1. 偵測路徑：直接列印出來
    print(f"\n[偵測路徑: {root_path}]")
    if os.path.exists(root_path):
        for root, dirs, files in os.walk(root_path):
            level = root.replace(root_path, '').count(os.sep)
            indent = ' ' * 4 * level
            print(f"{indent}[目錄] {os.path.basename(root)}")
            for f in files:
                print(f"{indent}    - {f}")
    else:
        print("警告：路徑 C:\\Genesis 不存在，請確認環境設定。")

    # 2. 偵測配搭程式：直接列印出來
    print("\n[偵測配搭程式與依賴環境]")
    check_cmds = {
        "Python": "python --version",
        "Node.js": "node -v",
        "Git": "git --version"
    }
    
    for name, cmd in check_cmds.items():
        try:
            version = subprocess.check_output(cmd, shell=True).decode().strip()
            print(f"-> {name}: {version}")
        except:
            print(f"-> {name}: 未偵測到")
    
    print("\n--- [偵測結束] ---")

if __name__ == "__main__":
    scan_resources_and_print()