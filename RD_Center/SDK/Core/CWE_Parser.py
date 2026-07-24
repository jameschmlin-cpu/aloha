# -*- coding: utf-8 -*-

# 檔案：C:\Genesis\Genesis_Core\CWE_Parser.py

# 狀態：修正版 (解決 UNIQUE constraint 衝突)



import xml.etree.ElementTree as ET

import sqlite3

import os



def parse_cwe_to_db():

    xml_file = r"C:\Genesis\Genesis_Core\Data\cwec_v4.20.xml"

    db_file = r"C:\Genesis\Genesis_Core\Data\CWE_Standard.db"

    

    print(f"[*] 正在解析 CWE XML: {xml_file}...")

    

    context = ET.iterparse(xml_file, events=('end',))

    

    conn = sqlite3.connect(db_file)

    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS CWE_Library (cwe_id TEXT PRIMARY KEY, mitigation TEXT)")

    

    count = 0

    for event, elem in context:

        if elem.tag.endswith('Weakness'):

            cwe_id = f"CWE-{elem.get('ID')}"

            mitigation_text = "標準防禦: 請查閱官方 CWE 建議"

            

            mitigations = elem.find('.//{http://cwe.mitre.org/cwe-7}Mitigations')

            if mitigations is not None:

                m_node = mitigations.find('.//{http://cwe.mitre.org/cwe-7}Mitigation')

                if m_node is not None and m_node.text:

                    mitigation_text = m_node.text.strip()

            

            # 關鍵修改：使用 INSERT OR IGNORE 避開重複項衝突

            cursor.execute("INSERT OR IGNORE INTO CWE_Library (cwe_id, mitigation) VALUES (?, ?)", 

                           (cwe_id, mitigation_text))

            

            if cursor.rowcount > 0:

                count += 1

            elem.clear()

            

    conn.commit()

    conn.close()

    print(f"[*] 轉換完成，共寫入 {count} 筆唯一弱點規則至 {db_file}")



if __name__ == "__main__":

    if os.path.exists(r"C:\Genesis\Genesis_Core\Data\cwec_v4.20.xml"):

        parse_cwe_to_db()

    else:

        print("[!] 錯誤: 找不到 XML 檔案。")