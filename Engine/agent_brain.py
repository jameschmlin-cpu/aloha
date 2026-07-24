# -*- coding: utf-8 -*-

import os

import sys

import hashlib



class LobsterCoreBrain:

    def __init__(self):

        self.base_dir = r"C:\ITE"

        

    def verify_node_integrity(self, filepath):

        if not os.path.exists(filepath):

            return False

        sha = hashlib.sha256()

        with open(filepath, "rb") as f:

            for chunk in iter(lambda: f.read(4096), b""):

                sha.update(chunk)

        return sha.hexdigest()



    def execute_closed_loop_task(self, task_name, filename, data):

        print(f"\n【目標導向決策】執行任務: {task_name}")

        target_path = os.path.join(self.base_dir, "engine", filename)

        

        try:

            with open(target_path, "w", encoding="utf-8") as f:

                f.write(data)

            

            # 實體 Hash 提取

            current_hash = self.verify_node_integrity(target_path)

            print(f"[Node C-Verify] 物理寫入成功。 SHA-256: {current_hash}")

            print("【解決問題】系統完全閉環。獲取實體回傳代碼。")

            return current_hash

        except Exception as e:

            print(f"🚨【系統熔斷】任務執行失敗。 Root Cause: {str(e)}")

            sys.exit(1)



if __name__ == '__main__':

    brain = LobsterCoreBrain()

    brain.execute_closed_loop_task("本地推論優化同步", "rtx3060_vram_lock.cfg", "VRAM_TARGET_LIMIT=12GB\nCACHE_QUANT=Q4_0\nFLASH_ATTENTION=ON")

