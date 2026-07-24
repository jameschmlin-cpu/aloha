# -*- coding: utf-8 -*-

# 檔案：C:\Genesis\Genesis_Core\Memory_Interface.py

# 狀態：全功能單一封裝版 - 整合故障監控與跨模組鎖定



import sys


import sqlite3

from datetime import datetime



# 強制路徑錨定

sdk_path = r"C:\Genesis\SDK\Base"

if sdk_path not in sys.path:

    sys.path.append(sdk_path)

from connectivity_base import BaseConnectivityOP



class Memory_Interface(BaseConnectivityOP):

    def __init__(self):

        super().__init__()

        self.mem_db_path = r"C:\Genesis\Genesis_Core\Data\Unified_Empire_Memory.db"



    def report(self, tag, message):

        output = f"[報訊][{tag}] {message}"

        sys.stdout.write(output + "\n")

        with open(self.audit_log, "a") as f:

            f.write(output + "\n")



   # --- 功能一：全節點故障監控 (內嵌實體邏輯) ---

    def check_and_fuse_node(self, node_id, timeout_sec=60):

        """實體故障診斷：檢查心跳並強制熔斷"""

        conn = sqlite3.connect(self.mem_db_path)

        cursor = conn.cursor()

        cursor.execute("SELECT timestamp FROM State_Table WHERE service_name = ?", (node_id,))

        row = cursor.fetchone()

        

        if not row:

            conn.close()

            return False

            

        last_time = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')

        conn.close()

        

        diff = (datetime.now() - last_time).total_seconds()

        if diff > timeout_sec:

            # 實體熔斷邏輯：直接更新狀態至 CRITICAL_FAILURE，強制隔離

            conn = sqlite3.connect(self.mem_db_path)

            conn.execute("UPDATE State_Table SET status = 'CRITICAL_FAILURE' WHERE service_name = ?", (node_id,))

            conn.commit()

            conn.close()

            self.report("CRITICAL_FAILURE", f"Node {node_id} isolated due to timeout ({diff}s).")

            return False

        return True



    # --- 功能二：跨模組同步校驗 (真值來源鎖定) ---

    def execute_with_lock(self, service_name, action_func, *args):

        """強制鎖定檢查：執行前檢查 lock_status"""

        conn = sqlite3.connect(self.mem_db_path)

        cursor = conn.cursor()

        cursor.execute("SELECT lock_status FROM State_Table WHERE service_name = ?", (service_name,))

        row = cursor.fetchone()

        conn.close()

        

        if row and row[0] == 'LOCKED':

            self.report("ACCESS_DENIED", f"Service {service_name} is LOCKED. Execution aborted.")

            return None

        

        # 執行任務

        return action_func(*args)



    # --- 功能三：整合型 QC 狀態更新 ---

    def update_status(self, service_name, status, hash_val=None):

        """含 Hash 稽核的實體更新"""

        conn = sqlite3.connect(self.mem_db_path)

        # 稽核機制：比對 Hash

        if hash_val:

            cursor = conn.cursor()

            cursor.execute("SELECT hash_val FROM State_Table WHERE service_name = ?", (service_name,))

            db_hash = cursor.fetchone()

            if not db_hash or db_hash[0] != hash_val:

                self.report("SECURITY_VIOLATION", f"Integrity check failed for {service_name}.")

                conn.close()

                return False

        

        conn.execute("UPDATE State_Table SET status = ?, timestamp = ? WHERE service_name = ?", 

                     (status, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), service_name))

        conn.commit()

        conn.close()

        self.report("UPDATE_SUCCESS", f"{service_name} set to {status}.")

        return True



if __name__ == "__main__":

    mem = Memory_Interface()

    # 執行監控與校驗

    if mem.check_and_fuse_node('Node_A'):

        sys.stdout.write("[系統] Node_A 正常運作。\n")

    else:

        sys.stdout.write("[系統] Node_A 已隔離。\n")