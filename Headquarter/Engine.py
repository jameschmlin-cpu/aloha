import os
import yaml
import sys
import shutil

class AutonomousEngine:
    def __init__(self, root_path=r"C:\Genesis"):
        self.root = root_path
        self.log_path = os.path.join(root_path, "system_monitor.log")
        self.setup_environment()

    def setup_environment(self):
        """初始化環境與檢查，自動化部署"""
        os.makedirs(os.path.join(self.root, "Headquarter"), exist_ok=True)

    def log(self, message, level="INFO"):
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(f"[{level}] {message}\n")
        print(f"[{level}] {message}")

    def self_heal(self, yaml_path, error):
        """故障排除與熔斷處理：自動處理異常"""
        self.log(f"Self-Healing Triggered for {yaml_path}: {error}", "CRITICAL")
        # 1. 執行熔斷：將錯誤檔案移至隔離區
        quarantine_dir = os.path.join(self.root, "Quarantine")
        os.makedirs(quarantine_dir, exist_ok=True)
        shutil.move(yaml_path, os.path.join(quarantine_dir, os.path.basename(yaml_path)))
        self.log("File moved to quarantine and system stabilized.", "INFO")

    def execute(self, yaml_path):
        """執行引擎：解析與自動化調度"""
        try:
            with open(yaml_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            # 驗證結構
            if not config or 'Action' not in config:
                raise ValueError("Invalid YAML Structure: Missing Action block")
            
            # 執行邏輯 (封裝至 Action.Logic)
            logic = config['Action'].get('Logic', 'Default')
            self.log(f"Executing Skill: {logic}...")
            
            # 此處為 Agent 調度區，若執行失敗觸發自癒
            return True
            
        except Exception as e:
            self.self_heal(yaml_path, str(e))
            return False

    def run_full_auto(self):
        """全自動掃描目錄執行"""
        targets = [r"C:\Genesis\Headquarter\Company_Assets", r"C:\Genesis\Library\Expert_Modules"]
        for target in targets:
            if not os.path.exists(target): continue
            for file in os.listdir(target):
                if file.endswith(".yaml"):
                    self.execute(os.path.join(target, file))

if __name__ == "__main__":
    # 全自動執行模式，無需人工介入
    engine = AutonomousEngine()
    engine.run_full_auto()
    sys.exit(0)