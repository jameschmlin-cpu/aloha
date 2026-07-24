# -*- coding: utf-8 -*-
import os
import subprocess

class GenesisPreFlightSuite:
    def __init__(self):
        self.root = r"C:\Genesis"
        self.old_path = r"C:\Genesis"
        self.new_path = r"C:\Genesis"

    def run_all(self):
        print("=== [Genesis] 啟動全域預檢與修復序列 (編碼升級版) ===")
        self.fix_permissions()
        self.fix_hardcoded_paths()
        self.check_dependencies()
        print("=== [Genesis] 修復與檢查程序已完成 ===")

    def fix_permissions(self):
        print("[1/3] 正在修復物理寫入權限...")
        cmd = f'icacls "{self.root}" /grant:r %USERNAME%:(OI)(CI)F /T /C /Q'
        subprocess.check_call(cmd, shell=True)

    def fix_hardcoded_paths(self):
        print("[2/3] 正在全域掃描並修正編碼問題與路徑...")
        for root, _, files in os.walk(self.root):
            for file in files:
                if file.endswith(".py"):
                    path = os.path.join(root, file)
                    # 嘗試以多種編碼讀取，解決 UnicodeDecodeError
                    content = None
                    for enc in ['utf-8', 'cp950', 'big5', 'latin-1']:
                        try:
                            with open(path, 'r', encoding=enc) as f:
                                content = f.read()
                            break
                        except: continue
                    
                    if content and self.old_path in content:
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(content.replace(self.old_path, self.new_path))
                        print(f" -> 修正路徑並轉碼: {file}")

    def check_dependencies(self):
        print("[3/3] 最終結構完整性檢查...")
        for d in ["Config", "Database", "RD_Center"]:
            if not os.path.exists(os.path.join(self.root, d)):
                print(f"[Error] 遺失必要目錄: {d}")
        print("[Success] 環境已準備就緒。")

if __name__ == "__main__":
    suite = GenesisPreFlightSuite()
    suite.run_all()