# -*- coding: utf-8 -*-
# Genesis_AG_Master_Commander.py - 帝國自動化指揮核心
# 任務：全域自主作業、故障排除與自動調度
# 此模組作為 Genesis AG 之主腦，請置於 C:\Genesis\.agents\skills\empire_agents\

import os
import threading
import time
import importlib.util
import logging

logging.basicConfig(filename=r'C:\Genesis\system_monitor.log', level=logging.INFO)

class GenesisMasterCommander:
    def __init__(self):
        self.agent_dir = r"C:\Genesis\.agents\skills\empire_agents"
        self.cycle_time = 300 

    def start_orchestration(self):
        """啟動全域指揮鏈"""
        print("[主腦] 指揮鏈啟動，掃描所有可用代理...")
        for agent_file in os.listdir(self.agent_dir):
            if agent_file.endswith(".py") and "Master" not in agent_file:
                threading.Thread(target=self._monitor_agent, args=(agent_file,), daemon=True).start()
                logging.info(f"[主腦] 指揮鏈已掛載 Agent: {agent_file}")

    def _monitor_agent(self, filename):
        """循環執行與監控"""
        path = os.path.join(self.agent_dir, filename)
        while True:
            try:
                spec = importlib.util.spec_from_file_location(filename, path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, 'run'):
                    module.run()
            except Exception as e:
                logging.error(f"[主腦] Agent {filename} 故障，啟動自動重置: {e}")
            time.sleep(self.cycle_time)

if __name__ == "__main__":
    commander = GenesisMasterCommander()
    commander.start_orchestration()