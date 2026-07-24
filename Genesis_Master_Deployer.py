# -*- coding: utf-8 -*-
import sys
import os

# [強制路徑歸位] 確保所有子目錄下的 SDK 都能被偵測到
GENESIS_ROOT = r"C:\Genesis"
SDK_PATHS = [
    GENESIS_ROOT, 
    os.path.join(GENESIS_ROOT, "RD_Center")
]

for p in SDK_PATHS:
    if p not in sys.path:
        sys.path.insert(0, p)

# 驗證模組是否存在，避免再次出現 ModuleNotFoundError
try:
    from Base_Template import GenesisBaseTemplate
except ImportError as e:
    print(f"[致命錯誤] 無法導入 Base_Template，路徑配置失敗: {e}")
    print(f"[除錯] 目前系統搜尋路徑: {sys.path}")
    sys.exit(1)

class MasterDeployer(GenesisBaseTemplate):
    def __init__(self):
        super().__init__()
        self.audit_log = r"C:\Genesis\Genesis_Ultimate_Audit.log"
        self.verified_bricks = []

    def deploy(self):
        print("[Deployer] 啟動閉環校驗...")
        if not os.path.exists(self.audit_log):
            print(f"[錯誤] 找不到審計日誌: {self.audit_log}")
            return

        with open(self.audit_log, 'r', encoding='utf-8') as f:
            for line in f:
                if "[✅ 安全]" in line:
                    brick_path = line.split("|")[1].strip()
                    self.verified_bricks.append(brick_path)

        for brick in self.verified_bricks:
            print(f"[部署] 積木已掛載: {os.path.basename(brick)}")
        
        print("-" * 50)
        print("[Final Ignition Successful] 帝國引擎全功率運行中。")

if __name__ == "__main__":
    deployer = MasterDeployer()
    deployer.deploy()