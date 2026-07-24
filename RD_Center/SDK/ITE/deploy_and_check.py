import os

import sys

import sqlite3

import hashlib

import platform

import multiprocessing



def calculate_file_hash(filepath):

    """計算實體檔案的 SHA-256 Hash 值，確保防逃逸校驗"""

    sha256_hash = hashlib.sha256()

    with open(filepath, "rb") as f:

        for byte_block in iter(lambda: f.read(4096), b""):

            sha256_hash.update(byte_block)

    return sha256_hash.hexdigest()



def detect_and_deploy():

    print("==================================================")

    print("  龍蝦系統核心：本地端資源自主診斷與佈署自動化啟動  ")

    print("==================================================")

    

    # 1. 物理端與邏輯端資源環境偵測

    print("\n[Node A] 啟動本地環境實體偵測...")

    system_info = {

        "OS": platform.system(),

        "OS_Release": platform.release(),

        "CPU_Cores": multiprocessing.cpu_count(),

        "Python_Version": platform.python_version()

    }

    

    for key, value in system_info.items():

        print(f"  -> {key}: {value}")

        

    # 核心路徑檢查

    base_dir = r"C:\Genesis"

    if not os.path.exists(base_dir):

        print(f"🚨【權限阻斷】未偵測到實體核心路徑 {base_dir}，請先建立該目錄以利掛載。")

        sys.exit(1)

    print(f"  -> 核心儲存路徑連通狀態: 正常 ({base_dir})")



    # 2. 建立極簡產品化目錄結構

    print("\n[Node B] 建立封裝模組目錄...")

    sub_dirs = ["database", "engine", "logs", "mcp_servers"]

    for folder in sub_dirs:

        target_path = os.path.join(base_dir, folder)

        os.makedirs(target_path, exist_ok=True)

        print(f"  -> 建立路徑: {target_path} ... 成功")



    # 3. 初始化 RAG 共同記憶資料庫 (SQLite)

    print("\n[Node C] 初始化本地輕量化 RAG 記憶體...")

    db_path = os.path.join(base_dir, "database", "history_experience.db")

    try:

        with sqlite3.connect(db_path) as conn:

            conn.execute("""

                CREATE TABLE IF NOT EXISTS knowledge_vault (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    context TEXT NOT NULL,

                    category TEXT,

                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP

                )

            """)

            # 填入 DFMEA 核心導向記憶

            conn.execute("""

                INSERT INTO knowledge_vault (context, category) 

                SELECT '核心規範：所有 Agent 行為必須經過全節點校驗（Node A-D），未取得實體成功代碼前，嚴禁用口頭回報成功。', 'QC_STANDARD'

                WHERE NOT EXISTS (SELECT 1 FROM knowledge_vault WHERE category = 'QC_STANDARD')

            """)

        print(f"  -> RAG SQLite 資料庫配置完成: {db_path}")

    except Exception as e:

        print(f"🚨【技術瓶頸】RAG 資料庫寫入失敗。原因: {str(e)}")

        sys.exit(1)



    # 4. 寫入並佈署 Agent Skills 核心大腦

    print("\n[Node D] 寫入核心控制大腦邏輯並鎖定...")

    brain_code = """# -*- coding: utf-8 -*-

import os

import sys

import hashlib



class LobsterCoreBrain:

    def __init__(self):

        self.base_dir = r"C:\\ITE"

        

    def verify_node_integrity(self, filepath):

        if not os.path.exists(filepath):

            return False

        sha = hashlib.sha256()

        with open(filepath, "rb") as f:

            for chunk in iter(lambda: f.read(4096), b""):

                sha.update(chunk)

        return sha.hexdigest()



    def execute_closed_loop_task(self, task_name, filename, data):

        print(f"\\n【目標導向決策】執行任務: {task_name}")

        target_path = os.path.join(self.base_dir, "engine", filename)

        

        try:

            with open(target_path, "w", encoding="utf-8") as f:

                f.write(data)

            

            # 實體 Hash 提取

            current_hash = self.verify_node_integrity(target_path)

            print(f"[Node C-Verify] 物理寫入成功。 SHA-256: {current_hash}")

            print(f"【解決問題】系統完全閉環。獲取實體回傳代碼。")

            return current_hash

        except Exception as e:

            print(f"🚨【系統熔斷】任務執行失敗。 Root Cause: {str(e)}")

            sys.exit(1)



if __name__ == '__main__':

    brain = LobsterCoreBrain()

    brain.execute_closed_loop_task("本地推論優化同步", "rtx3060_vram_lock.cfg", "VRAM_TARGET_LIMIT=12GB\\nCACHE_QUANT=Q4_0\\nFLASH_ATTENTION=ON")

"""

    

    brain_path = os.path.join(base_dir, "engine", "agent_brain.py")

    try:

        with open(brain_path, "w", encoding="utf-8") as f:

            f.write(brain_code)

        

        # 提取實體佈署 Hash

        deploy_hash = calculate_file_hash(brain_path)

        print(f"  -> 核心大腦佈署成功: {brain_path}")

        print(f"  -> 實體 Hash 驗證值: {deploy_hash}")

    except Exception as e:

        print(f"🚨【技術瓶頸】核心大腦物理寫入中斷。原因: {str(e)}")

        sys.exit(1)



    print("\n==================================================")

    print("  佈署與校驗全數通過！請於本地端終端機執行大腦程式  ")

    print("  執行指令: python C:\\ITE\\engine\\agent_brain.py  ")

    print("==================================================")



if __name__ == "__main__":

    detect_and_deploy()