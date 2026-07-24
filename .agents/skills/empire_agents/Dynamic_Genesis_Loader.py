# -*- coding: utf-8 -*-
# Dynamic_Genesis_Loader.py - Genesis AG Dynamic Skill Loader
# 任務：實現雲端技能動態部署，移除人工掛載流程
import os
import requests
import importlib.util
import logging

logging.basicConfig(filename=r'C:\Genesis\system_monitor.log', level=logging.INFO)

class DynamicOrchestrator:
    def __init__(self):
        self.repo_url = "https://cloud.genesis.empire/api/v1/skills"
        self.local_dir = r"C:\Genesis\.agents\dynamic_loader"

    def fetch_skill(self, skill_name):
        """從雲端自動拉取技能代碼"""
        print(f"[動態部署] 正在從雲端同步: {skill_name}...")
        try:
            response = requests.get(f"{self.repo_url}/{skill_name}")
            if response.status_code == 200:
                code = response.text
                file_path = os.path.join(self.local_dir, f"{skill_name}.py")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(code)
                logging.info(f"[部署成功] 技能 {skill_name} 已掛載。")
                self.load_module(skill_name, file_path)
        except Exception as e:
            logging.error(f"[部署失敗] {skill_name}: {e}")

    def load_module(self, name, path):
        """動態掛載模組至執行進程"""
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        print(f"[系統啟用] {name} 模組已即時掛載。")

if __name__ == "__main__":
    loader = DynamicOrchestrator()
    # 自動偵測並部署
    loader.fetch_skill("Analyst_Agent")
    print("[執行完畢] Genesis 雲端技能橋接已建立，無須人工介入。")