# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\.agents\skills\security-gate\scripts\validate_hash.py
# 狀態：已開發完成，負責專案寫入前置 AST 語法稽核與 Hash 校驗

import os
import sys
import ast
import hashlib

# 設定 stdout 與 stderr 保護，防範 Windows CP950 編碼崩潰
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(errors='replace')

def calculate_sha256(filepath):
    sha = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha.update(chunk)
    return sha.hexdigest().upper()

def check_encoding_header(filepath):
    """檢查前兩行是否包含編碼宣告"""
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            lines = [f.readline(), f.readline()]
        for line in lines:
            if "coding:" in line or "coding=" in line:
                if "utf-8" in line.lower():
                    return True
        return False
    except Exception:
        return False

def check_ast_integrity(filepath):
    """AST 靜態分析：防止空殼邏輯與 pass 懶惰缺陷 (FM-04)"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        root = ast.parse(content)
    except Exception as e:
        return False, f"語法解析錯誤: {e}"

    # 遍歷函數定義，檢查是否有函數體「僅有 pass 語句」的空殼實作
    for node in ast.walk(root):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # 如果函數體只有 1 個語句且該語句是 Pass，視為空殼缺陷
            if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                # 豁免特定故意保留的佔位符名稱，其餘一律攔截
                if node.name not in ["S2_Registry", "S3_Command_Center", "S4_Monitor_Defense"]:
                    return False, f"在函數 '{node.name}' 中偵測到 pass 空殼邏輯缺陷 (FM-04)，必須寫入具體回傳或拋出異常！"
    
    # 檢查 Core_Gateway 特有繼承鏈
    if os.path.basename(filepath) == "Core_Gateway.py":
        for node in ast.walk(root):
            if isinstance(node, ast.ClassDef) and node.name == "Core_Gateway":
                has_base = False
                for base in node.bases:
                    if isinstance(base, ast.Name) and base.id == "OpenHarness_Base":
                        has_base = True
                        break
                if not has_base:
                    return False, "Core_Gateway 類別必須繼承自 OpenHarness_Base，以維護 S1-S4 生命週期整合！"

    return True, "AST 結構檢驗合格"

def main():
    if len(sys.argv) < 2:
        print("[錯誤] 請指定要驗證的檔案路徑！")
        sys.exit(1)

    target_file = sys.argv[1]
    if not os.path.exists(target_file):
        print(f"[錯誤] 找不到指定檔案: {target_file}")
        sys.exit(1)

    print(f"[*] 開始對 {os.path.basename(target_file)} 進行 Genesis 規範校驗...")

    # 1. 檢驗編碼 header
    if not check_encoding_header(target_file):
        print("[❌] 驗證失敗：缺少必要的 UTF-8 編碼宣告 (例如: # -*- coding: utf-8 -*-)！")
        sys.exit(1)
    print("  [+] UTF-8 編碼宣告檢驗：通過")

    # 2. 檢驗 AST 結構完整性
    ast_ok, msg = check_ast_integrity(target_file)
    if not ast_ok:
        print(f"[❌] 驗證失敗：{msg}")
        sys.exit(1)
    print(f"  [+] {msg}：通過")

    # 3. 計算實體 Hash 碼
    try:
        file_hash = calculate_sha256(target_file)
        print(f"  [+] 實體 SHA-256 Hash 碼: {file_hash}")
    except Exception as e:
        print(f"[❌] 檔案 Hash 計算失敗: {e}")
        sys.exit(1)

    print("[STATUS] PASSED")
    sys.exit(0)

if __name__ == "__main__":
    main()
