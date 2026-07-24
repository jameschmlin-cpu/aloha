# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\RD_Center\SDK\System\LangGraph_Core.py
# 狀態：LangGraph AI 總管核心大腦 (完整實體版)
# 實體 Hash: 0xGEN-LANGGRAPH-CORE-V2

import os
import sys
import json
import time
import sqlite3
import datetime
from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END

# Prepend paths for relative imports
GENESIS_BASE = r"C:\Genesis"
sys.path.insert(0, os.path.join(GENESIS_BASE, "RD_Center", "SDK", "System"))
sys.path.insert(0, os.path.join(GENESIS_BASE, "RD_Center", "SDK", "AI_Core"))

from LightRAG_Engine import GenesisLightRAGEngine
from Gemini_Agent import GeminiAgent

LOG_FILE = os.path.join(GENESIS_BASE, "Logs", "LangGraph_Core.log")
DB_PATH = os.path.join(GENESIS_BASE, "Database", "Genesis_DFMEA.db")

def log_msg(msg):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] [LangGraph Core] {msg}"
    print(entry)
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry + "\n")

# 定義 LangGraph 狀態
class GenesisState(TypedDict):
    instruction: str
    context: str
    decision: Dict[str, Any]
    task_id: str
    status: str

# 1. 檢索節點：查詢 LightRAG 雙層知識圖譜
def retrieve_knowledge(state: GenesisState) -> Dict[str, Any]:
    log_msg("[Brain Node: Retrieve] 正在向 LightRAG 檢索引擎查詢相關上下文...")
    try:
        engine = GenesisLightRAGEngine()
        # 進行 hybrid 混合檢索
        retrieved_context = engine.query(state["instruction"], mode="hybrid")
        if not retrieved_context or retrieved_context == "None":
            retrieved_context = "無直接相關知識圖譜記錄。"
        log_msg(f"[Brain Node: Retrieve] 成功檢索到 {len(retrieved_context)} 字元之圖譜上下文。")
    except Exception as e:
        log_msg(f"[警告] 檢索圖譜失敗: {e}")
        retrieved_context = "圖譜檢索異常。"
        
    return {"context": retrieved_context}

# 2. 決策節點：呼叫 GeminiAgent 進行分流決策
def make_decision(state: GenesisState) -> Dict[str, Any]:
    log_msg("[Brain Node: Decision] 正在呼叫 GeminiAgent 執行決策生成...")
    agent = GeminiAgent()
    telemetry_ctx = {
        "timestamp": datetime.datetime.now().isoformat(),
        "rag_knowledge": state["context"]
    }
    # 執行自然語言指令解析與決策
    decision = agent.execute_free_instruction(state["instruction"], telemetry_context=telemetry_ctx)
    log_msg(f"[Brain Node: Decision] 產出決策類別: {decision.get('response_type', 'TEXT')}，決策目標: {decision.get('target_brick', 'None')}")
    return {"decision": decision}

# 3. 執行節點：寫入 SQLite 同步表並等待 Sync Daemon (TDD 剛性檢驗)
def execute_and_verify(state: GenesisState) -> Dict[str, Any]:
    decision = state["decision"]
    if decision.get("response_type") != "ACTION" or not decision.get("patch_code"):
        log_msg("[Brain Node: Execute] 無須物理寫入/修補代碼，決策為單純對話回覆。")
        return {"status": "SUCCESS"}
        
    brick_name = decision.get("target_brick", "")
    if not brick_name.endswith(".py"):
        brick_name += ".py"
        
    task_id = "langgraph_task_" + str(int(time.time()))
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    instruction_payload = json.dumps({
        "brick": brick_name,
        "code": decision["patch_code"]
    })
    
    log_msg(f"[Brain Node: Execute] 偵測到 ACTION 代碼修補任務，物理註冊同步任務: {task_id} -> {brick_name}")
    
    try:
        # 寫入 SQLite 等待 Sync Daemon 自癒監控編譯
        conn = sqlite3.connect(DB_PATH, timeout=5.0)
        conn.execute("PRAGMA journal_mode=WAL;")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Sync_Control_Table (task_id, instruction, status, last_hash, timestamp)
            VALUES (?, ?, 'PENDING', '', ?)
        """, (task_id, instruction_payload, timestamp))
        conn.commit()
        conn.close()
        
        # 等待同步守護進程處理 (等待 TDD 驗證)
        log_msg("[Brain Node: Execute] 任務已註冊，等待 Genesis_Sync_Daemon 執行 Ruff、編譯與 TDD 驗證...")
        
        # 輪詢狀態
        max_wait = 20 # 最多等待 20 秒
        task_status = "PENDING"
        for _ in range(max_wait):
            time.sleep(1)
            conn = sqlite3.connect(DB_PATH, timeout=5.0)
            cursor = conn.cursor()
            cursor.execute("SELECT status FROM Sync_Control_Table WHERE task_id = ?", (task_id,))
            row = cursor.fetchone()
            conn.close()
            if row:
                task_status = row[0]
                if task_status in ["COMPLETED", "FAILED", "MELTDOWN", "REJECTED"]:
                    break
                    
        log_msg(f"[Brain Node: Execute] TDD 閉環驗證完成，最終任務狀態: {task_status}")
        return {"task_id": task_id, "status": task_status}
        
    except Exception as e:
        log_msg(f"[❌] 註冊同步任務失敗: {e}")
        return {"status": "ERROR"}

class GenesisLangGraphBrain:
    def __init__(self):
        # 建立狀態圖
        workflow = StateGraph(GenesisState)
        
        # 加入節點
        workflow.add_node("retrieve", retrieve_knowledge)
        workflow.add_node("decide", make_decision)
        workflow.add_node("execute", execute_and_verify)
        
        # 設定進入點與連線
        workflow.set_entry_point("retrieve")
        workflow.add_edge("retrieve", "decide")
        workflow.add_edge("decide", "execute")
        workflow.add_edge("execute", END)
        
        self.app = workflow.compile()
        
    def execute_flow(self, user_instruction: str) -> Dict[str, Any]:
        log_msg(f"=== [LangGraph] 啟動全局控制迴圈，指令: {user_instruction} ===")
        initial_state = {
            "instruction": user_instruction,
            "context": "",
            "decision": {},
            "task_id": "",
            "status": ""
        }
        final_state = self.app.invoke(initial_state)
        log_msg("=== [LangGraph] 全局控制迴圈執行結束 ===")
        return final_state

if __name__ == "__main__":
    brain = GenesisLangGraphBrain()
    # 支援指令列執行測試
    test_instruction = sys.argv[1] if len(sys.argv) > 1 else "系統初始化自癒檢測"
    res = brain.execute_flow(test_instruction)
    print(f"\n[LangGraph 執行結果]:\n{json.dumps(res, indent=4, ensure_ascii=False)}")