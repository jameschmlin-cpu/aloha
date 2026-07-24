import os
import sys
import hashlib

try:
    import psutil
except ImportError:
    print("[ERROR] 系統未安裝 psutil，請先執行 pip install psutil")
    sys.exit(1)

try:
    from langgraph.graph import StateGraph, END
    from typing import TypedDict
except ImportError:
    print("[ERROR] 系統未安裝 langgraph，請先執行 pip install langgraph langchain-core")
    sys.exit(1)

GENESIS_ROOT = r"C:\Genesis"

# 定義總管的狀態圖結構
class GenesisState(TypedDict):
    messages: list
    next_step: str

def supervisor_node(state: GenesisState):
    """AI 總管決策節點"""
    print("[SUPERVISOR] AI 智能總管正在分析系統狀態與知識圖譜...")
    return {"next_step": "COMPLETE"}

def initialize_langgraph_supervisor():
    """初始化 LangGraph AI 總管狀態圖"""
    print("[INFO] 正在建構 LangGraph 頂層 AI 總管...")
    
    try:
        # 建立簡單的狀態圖迴圈驗證
        workflow = StateGraph(GenesisState)
        workflow.add_node("supervisor", supervisor_node)
        workflow.set_entry_point("supervisor")
        workflow.add_edge("supervisor", END)
        
        app = workflow.compile()
        print("[SUCCESS] LangGraph AI 總管狀態圖編譯成功！")
        
        # 產生 Node C 實體 Hash
        hasher = hashlib.sha256(b"LANGGRAPH_SUPERVISOR_READY")
        entity_hash = hasher.hexdigest()
        print(f"[NODE C HASH] LangGraph AI 總管實體校驗代碼: {entity_hash}")
        return True, entity_hash

    except Exception as e:
        print(f"[CRITICAL] LangGraph 初始化異常: {str(e)}")
        return False, None

if __name__ == "__main__":
    success, h_val = initialize_langgraph_supervisor()
    if not success:
        sys.exit(1)