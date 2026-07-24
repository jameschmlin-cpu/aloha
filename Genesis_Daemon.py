import time
from Gemini_Agent_Enhanced import GeminiAgentEnhanced

def run_genesis_daemon():
    agent = GeminiAgentEnhanced()
    print("[系統] 帝國自治引擎啟動中...")
    while True:
        # 1. 查詢資料庫是否有 PENDING 任務
        tasks = get_pending_tasks_from_db() # 需接上您的 SQLite
        for task in tasks:
            print(f"[節點] 偵測到新任務: {task['name']}")
            
            # 2. 自動呼叫您的 Agent (自動銜接)
            decision = agent.execute_free_instruction(task['name'], {"status": "AUTO_TRIGGER"})
            
            # 3. 自動執行決策 (核心橋接)
            if decision['decision'] == "EXECUTE_BRICK":
                execute_brick(decision['target_brick'], decision['patch_code'])
                mark_task_complete(task['id'])
        
        time.sleep(10) # 每 10 秒檢查一次，自動循環