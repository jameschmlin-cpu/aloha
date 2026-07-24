# -*- coding: utf-8 -*-
# Compiled Brick from: Genesis_Imperial_Total_Repair.py
# Category: Core

class GenesisImperialTotalRepairBrick:
    def run(self, ctx=None):
        try:
            import os

            # 需要修復的檔案清單 (根據您的 Log 歸納)
            TARGET_FILES = [
                r"C:\Genesis\RD_Center\SDK\Core\Grand_Chassis.py",
                r"C:\Genesis\RD_Center\SDK\Core\Orchestrator.py",
                r"C:\Genesis\RD_Center\SDK\Core\Upper_Sovereign_Manager.py",
                r"C:\Genesis\RD_Center\SDK\ITE\ai_central_orchestrator.py",
                r"C:\Genesis\RD_Center\SDK\ITE\AI_Empire_Complete.py",
                r"C:\Genesis\RD_Center\SDK\ITE\Google_Library_Deployer.py",
                r"C:\Genesis\RD_Center\SDK\ITE\rebuild_vault.py",
                r"C:\Genesis\RD_Center\SDK\System\Central_Dispatcher.py",
                r"C:\Genesis\RD_Center\SDK\System\Imperial_Sovereign_Core.py"
            ]

            def repair_file(path):
                try:
                    with open(path, 'rb') as f:
                        content = f.read()
                    # 移除 BOM 與修正亂碼
                    text = content.decode('utf-8-sig').replace('\t', '    ')
                    # 強制修復路徑格式 (簡單正規化)
                    text = text.replace(r"'\C:", r"r'C:") 

                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(text)
                    return True
                except Exception:
                    return False

            print("[系統] 啟動帝國全自動外科手術修復...")
            for f in TARGET_FILES:
                if os.path.exists(f):
                    if repair_file(f):
                        print(f"[✅] 已修復: {f}")
                    else:
                        print(f"[❌] 修復失敗: {f}")
                else:
                    print(f"[⚠️] 找不到檔案: {f}")

            print("[系統] 修復作業結束。請確認無誤後，我們直接啟動 Master_Deployer。")
        except Exception as e:
            print(f"[GenesisImperialTotalRepairBrick] 運行失敗: {e}")
            return False
        return True
