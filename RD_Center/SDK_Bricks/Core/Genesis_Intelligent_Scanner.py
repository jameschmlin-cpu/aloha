# -*- coding: utf-8 -*-
# Compiled Brick from: Genesis_Intelligent_Scanner.py
# Category: Core

class GenesisIntelligentScannerBrick:
    def run(self, ctx=None):
        try:
            # -*- coding: utf-8 -*-
            import os
            import ast

            # 目標目錄清單
            TARGET_PATHS = [
                r"C:\Genesis\RD_Center\SDK\Core",
                r"C:\Genesis\RD_Center\SDK\ITE",
                r"C:\Genesis\RD_Center\SDK\System"
            ]

            def check_logic(path):
                """檢測程式邏輯中是否存在危險動作，並處理語法錯誤"""
                try:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        # 檢查是否包含惡意關鍵字 (排除路徑註解)
                        keywords = ['os.remove', 'shutil.rmtree', 'os.system(']
                        for kw in keywords:
                            if kw in content and 'system' not in path and 'cleaner' not in path.lower():
                                return True, kw

                        # 嘗試解析語法結構
                        tree = ast.parse(content)
                        return False, None

                except SyntaxError as e:
                    return True, f"SYNTAX_ERROR: {e.msg}"
                except Exception as e:
                    return True, f"READ_ERROR: {str(e)}"

            def run_smart_scan(target_dir):
                print(f"[智慧掃描] 正在執行深度邏輯分析: {target_dir}")
                if not os.path.exists(target_dir):
                    print(f"[系統警告] 路徑不存在: {target_dir}")
                    return

                for root, _, files in os.walk(target_dir):
                    for file in files:
                        if file.endswith(".py"):
                            path = os.path.join(root, file)
                            is_risky, trigger = check_logic(path)

                            if is_risky:
                                print(f"[⚠️ 異常] 發現問題: {file} | 原因: {trigger}")
                            else:
                                print(f"[✅ 安全] {file} 邏輯通過審核。")

            if __name__ == "__main__":
                print("--- Genesis 帝國智慧掃描引擎啟動 ---")
                for p in TARGET_PATHS:
                    run_smart_scan(p)
                print("--- 掃描作業完成 ---")
        except Exception as e:
            print(f"[GenesisIntelligentScannerBrick] 運行失敗: {e}")
            return False
        return True
