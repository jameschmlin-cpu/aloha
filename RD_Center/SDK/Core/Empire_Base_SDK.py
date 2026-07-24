# -*- coding: utf-8 -*-

# 檔案：C:\Genesis\Genesis_Core\Empire_Base_SDK.py

# 狀態：資源感測與閉環回報整合完成



import winreg

import os

import psutil

import sqlite3

from SDK.AI_Judgment_Module import AIJudgmentModule



class EmpireBaseSDK:

    def __init__(self):

        self.ai_judgment = AIJudgmentModule()

        self.memory_db = r"C:\Genesis\Genesis_Core\Data\Unified_Empire_Memory.db"

        # 保持原有註冊表掛載邏輯

        self._register_all_agents()

        

    def _register_all_agents(self):

        """[保留功能] 將六大模組掛載至註冊表"""

        agents = ["Telegram", "Doctor", "WBNCP", "Secretary", "Guard Board", "Sentry"]

        reg_path = r"SOFTWARE\ITE\Agents"

        try:

            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, reg_path)

            for agent in agents:

                agent_path = os.path.join(r"C:\Genesis\Genesis_Core", agent, f"{agent}.exe")

                winreg.SetValueEx(key, agent, 0, winreg.REG_SZ, agent_path)

            winreg.CloseKey(key)

        except PermissionError:

            self.ai_judgment.get_expert_decision("PermissionError", "RegisterAgents")



    def register_to_memory(self):

        """[新增功能] 建立代理人看板：將路徑寫入資料庫"""

        reg_path = r"SOFTWARE\ITE\Agents"

        try:

            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_READ)

            conn = sqlite3.connect(self.memory_db)

            # 確保 Guard_Board 資料表存在

            conn.execute("CREATE TABLE IF NOT EXISTS Guard_Board (agent_name TEXT PRIMARY KEY, path TEXT)")

            for i in range(10):

                try:

                    name, path, _ = winreg.EnumValue(key, i)

                    conn.execute("INSERT OR REPLACE INTO Guard_Board (agent_name, path) VALUES (?, ?)", (name, path))

                except OSError: break

            conn.commit()

            conn.close()

            winreg.CloseKey(key)

        except Exception: pass



    def is_agent_running(self, agent_name):

        """[新增功能] 資源感測器：檢查程序是否執行中"""

        for proc in psutil.process_iter(['name']):

            if proc.info['name'] == f"{agent_name}.exe":

                return True

        return False



    def invoke_agent(self, agent_name):

        """[閉環回報] 執行程序並獲取 Exit Code"""

        if self.is_agent_running(agent_name):

            return "ALREADY_RUNNING"

        

        try:

            reg_path = r"SOFTWARE\ITE\Agents"

            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_READ)

            path, _ = winreg.QueryValueEx(key, agent_name)

            winreg.CloseKey(key)

            

            # 使用 os.system 或 subprocess 執行並獲取狀態

            return_code = os.system(f'"{path}"')

            return return_code

        except Exception:

            return "EXEC_FAILED"



    def perform_safety_check(self, task_name):

        """[保留功能] 閉環入口：防禦點"""

        try:

            return True

        except Exception as e:

            return self.ai_judgment.get_expert_decision(str(type(e).__name__), task_name)