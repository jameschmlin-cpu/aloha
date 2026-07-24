# -*- coding: utf-8 -*-
# Compiled Brick from: Genesis_Architecture_Audit.py
# Category: Core

class GenesisArchitectureAuditBrick:
    def run(self, ctx=None):
        try:
            import json
            from pathlib import Path

            def scan_genesis_architecture(root_path=r"C:\Genesis"):
                root = Path(root_path)
                # 定義 SDK 層級路徑特徵
                architecture_map = {
                    "Base_Layer_OpenHarness": [],
                    "Active_20_Classes": [],
                    "Logical_Library_130": [],
                    "Unknown_Or_Orphaned": []
                }

                # 執行遞迴掃描
                for file_path in root.rglob("*.py"):
                    relative_path = str(file_path.relative_to(root))

                    # 邏輯層分類標記
                    if "OpenHarness" in relative_path:
                        architecture_map["Base_Layer_OpenHarness"].append(relative_path)
                    elif "SDK" in relative_path and "Library" not in relative_path:
                        architecture_map["Active_20_Classes"].append(relative_path)
                    elif "Library" in relative_path or "Logical_Library" in relative_path:
                        architecture_map["Logical_Library_130"].append(relative_path)
                    else:
                        architecture_map["Unknown_Or_Orphaned"].append(relative_path)

                # 儲存掃描結果至 JSON 檔案
                output_path = root / "Genesis_Map.json"
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(architecture_map, f, indent=4, ensure_ascii=False)

                return str(output_path)

            if __name__ == "__main__":
                result_file = scan_genesis_architecture()
                print(f"[掃描完成] 帝國拓撲圖已產出: {result_file}")
        except Exception as e:
            print(f"[GenesisArchitectureAuditBrick] 運行失敗: {e}")
            return False
        return True
