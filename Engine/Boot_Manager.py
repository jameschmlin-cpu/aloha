# C:\Genesis\Engine\Boot_Manager.py (啟動管理總管)
import json
import psutil

class BootManager:
    def __init__(self):
        self.registry_path = r"C:\Genesis\Database\Startup_Registry.json"
        
    def check_system_load(self):
        """評估 CPU 與 RAM 負載，若過高則延遲掛載"""
        cpu = psutil.cpu_percent(interval=1)
        return cpu < 70  # 低於 70% 負載才允許掛載高耗能任務

    def process_startup(self):
        with open(self.registry_path, 'r') as f:
            tasks = json.load(f)
            
        for task, config in tasks.items():
            if config['priority'] == 'CRITICAL':
                # 高優先級：立即掛載
                self.launch(task)
            elif config['priority'] == 'ON_DEMAND' and self.check_system_load():
                # 低優先級：視系統負載動態掛載
                self.launch(task)

    def launch(self, task):
        print(f"[系統] 動態掛載: {task}")
        # 執行掛載指令