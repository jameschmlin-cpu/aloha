# -*- coding: utf-8 -*-
# 檔案位置: C:\Genesis\Library\Robust_Robot\Skill_Deployment_Agent.py
import sys
import requests
sys.path.append(r"C:\Genesis")

from Base_Template import Base_Template
from Library_Main import LibraryCore

class Skill_Deployment_Agent(Base_Template, LibraryCore):
    """【職能部署器】負責自動化下載雲端模型"""
    def __init__(self, brick_id="DEPLOYER_01"):
        Base_Template.__init__(self, brick_id=brick_id)
        LibraryCore.__init__(self, db_path=r"C:\Genesis\Library\LibOption\LibrarySystem\Shared_Knowledge.db")

    def deploy_skill(self, job_title, url):
        def task():
            response = requests.get(url)
            if response.status_code == 200:
                self.add_entry(job_title, response.text)
                return True
            return False
        return self.run_protected(stage_id="DEPLOY", task=task)