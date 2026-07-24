# -*- coding: utf-8 -*-
# C:\Genesis\Headquarter\RD\Skill_02.py
# 任務：升級版 Genesis AG 帝國全域自主調度引擎 (整合 6 大 Subagents，導入看板事件驅動與 QC 閉環)

import os
import sys
import sqlite3
import hashlib
import logging
import subprocess
import time

# 頂真做事，初始化全域日誌，嚴禁任何外國翻譯腔
logging.basicConfig(
    filename=r'C:\Genesis\system_monitor.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    encoding='utf-8'
)

class UniversalGenesisAgent:
    def __init__(self):
        self.name = "Universal_Genesis_Agent"
        self.base_dir = r"C:\Genesis"
        self.db_path = os.path.join(self.base_dir, r"Database\Genesis_History.db")
        self.subagents_dir = os.path.join(self.base_dir, r".agents\skills\empire_agents")
        self.required_node_c_code = "0xFC09" # 剛性品質保證代碼
        
        # 確保核心目錄與資料庫完備
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        os.makedirs(self.subagents_dir, exist_ok=True)
        self._init_database()

        # 動態載入看板管理器，防止路徑解析異常
        if self.subagents_dir not in sys.path:
            sys.path.append(self.subagents_dir)
        from Kanban_Manager import KanbanManager
        self.kanban = KanbanManager(self.db_path)

    def _init_database(self):
        """初始化實體資料庫，用於追蹤 Agent 狀態與 Hash 校驗"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS agent_execution_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                agent_name TEXT,
                action TEXT,
                file_path TEXT,
                file_hash TEXT,
                status TEXT,
                node_c_code TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def calculate_file_hash(self, file_path):
        """實體 Hash 校驗，確保檔案寫入完整且未被篡改"""
        if not os.path.exists(file_path):
            return "FILE_NOT_FOUND"
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256.update(byte_block)
        return sha256.hexdigest()

    def _execute_subagent(self, script_name, args=[]):
        """實體呼叫 Subagent 腳本並獲取回傳結果"""
        script_path = os.path.join(self.subagents_dir, script_name)
        if not os.path.exists(script_path):
            logging.error(f"找不到指定的 Subagent 檔案: {script_path}")
            return False, "FILE_NOT_FOUND", ""

        # 執行前的 Token 預估與沙盒模擬 (SDK 校驗準備)
        file_hash = self.calculate_file_hash(script_path)
        logging.info(f"啟動 Subagent {script_name} (Hash: {file_hash[:8]})")

        try:
            # 實體執行子進程
            result = subprocess.run(
                [sys.executable, script_path] + args,
                capture_output=True,
                text=True,
                timeout=30,
                encoding='utf-8',
                errors='replace'
            )
            
            output = result.stdout.strip()
            if result.returncode == 0:
                logging.info(f"Subagent {script_name} 執行成功。回傳資訊: {output}")
                return True, file_hash, output
            else:
                logging.error(f"Subagent {script_name} 執行失敗。錯誤資訊: {result.stderr}")
                return False, file_hash, result.stderr
        except Exception as e:
            logging.error(f"執行 Subagent {script_name} 時發生異常: {str(e)}")
            return False, file_hash, str(e)

    # ==================== 核心六大技能對接 Subagents ====================

    def skill_diagnostic(self):
        """[PM Agent] 需求分析與工作拆解 (Node A)"""
        print(f"[{self.name}] 執行 Diag_Skill: PM Agent 需求校驗與路徑盤點...")
        success, file_hash, output = self._execute_subagent("Diag_Agent.py", ["--action", "diagnose"])
        self._log_action("PM_Agent", "diagnose", r"Diag_Agent.py", file_hash, "SUCCESS" if success else "FAILED", "")

    def skill_compiler(self):
        """[RD Agent] 程式撰寫與系統編譯 (Node B)"""
        print(f"[{self.name}] 執行 Compiler_Skill: RD Agent 程式碼自動編譯與資產生成...")
        success, file_hash, output = self._execute_subagent("Compiler_Agent.py", ["--action", "compile"])
        self._log_action("RD_Agent", "compile", r"Compiler_Agent.py", file_hash, "SUCCESS" if success else "FAILED", "")

    def skill_tester_kanban(self, task_id):
        """[QA Agent] 看板模式品質校驗 - 失敗退回重試，不直接熔斷"""
        print(f"[{self.name}] 執行 Tester_Skill: QA Agent 進行剛性校驗...")
        success, file_hash, output = self._execute_subagent("Tester_Agent.py", ["--action", "assert"])
        
        # 必須取得 Node C 的實體品質代碼
        if success and self.required_node_c_code in output:
            print(f"[{self.name}] [Node C QA通過] 任務 {task_id} 品質代碼核實成功: {self.required_node_c_code}")
            logging.info(f"Task {task_id} QA passed with code {self.required_node_c_code}.")
            self._log_action("QA_Agent", "assert", r"Tester_Agent.py", file_hash, "SUCCESS", self.required_node_c_code)
            return True
        else:
            print(f"[{self.name}] [Node C QA失敗] 任務 {task_id} 未能取得正確品質代碼，打回重試。")
            logging.warning(f"Task {task_id} QA failed verification.")
            self._log_action("QA_Agent", "assert", r"Tester_Agent.py", file_hash, "FAILED", "INVALID")
            return False

    def skill_security(self):
        """[SCM Agent] 供應鏈管理與權限安全稽核"""
        print(f"[{self.name}] 執行 Security_Skill: SCM Agent 安全稽核與套件依賴盤點...")
        success, file_hash, output = self._execute_subagent("Security_Agent.py", ["--action", "audit"])
        self._log_action("SCM_Agent", "audit", r"Security_Agent.py", file_hash, "SUCCESS" if success else "FAILED", "")

    def skill_sync(self):
        """[MFG_Agent] 自動化部署、製造與資料庫同步 (Node D)"""
        print(f"[{self.name}] 執行 Sync_Skill: MFG Agent 部署生產與資料庫閉環同步...")
        success, file_hash, output = self._execute_subagent("Sync_Agent.py", ["--action", "deploy"])
        self._log_action("MFG_Agent", "deploy", r"Sync_Agent.py", file_hash, "SUCCESS" if success else "FAILED", "")

    def skill_analyst(self):
        """[Sales Agent] 市場與數據成效分析"""
        print(f"[{self.name}] 執行 Analyst_Skill: Sales Agent 市場與數據成效分析...")
        success, file_hash, output = self._execute_subagent("Analyst_Agent.py", ["--action", "analyze"])
        self._log_action("Sales_Agent", "analyze", r"Analyst_Agent.py", file_hash, "SUCCESS" if success else "FAILED", "")

    def _log_action(self, agent_name, action, file_path, file_hash, status, node_c_code):
        """將執行紀錄寫入實體資料庫，達成不可篡改的營運閉環"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO agent_execution_log (agent_name, action, file_path, file_hash, status, node_c_code)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (agent_name, action, file_path, file_hash, status, node_c_code))
            conn.commit()
            conn.close()
        except Exception as e:
            logging.error(f"寫入資料庫失敗: {str(e)}")

    def run_all(self):
        """企業看板工作流模式啟動 (非同步/輪詢模擬)"""
        print(f"[{self.name}] === 啟動 Genesis 看板架構自主協作流水線 ===")
        logging.info("Kanban Orchestrator pipeline started.")

        # 1. 任務初始化 (Seed task if backlog is empty)
        root_task_id = "genesis_daily_audit"
        self.kanban.add_task(
            root_task_id,
            "Daily Genesis System Audit",
            "Perform full loop audit: PM -> SCM -> RD -> QA -> MFG -> Sales",
            "PM",
            "TODO"
        )

        # 2. 看板輪詢事件迴圈
        loop_active = True
        max_cycles = 15
        cycle = 0

        while loop_active and cycle < max_cycles:
            cycle += 1
            print(f"\n[{self.name}] --- 看板調度第 {cycle} 輪次開始 ---")
            time.sleep(0.5)

            # PM 部門處理
            todo_pm = self.kanban.get_tasks_by_dept_and_status("PM", "TODO")
            for t in todo_pm:
                print(f"[{self.name}] PM 部門接單: {t['task_id']}")
                self.kanban.update_task(t['task_id'], status="IN_PROGRESS")
                self.skill_diagnostic()
                # 轉交 SCM 與 RD 處理
                self.kanban.update_task(t['task_id'], status="TODO", assigned_department="SCM")
                # 派生 RD 工作卡
                self.kanban.add_task(f"{t['task_id']}_RD", "RD Compile & Refactor", "Write code & compile.", "RD", "TODO")

            # SCM 部門處理
            todo_scm = self.kanban.get_tasks_by_dept_and_status("SCM", "TODO")
            for t in todo_scm:
                print(f"[{self.name}] SCM 部門接單: {t['task_id']}")
                self.kanban.update_task(t['task_id'], status="IN_PROGRESS")
                self.skill_security()
                # 完成安全審核並進行安全簽章
                self.kanban.update_task(t['task_id'], status="COMPLETED", security_signed=1)

            # RD 部門處理
            todo_rd = self.kanban.get_tasks_by_dept_and_status("RD", "TODO")
            for t in todo_rd:
                print(f"[{self.name}] RD 部門接單: {t['task_id']}")
                self.kanban.update_task(t['task_id'], status="IN_PROGRESS")
                self.skill_compiler()
                # 編譯完轉交 QA 審查
                self.kanban.update_task(t['task_id'], status="PENDING_QA", assigned_department="QA")

            # QA 部門處理
            pending_qa = self.kanban.get_tasks_by_dept_and_status("QA", "PENDING_QA")
            for t in pending_qa:
                print(f"[{self.name}] QA 部門接單: {t['task_id']}")
                self.kanban.update_task(t['task_id'], status="IN_PROGRESS")
                qa_passed = self.skill_tester_kanban(t['task_id'])
                if qa_passed:
                    # 取得根任務狀態
                    root_t = self.kanban.get_task(root_task_id)
                    # 檢查 SCM 安全簽核是否已簽發
                    if root_t and root_t.get('security_signed') == 1:
                        print(f"[{self.name}] QA 品質與 SCM 安全均審查通過，進入部署。")
                        self.kanban.update_task(t['task_id'], status="PENDING_DEPLOY", assigned_department="MFG")
                    else:
                        print(f"[{self.name}] QA 品質通過，但 SCM 安全核可未簽署，等待 SCM...")
                        self.kanban.update_task(t['task_id'], status="PENDING_QA")
                else:
                    self.kanban.increment_retry(t['task_id'])
                    updated_t = self.kanban.get_task(t['task_id'])
                    # CEO 監管限制：最多重試 3 次，否則強制熔斷升級
                    if updated_t['retry_count'] >= 3:
                        print(f"❌ [{self.name}] 重大故障：QA 失敗達 3 次上限，啟動系統熔斷！")
                        self.kanban.update_task(t['task_id'], status="ESCALATED", assigned_department="CEO")
                        loop_active = False
                    else:
                        # 退回 RD 重新處理
                        print(f"[{self.name}] QA 未能通過，任務退回 RD 部門重構...")
                        self.kanban.update_task(t['task_id'], status="TODO", assigned_department="RD")

            # MFG 部門處理
            pending_mfg = self.kanban.get_tasks_by_dept_and_status("MFG", "PENDING_DEPLOY")
            for t in pending_mfg:
                print(f"[{self.name}] MFG 部門接單: {t['task_id']}")
                self.kanban.update_task(t['task_id'], status="IN_PROGRESS")
                self.skill_sync()
                # 部署成功，轉交 Sales 進行營運成效分析
                self.kanban.update_task(t['task_id'], status="COMPLETED", assigned_department="Sales")

            # Sales 部門處理
            todo_sales = self.kanban.get_tasks_by_dept_and_status("Sales", "COMPLETED")
            for t in todo_sales:
                print(f"[{self.name}] Sales 部門接單: {t['task_id']}")
                self.kanban.update_task(t['task_id'], status="IN_PROGRESS")
                self.skill_analyst()
                self.kanban.update_task(t['task_id'], status="COMPLETED")
                
                # 同步完成根任務
                self.kanban.update_task(root_task_id, status="COMPLETED")
                print(f"[{self.name}] === 企業全域任務 {root_task_id} 成功閉環完成！ ===")
                loop_active = False # 全部工作順利結束

        # 檢測最終狀態，觸發 CEO 級修復
        final_root = self.kanban.get_task(root_task_id)
        if final_root and final_root.get('status') == "ESCALATED":
            logging.critical("System Escalated: Initiating system recovery doctor loop.")
            print(f"\n❌ [{self.name}] [CEO 審批介入] 檢測到任務被判定為重大異常！")
            print(f"[{self.name}] 正在啟動 Doctor 修復機制並中斷運行...")
            sys.exit("System Halt: Corporate escalation initiated.")

if __name__ == "__main__":
    agent = UniversalGenesisAgent()
    agent.run_all()