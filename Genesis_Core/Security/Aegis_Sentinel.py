# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\Genesis_Core\Security\Aegis_Sentinel.py
import json
import sqlite3
import os

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
import sys
sys.path.append(os.path.join(GENESIS_BASE, "RD_Center"))
from SDK.Core.console_defender import setup_global_defense
setup_global_defense()
STATUS_FILE = os.path.join(GENESIS_BASE, "Genesis_Core", "Vault", "Hardware_Status.json")
DB_PATH = os.path.join(GENESIS_BASE, "Database", "Genesis_DFMEA.db")

class AegisSentinel:
    def check_physical_integrity(self):
        if not os.path.exists(STATUS_FILE): return
        
        with open(STATUS_FILE, "r") as f:
            status = json.load(f)
            
        # 邏輯判定 (FM-12 硬碟壞軌風險)
        if status["ssd_health"] < 20:
            self.trigger_fm("FM-12")
            
        # 邏輯判定 (FM-11 溫度過高)
        if status["cpu_temp"] > 90:
            self.trigger_fm("FM-11")

    def trigger_fm(self, fm_id):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT corrective FROM dfmea_matrix WHERE id=?", (fm_id,))
        action = cur.fetchone()[0]
        print(f"[警告] 物理異常偵測：觸發 {fm_id} -> {action}")
        conn.close()

if __name__ == "__main__":
    sentinel = AegisSentinel()
    sentinel.check_physical_integrity()