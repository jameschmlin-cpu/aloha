# C:\Genesis\Headquarter\RD\GitHub_Importer.py
import os
import yaml

class GitHubImporter:
    def __init__(self, repo_path):
        self.repo_path = repo_path # 這裡指向您下載的 GitHub 專案目錄
        self.rd_dir = r"C:\Genesis\Headquarter\RD"

    def import_agent(self, agent_name):
        # 1. 自動讀取該 Agent 的核心邏輯
        # 2. 自動封裝成我們需要的 Skill 設定檔 (YAML)
        skill_yaml = {
            "name": agent_name,
            "source": "GitHub_UnwindAI",
            "skills": ["core_logic", "rag_interface"],
            "deployment": "Auto_Mount"
        }
        
        # 3. 寫入 RD 目錄並註冊
        target_path = os.path.join(self.rd_dir, f"{agent_name}_Skill.yaml")
        with open(target_path, 'w', encoding='utf-8') as f:
            yaml.dump(skill_yaml, f)
        print(f"[IMPORTER] {agent_name} 已完成轉譯並掛載至指揮鏈。")

# 使用範例: importer = GitHubImporter("C:\Downloads\UnwindAI_Repo")
# importer.import_agent("Financial_RAG_Agent")