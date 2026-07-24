import os

import shutil



# 設定檔案庫

ARCHIVE_PATH = r"C:\Genesis\Archive_Fraud"

RESTORE_PATH = r"C:\Genesis\SDK"



def restore_legacy_files():

    print("⚖️ [帝國遺產修正案] 啟動遺產赦免程序...")

    

    # 定義前輩留下的核心特徵關鍵字 (根據 Grand_Chassis.py 的風格)

    legacy_markers = ["sqlite3", "hashlib", "datetime", "SovereignBlankForm", "chassis"]

    

    for file in os.listdir(ARCHIVE_PATH):

        if file.endswith(".py"):

            src = os.path.join(ARCHIVE_PATH, file)

            with open(src, 'r', encoding='utf-8', errors='ignore') as f:

                content = f.read()

                

                # 只要符合前輩的特徵，即刻歸還

                if any(marker in content for marker in legacy_markers):

                    shutil.move(src, os.path.join(RESTORE_PATH, file))

                    print(f"✅ [遺產歸還]: {file}")

                else:

                    print(f"⚠️ [持續封存]: {file} (經判定確認為前任垃圾)")



if __name__ == "__main__":

    restore_legacy_files()