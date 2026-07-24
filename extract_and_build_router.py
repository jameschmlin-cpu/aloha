# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\extract_and_build_router.py
# 狀態：修復 AST 解析錯誤的修正版
# 實體 Hash: 0xGEN-CODE-EXTRACTOR-V2

import os
import sys
import ast
import hashlib

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(errors='replace')

GENESIS_BASE = r"C:\Genesis"
OUTPUT_ROUTER_FILE = os.path.join(GENESIS_BASE, "Management_Hub", "selector_routing_table.py")

def extract_logic_from_file(filepath):
    if not os.path.exists(filepath):
        return {"status": "missing", "functions": [], "triggers": []}
        
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            
        tree = ast.parse(content)
        functions = []
        triggers = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_name = node.name
                functions.append(func_name)
                
                # 嘗試將函式內容還原為字串來安全檢索關鍵字
                try:
                    func_code = ast.unparse(node).lower()
                except:
                    func_code = func_name.lower()
                    
                if "memory" in func_code or "percent" in func_code or "governor" in func_code:
                    triggers.append("memory_threshold")
                if "file" in func_code or "watch" in func_code or "path" in func_code:
                    triggers.append("file_event")
                if "error" in func_code or "log" in func_code or "doctor" in func_code:
                    triggers.append("error_log")
                if "graph" in func_code or "rag" in func_code or "agent" in func_code:
                    triggers.append("heavy_task")
                    
        return {
            "status": "success",
            "functions": functions,
            "triggers": list(set(triggers)) if triggers else ["ondemand_default"]
        }
    except Exception as e:
        return {"status": "error", "message": str(e), "functions": [], "triggers": ["ondemand_default"]}

def scan_and_build_router():
    print("=== [程式碼萃取器 V2] 重新掃描並修正 AST 解析 ===")
    
    targets = {
        "empire_governor": os.path.join(GENESIS_BASE, "Management_Hub", "Empire_Resource_Governor.py"),
        "memory_guard": os.path.join(GENESIS_BASE, "Management_Hub", "Memory_Guardian.py"),
        "memory_sync_guard": os.path.join(GENESIS_BASE, "Management_Hub", "Memory_Sync_Guard.py"),
        "file_watcher": os.path.join(GENESIS_BASE, "Engine", "Watcher.py"),
        "doctor_guard": os.path.join(GENESIS_BASE, "Management_Hub", "Doctor.py"),
        "command_dispatcher": os.path.join(GENESIS_BASE, "RD_Center", "SDK", "System", "Command_Dispatcher.py"),
        "genesis_sync_daemon": os.path.join(GENESIS_BASE, "Genesis_Sync_Daemon.py"),
        "log_health_monitor": os.path.join(GENESIS_BASE, "Management_Hub", "Log_Health_Monitor.py"),
        "qc_watcher": os.path.join(GENESIS_BASE, "Management_Hub", "QC_Watcher.py"),
        "closed_loop_optimizer": os.path.join(GENESIS_BASE, "genesis_closed_loop_optimizer.py"),
        "safety_referee": os.path.join(GENESIS_BASE, "genesis_safety_referee.py"),
        "langgraph_core": os.path.join(GENESIS_BASE, "RD_Center", "SDK", "System", "LangGraph_Core.py"),
        "lightrag_engine": os.path.join(GENESIS_BASE, "RD_Center", "SDK", "System", "LightRAG_Engine.py")
    }
    
    routing_table = {}
    
    for key, path in targets.items():
        print(f"  [分析中] 正在剖析: {key}")
        analysis = extract_logic_from_file(path)
        routing_table[key] = {
            "path": path,
            "analysis": analysis
        }
        print(f"    -> 狀態: {analysis['status']} | 偵測到觸發條件: {analysis['triggers']}")

    router_code = f"""# -*- coding: utf-8 -*-
# 自動生成的條件路由對應表（由 extract_and_build_router.py V2 產出）
# 實體 Hash: {hashlib.sha256(str(routing_table).encode('utf-8')).hexdigest()[:16]}

DYNAMIC_ROUTING_TABLE = {routing_table!r}
"""
    
    os.makedirs(os.path.dirname(OUTPUT_ROUTER_FILE), exist_ok=True)
    with open(OUTPUT_ROUTER_FILE, "w", encoding="utf-8") as f:
        f.write(router_code)
        
    print(f"=== [萃取完成] 成功修復並產出路由表至: {OUTPUT_ROUTER_FILE} ===")

if __name__ == "__main__":
    scan_and_build_router()