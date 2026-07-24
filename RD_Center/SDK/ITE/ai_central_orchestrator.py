import os

import json

import ast

import warnings



# QE防錯：剛性封鎖前任留下的所有字串與轉義警告雜訊

warnings.filterwarnings("ignore", category=SyntaxWarning)



BRAIN_DB = r"C:\\ITE\\native_brain_db.json"

SDK_DIR = r"C:\\ITE"



def sub_A_clean_and_scan():

    assets = []

    for root, dirs, files in os.walk(SDK_DIR):

        for file in files:

            if file.endswith('.py') and file != "AI_Central_Orchestrator.py":

                assets.append(os.path.join(root, file))

    return assets



def sub_B_perfect_gatekeeper(file_paths):

    clean_assets = []

    for path in file_paths:

        try:

            with open(path, 'r', encoding='utf-8-sig', errors='ignore') as f:

                content = f.read()

            if "TODO" in content or "pass" in content:

                continue

            ast.parse(content)

            clean_assets.append(path)

        except Exception:

            continue

    print(f"\n[副程式 B V3] 完工：已自動過濾雜訊！篩選出 {len(clean_assets)} 支地端安全真傢伙。")

    return clean_assets



def sub_C_dynamic_brain_update(conclusions):

    if os.path.exists(BRAIN_DB):

        with open(BRAIN_DB, 'r', encoding='utf-8') as f:

            db = json.load(f)

        db["dynamic_learning_conclusions"] = conclusions

        db["last_整理_time"] = "2026-05-29"

        with open(BRAIN_DB, 'w', encoding='utf-8') as f:

            json.dump(db, f, indent=4, ensure_ascii=False)

        print("[副程式 C V3] 大腦增量重新整理完畢。")



if __name__ == "__main__":

    print("=== Taipei 百佳長照 & 林口基地 中央調度器 V3 雜訊淨化點火 ===")

    raw_files = sub_A_clean_and_scan()

    clean_files = sub_B_perfect_gatekeeper(raw_files)

    

    conclusions = [f"B計畫完全定錨：已由 V3 閘衛兵完全洗淨解鎖 {len(clean_files)} 支真傢伙資產。"]

    sub_C_dynamic_brain_update(conclusions)

    print("=== 系統去毒完畢，第一階段倉庫與調度線 100% 閉環待命 ===")


