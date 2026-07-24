# -*- coding: utf-8 -*-
# C:\Genesis\SDK\pre_flight_check.py
# 嚴格執行：預判全局 - 行為分析與歷史風險熔斷

import sqlite3
import ast
import os
import sys

def find_genesis_base():
    if "GENESIS_HOME" in os.environ:
        return os.environ["GENESIS_HOME"]
    current = os.path.abspath(__file__)
    while True:
        parent, name = os.path.split(current)
        if name.lower() == "genesis" or os.path.exists(os.path.join(current, "Genesis_Map.json")):
            return current
        if not name:
            break
        current = parent
    return r"C:\Genesis"

GENESIS_BASE = find_genesis_base()
sys.path.insert(0, os.path.join(GENESIS_BASE, "RD_Center"))

from SDK.Core.console_defender import setup_global_defense
setup_global_defense()

class IndustrialPreFlight:
    def __init__(self):
        # 實體路徑鎖定
        self.db_path = os.path.join(GENESIS_BASE, "Database", "Genesis_DFMEA.db")

    def analyze_behavior(self, script_path):
        """Stage 1: 行為風險評估 (透過 AST 語法樹)"""
        try:
            with open(script_path, 'r', encoding='utf-8', errors='ignore') as f:
                tree = ast.parse(f.read())
            
            risk_score = 0
            for node in ast.walk(tree):
                # 偵測破壞性屬性 (僅當主體為系統模組 os/subprocess/shutil 時)
                if isinstance(node, ast.Attribute):
                    if node.attr in ['remove', 'rmdir', 'unlink', 'system', 'popen']: 
                        if isinstance(node.value, ast.Name) and node.value.id in ['os', 'subprocess', 'shutil']:
                            risk_score += 50
                        elif not isinstance(node.value, ast.Name):
                            # 調用主體非靜態變數名，保留輕微安全防禦值，不直接觸發熔斷
                            risk_score += 15
                # 偵測危險系統呼叫
                if isinstance(node, ast.Call):
                    func_name = ''
                    if isinstance(node.func, ast.Name):
                        func_name = node.func.id
                    elif isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
                        func_name = node.func.value.id
                    if func_name in ['subprocess', 'os', 'shutil']:
                        risk_score += 30
            return risk_score
        except Exception as e:
            print(f"[除錯] 行為分析失敗: {e}")
            return 0

    def check_risk_matrix(self, script_path):
        """Stage 2: 歷史失效機率查詢 (DFMEA 資料庫對接)"""
        if not os.path.exists(self.db_path):
            return 0
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT severity FROM dfmea_matrix WHERE problem_point LIKE ?", 
                           (f"%{os.path.basename(script_path)}%",))
            res = cursor.fetchone()
            return res[0] if res else 0
        except:
            return 0
        finally:
            conn.close()

    def run_pre_flight(self, script_path):
        """Stage 3: 全局預判決策 (整合行為與歷史)"""
        if not os.path.exists(script_path):
            print(f"[錯誤] 檔案不存在: {script_path}")
            return False
            
        behavior_risk = self.analyze_behavior(script_path)
        history_risk = self.check_risk_matrix(script_path)
        total_risk = behavior_risk + history_risk
        
        print(f"[全局預判] 程式: {os.path.basename(script_path)}")
        print(f"[運算結果] 行為風險: {behavior_risk} | 歷史風險: {history_risk} | 總分: {total_risk}")
        
        # Stage 4: 熔斷判定
        if total_risk > 60:
            print("[熔斷警報] 風險指標超過 60，物理執行已禁止！")
            return False
        
        print("[預判合格] 系統安全，允許掛載執行。")
        return True

if __name__ == "__main__":
    # 執行自我驗證邏輯
    checker = IndustrialPreFlight()
    # 預設對 gatekeeper 進行預判測試
    target_path = os.path.join(GENESIS_BASE, "SDK", "gatekeeper.py")
    success = checker.run_pre_flight(target_path)
    
    # 確保返回正確的 Exit Code
    if not success:
        sys.exit(1)