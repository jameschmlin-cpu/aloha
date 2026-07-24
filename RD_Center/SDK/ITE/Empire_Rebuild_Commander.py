import os

import shutil


import ast



# 設定路徑

SDK_PATH = r"C:\Genesis\SDK"

ARCHIVE_PATH = r"C:\Genesis\Archive_Fraud"

os.makedirs(ARCHIVE_PATH, exist_ok=True)



def is_hollow(filepath):

    """檢查是否為空殼，加入邏輯判斷"""

    try:

        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:

            code = f.read()

            tree = ast.parse(code)

            # 判斷標準：若類別/函數過少或含 TODO/pass，即為空殼

            nodes = [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.ClassDef))]

            if len(nodes) < 2 or "TODO" in code or "pass" in code:

                return True

    except: return True

    return False



def rebuild_empire():

    report = []

    print("🚀 [重構總司令] 正在清算 SDK... ")

    

    for root, _, files in os.walk(SDK_PATH):

        for file in files:

            if file.endswith(".py"):

                path = os.path.join(root, file)

                # 判定

                if is_hollow(path):

                    # 執行物理搬移 (割離垃圾)

                    dest = os.path.join(ARCHIVE_PATH, file)

                    shutil.move(path, dest)

                    report.append(f"【廢墟封存】: {file}")

                else:

                    report.append(f"【基石保留】: {file}")

    

    # 輸出總帳

    with open(os.path.join(SDK_PATH, "重構總帳.log"), "w", encoding="utf-8") as f:

        f.write("\n".join(report))

    print(f"✅ [重構完成] 總帳已存入 SDK 目錄。所有廢墟已封存至 {ARCHIVE_PATH}")



if __name__ == "__main__":

    rebuild_empire()