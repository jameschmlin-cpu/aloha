# -*- coding: utf-8 -*-
# 檔案位置: C:\Genesis\RD_Center\SDK_Bricks\Logic\Test_Deployment.py
# 執行此程式，將雲端職能模型正式同步到您的圖書館 (Shared_Knowledge.db)
import sys
import os

GENESIS_BASE = r"C:\Genesis"
if GENESIS_BASE not in sys.path:
    sys.path.insert(0, GENESIS_BASE)
sys.path.insert(0, os.path.join(GENESIS_BASE, "Library"))
sys.path.insert(0, os.path.join(GENESIS_BASE, "Library", "LibOption", "LibrarySystem"))
sys.path.insert(0, os.path.join(GENESIS_BASE, "RD_Center"))

from Rules.Orchestrator import Swarm_Orchestrator

def execute_deployment():
    # 1. 初始化指揮中心 (賦予它系統治理的 Brick ID)
    commander = Swarm_Orchestrator(brick_id="ROOT_COMMANDER_01")

    # 2. 定義雲端職能庫路徑 (這些模型已針對您的資料庫 Schema 完成規格化)
    talent_store = {
        "RND_Engineer": "https://genesis-cloud.ai/models/v1/RND_Engineer_Full.json",
        "QC_Specialist": "https://genesis-cloud.ai/models/v1/QC_Specialist_Full.json"
    }

    # 3. 觸發下載與部署
    print("[系統] 開始同步人才職能模型...")
    for job, url in talent_store.items():
        # 使用 run_scenario 執行同步，若 DB 無資料，指揮官會自動調用下載器
        result = commander.run_scenario(job, download_url=url)
        print(f"[報告] 職能部署狀態: {result}")

if __name__ == "__main__":
    execute_deployment()
