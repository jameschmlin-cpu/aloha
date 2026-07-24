# -*- coding: utf-8 -*-


"""


====================================================================


龍蝦帝國 (OpenClaw) 最高核心載體


大一統鋼鐵底盤總模組：Grand_Chassis.py (五大派系自動化裝填完全體)


物理鎖定路徑: C:\Genesis\SDK\Core\Grand_Chassis.py


[修正日誌]：


  1. 修復 Python 3.12+ 轉義路徑警告 (SyntaxWarning)。


  2. 強制隔離資料庫寫入路徑至 Database_Active 以避開唯讀鎖定。


  3. 加入寫入成功與失敗的剛性物理校驗機制。


====================================================================


"""





import os


import json


import time


import sqlite3


import hashlib


from datetime import datetime





# 剛性鎖定 C:\Genesis 核心路徑 (使用原始字串 R 開頭防止轉義警告)


BASE_PATH = r"C:\Genesis"


REGISTRY_FILE = os.path.join(BASE_PATH, "SDK", "Registry.json")


# 移至 Active 資料夾避開唯讀與系統鎖定


DB_DIR = os.path.join(BASE_PATH, "Database_Active")


DB_PATH = os.path.join(DB_DIR, "Lobster_Connectivity.db")


COMPONENTS_DIR = os.path.join(BASE_PATH, "SDK", "Components")





class LobsterGrandChassis:


    


    def __init__(self):


        self.registry_path = REGISTRY_FILE


        self.db_path = DB_PATH


        self.components_dir = COMPONENTS_DIR


        


        # 建立物理端必備資料夾防線


        os.makedirs(self.components_dir, exist_ok=True)


        os.makedirs(DB_DIR, exist_ok=True)


        self._ensure_db_initialized()


        self._write_chassis_log("CHASSIS_INIT", "SUCCESS", "大一統鋼鐵底盤初始化，路徑導通。")


    # 直接掛載中央調度器，消除連線延遲


        self.dispatcher = Central_Dispatcher_Core(self.registry_path)





    def _ensure_db_initialized(self):


        """物理硬咬合：確保資料庫導通"""


        try:


            conn = sqlite3.connect(self.db_path, timeout=30)


            cursor = conn.cursor()


            cursor.execute('''


                CREATE TABLE IF NOT EXISTS connectivity_logs (


                    id INTEGER PRIMARY KEY AUTOINCREMENT,


                    timestamp TEXT,


                    task_name TEXT,


                    status TEXT,


                    detail TEXT


                )


            ''')


            conn.commit()


            conn.close()


        except Exception as e:


            print(f"[DB_FATAL] 無法初始化資料庫: {e}")





    def _write_chassis_log(self, action: str, status: str, detail: str):


        """誠信審計存證"""


        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


        try:


            conn = sqlite3.connect(self.db_path, timeout=30)


            cursor = conn.cursor()


            cursor.execute('''


                INSERT INTO connectivity_logs (timestamp, task_name, status, detail)


                VALUES (?, ?, ?, ?)


            ''', (timestamp, f"[Grand_Chassis] {action}", status, detail))


            conn.commit()


            conn.close()


        except Exception as e:


            print(f"[LOG_FATAL] {e}")





    def get_faction_blueprint(self, module_id: str) -> str:


        """派系核心藍圖庫"""


        blueprints = {


            "VERTEX_AI_BASICS": "    def execute_core_skill(self, payload: dict) -> dict:\n        return {'status': 'SUCCESS', 'faction': 'Google Agent Skills'}",


            "ADMIN_PAYROLL_CORE": "    def execute_core_skill(self, payload: dict) -> dict:\n        return {'status': 'SUCCESS', 'faction': 'Salary_Payroll_SOP'}",


            "CLAUDE_SANDBOX_COMPILER": "    def execute_core_skill(self, payload: dict) -> dict:\n        return {'status': 'SUCCESS', 'faction': 'Claude_Sandbox'}",


            "PUBLIC_OS_HAL": "    def execute_core_skill(self, payload: dict) -> dict:\n        return {'status': 'SUCCESS', 'faction': 'OS_HAL_LAYER'}",


            "DEEPMIND_VRAM_RESIDENT": "    def execute_core_skill(self, payload: dict) -> dict:\n        return {'status': 'SUCCESS', 'faction': 'VRAM_OPT'}"


        }


        return blueprints.get(module_id, "")





    def webmcp_auto_build_component(self, module_id: str) -> dict:


        """自動化生產核心邏輯"""


        if not os.path.exists(self.registry_path):


            return {"status": "FAIL", "message": "Missing Registry.json"}





        with open(self.registry_path, 'r', encoding='utf-8') as f:


            registry = json.load(f)





        if module_id not in registry.get("components", {}):


            return {"status": "FAIL", "message": f"Module {module_id} not in registry"}





        file_name = registry["components"][module_id].get("file_name")


        physical_file_path = os.path.join(self.components_dir, file_name)





        faction_skill = self.get_faction_blueprint(module_id)


        raw_code = f"class {module_id}_Component:\n{faction_skill}"


        sha256_hash = hashlib.sha256(raw_code.encode('utf-8')).hexdigest()


        


        final_code = f"# Hash: {sha256_hash}\n{raw_code}"





        try:


            with open(physical_file_path, 'w', encoding='utf-8') as f:


                f.write(final_code)


            


            registry["components"][module_id]["status"] = "ACTIVE"


            registry["components"][module_id]["sha256"] = sha256_hash


            with open(self.registry_path, 'w', encoding='utf-8') as f:


                json.dump(registry, f, indent=4)


            


            print(f"🟢 [裝填成功] {module_id}")


            return {"status": "SUCCESS"}


        except Exception as e:


            return {"status": "FAIL", "message": str(e)}





   def execute_empire_tasks(self):


            # 調度器直接操作 Chassis 生產線


            self.dispatcher.run_cycle(self)





if __name__ == "__main__":


    chassis = LobsterGrandChassis()


    factions = ["VERTEX_AI_BASICS", "ADMIN_PAYROLL_CORE", "CLAUDE_SANDBOX_COMPILER", "PUBLIC_OS_HAL", "DEEPMIND_VRAM_RESIDENT"]


    for f in factions:


        chassis.webmcp_auto_build_component(f)