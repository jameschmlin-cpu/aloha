# 檔案：C:\Genesis\Genesis_Core\Path_Validator.py

import os

import sqlite3

import re



def validate_paths():

    report = []

    # 權威路徑庫

    db_path = r"C:\Genesis\Genesis_Core\Data\path_master.db"

    conn = sqlite3.connect(db_path)

    authorized = [row[0] for row in conn.execute("SELECT physical_path FROM PathRegistry").fetchall()]

    conn.close()



    # 掃描 59 支程式

    for root, _, files in os.walk(r"C:\Genesis\Genesis_Core"):

        for file in files:

            if file.endswith((".py", ".ps1", ".bat")):

                with open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore') as f:

                    content = f.read()

                    found_paths = re.findall(r'[A-Z]:\\[^"\s]+', content)

                    for p in found_paths:

                        # 檢查是否在權威路徑清單內

                        if not any(auth in p for auth in authorized):

                            report.append(f"檔案: {file} | 錯誤路徑: {p}")

    

    with open("Audit_Report.txt", "w", encoding="utf-8") as f:

        f.write("\n".join(report))

    print("[*] 稽核完成，結果已產出於 Audit_Report.txt")



if __name__ == "__main__":

    validate_paths()