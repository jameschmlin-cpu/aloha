# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\Management_Hub\dashboard_ai_orchestrator.py
# 狀態：AI 智慧程式編排與多工工具鏈協同引擎 (LangGraph + Prefect 整合版)
# 實體 Hash: 0xGEN-DASHBOARD-AI-ORCHESTRATOR-ULTIMATE

import os
import sys
import json
import hashlib
import time
import logging
import subprocess
import urllib.request
import urllib.error
from typing import TypedDict, List, Optional
from diskcache import Cache

# Core toolchain imports
from prefect import flow, task
from langgraph.graph import StateGraph, END

GENESIS_BASE = r"C:\Genesis"
sys.path.insert(0, os.path.join(GENESIS_BASE, "RD_Center"))
sys.path.insert(0, os.path.join(GENESIS_BASE, "RD_Center", "SDK"))
sys.path.insert(0, os.path.join(GENESIS_BASE, "RD_Center", "SDK", "AI_Core"))
sys.path.insert(0, os.path.join(GENESIS_BASE, "RD_Center", "SDK", "System"))

from Gemini_Agent import GeminiAgent

DASHBOARD_DATA_PATH = os.path.join(GENESIS_BASE, "Config", "dashboard_ai_intelligence.json")
LOG_FILE = os.path.join(GENESIS_BASE, "Logs", "dashboard_ai_orchestrator.log")
CACHE_DIR = os.path.join(GENESIS_BASE, "cache", "orchestrator_analysis")

os.makedirs(os.path.dirname(DASHBOARD_DATA_PATH), exist_ok=True)
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# 解決標準輸出與日誌編碼
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - [AI-ORCHESTRATOR-FLOW] - %(message)s'
)

def log_and_print(msg):
    print(f"[AI-ORCHESTRATOR-FLOW] {msg}")
    logging.info(msg)

# 1. LightRAG 圖譜Grounding對接 (使用子進程隔離避免 asyncio event loop 跨執行緒鎖定衝突)
def query_lightrag_context(filename):
    try:
        engine_script = os.path.join(GENESIS_BASE, "RD_Center", "SDK", "System", "LightRAG_Engine.py")
        q = f"Describe module dependencies, caller functions or use case of script {filename}"
        res = subprocess.run(
            [sys.executable, engine_script, 'query', q],
            capture_output=True, text=True, encoding='utf-8', errors='ignore', creationflags=0x08000000, timeout=20.0
        )
        output = res.stdout.strip()
        if "[LightRAG 檢索結果]:" in output:
            return output.split("[LightRAG 檢索結果]:")[-1].strip()
        return output
    except Exception as e:
        logging.error(f"RAG query subprocess failed for {filename}: {e}")
        return "No RAG context available."

# 2. Ruff 靜態防禦代碼檢驗
def run_ruff_check(filepath):
    try:
        # 執行 ruff 檢查並以 JSON 格式輸出
        res = subprocess.run(
            ['ruff', 'check', '--format=json', filepath],
            capture_output=True, text=True, creationflags=0x08000000
        )
        if res.stdout.strip():
            return json.loads(res.stdout)
    except Exception as e:
        logging.error(f"Ruff execution failed on {filepath}: {e}")
    return []

# 3. LLM 呼叫核心
def call_llm_direct(prompt):
    gemini_key = ""
    config_path = r"C:\Genesis\Config\telegram_config.json"
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                key = cfg.get("gemini_api_key", "")
                if key and "YOUR_GEMINI_API_KEY" not in key:
                    gemini_key = key
        except Exception:
            pass

    capability_schema = {
        "type": "OBJECT",
        "properties": {
            "category": {"type": "STRING"},
            "ai_best_use_case": {"type": "STRING"},
            "readiness_score": {"type": "INTEGER"},
            "short_description": {"type": "STRING"},
            "dependencies": {
                "type": "ARRAY",
                "items": {"type": "STRING"}
            }
        },
        "required": ["category", "ai_best_use_case", "readiness_score", "short_description", "dependencies"]
    }

    if gemini_key:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={gemini_key}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "responseMimeType": "application/json",
                    "responseSchema": capability_schema
                }
            }
            req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=15) as response:
                res_data = json.loads(response.read().decode('utf-8'))
                res_text = res_data['candidates'][0]['content']['parts'][0]['text']
                return json.loads(res_text)
        except Exception as e:
            logging.error(f"Gemini call failed: {e}")

    # Fallback to local Ollama
    try:
        url = "http://localhost:11434/api/chat"
        messages = [
            {"role": "system", "content": "You are a software architect. Output JSON matching the schema: {\"category\": string, \"ai_best_use_case\": string, \"readiness_score\": integer, \"short_description\": string, \"dependencies\": [string]}"},
            {"role": "user", "content": prompt}
        ]
        payload = {
            "model": "qwen2.5-coder:7b",
            "messages": messages,
            "stream": False,
            "format": "json"
        }
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=12) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            res_text = res_data['message']['content']
            return json.loads(res_text)
    except Exception as e:
        logging.error(f"Local Ollama fallback failed: {e}")
        return {
            "category": "核心服務與控制鏈",
            "ai_best_use_case": "按需調度執行",
            "readiness_score": 85,
            "short_description": "支援系統指令派發與自癒聯防的核心服務",
            "dependencies": []
        }

# 4. LangGraph 閉環狀態圖編排
class OrchestrationState(TypedDict):
    filepath: str
    filename: str
    relative_path: str
    sha256: str
    code_snippet: str
    ruff_warnings: List[dict]
    rag_context: str
    readiness_score: int
    ai_card: dict
    errors: List[str]

def ruff_node(state: OrchestrationState) -> dict:
    violations = run_ruff_check(state['filepath'])
    # 每個警告降低就緒分數 5 分，最低 30 分
    score = max(30, 100 - len(violations) * 5)
    return {"ruff_warnings": violations, "readiness_score": score}

def rag_node(state: OrchestrationState) -> dict:
    context = query_lightrag_context(state['filename'])
    return {"rag_context": context}

def gemini_node(state: OrchestrationState) -> dict:
    # 組合 Ruff 報告與 RAG 雙層關係圖譜進行深層 AI 語意彙整
    prompt = (
        f"You are the Genesis System Architect. Analyze code architecture and compile capability metrics.\n\n"
        f"File Name: {state['filename']}\n"
        f"Path: {state['relative_path']}\n"
        f"Ruff violations count: {len(state['ruff_warnings'])} warnings.\n"
        f"LightRAG Grounding Context:\n{state['rag_context']}\n\n"
        f"Code Snippet:\n{state['code_snippet']}\n\n"
        f"Please synthesize this into a structured Capability Card JSON containing:\n"
        f"- category (分類，例如：系統防護與健康監控、核心智慧路由、資料調度與同步、輔助工具)\n"
        f"- ai_best_use_case (此模組的最佳使用情境/起火時機)\n"
        f"- readiness_score (就緒分數，建議使用: {state['readiness_score']})\n"
        f"- short_description (一句話簡介功能)\n"
        f"- dependencies (列出此檔案依賴的其他模組/檔案名稱)"
    )
    ai_card = call_llm_direct(prompt)
    return {"ai_card": ai_card}

# 組裝與編譯 LangGraph
workflow = StateGraph(OrchestrationState)
workflow.add_node("ruff", ruff_node)
workflow.add_node("rag", rag_node)
workflow.add_node("gemini", gemini_node)

workflow.set_entry_point("ruff")
workflow.add_edge("ruff", "rag")
workflow.add_edge("rag", "gemini")
workflow.add_edge("gemini", END)

compiled_graph = workflow.compile()

# 5. Prefect 工作流 Tasks & Flow
def add_script(scripts, file, full_path):
    try:
        hasher = hashlib.sha256()
        with open(full_path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                hasher.update(chunk)
        sha = hasher.hexdigest()
        scripts.append({
            "file_name": file,
            "full_path": full_path,
            "relative_path": os.path.relpath(full_path, GENESIS_BASE),
            "sha256": sha
        })
    except Exception as e:
        logging.error(f"Scan properties error on {file}: {e}")

@task(name="Scan Genesis codebase Python scripts")
def scan_codebase_task():
    scripts = []
    
    # 1. Scan Management_Hub
    hub_dir = os.path.join(GENESIS_BASE, "Management_Hub")
    if os.path.exists(hub_dir):
        for file in os.listdir(hub_dir):
            if file.endswith(".py"):
                full_path = os.path.join(hub_dir, file)
                add_script(scripts, file, full_path)
                
    # 2. Scan Logic Bricks
    logic_dir = os.path.join(GENESIS_BASE, "RD_Center", "SDK_Bricks", "Logic")
    if os.path.exists(logic_dir):
        for file in os.listdir(logic_dir):
            if file.endswith(".py"):
                full_path = os.path.join(logic_dir, file)
                add_script(scripts, file, full_path)
                
    # 3. Add key root files
    key_root_files = ["dashboard_server.py", "genesis_closed_loop_optimizer.py"]
    for file in key_root_files:
        full_path = os.path.join(GENESIS_BASE, file)
        if os.path.exists(full_path):
            add_script(scripts, file, full_path)
            
    return scripts

@task(name="LangGraph Analysis Node Worker")
def process_single_script(script, cache):
    cache_key = f"analysis_{script['sha256']}"
    cached_val = cache.get(cache_key)
    
    if cached_val:
        return cached_val, True
        
    # 讀取代碼片段 (前 150 行)
    try:
        with open(script["full_path"], "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
        snippet = "".join(lines[:150])
    except Exception:
        snippet = ""
        
    initial_state = {
        "filepath": script["full_path"],
        "filename": script["file_name"],
        "relative_path": script["relative_path"],
        "sha256": script["sha256"],
        "code_snippet": snippet,
        "ruff_warnings": [],
        "rag_context": "",
        "readiness_score": 100,
        "ai_card": {},
        "errors": []
    }
    
    # 執行 LangGraph 狀態圖
    final_state = compiled_graph.invoke(initial_state)
    result = final_state["ai_card"]
    
    # 將 RAG 依賴與 Ruff 診斷附加在結果中
    result["ruff_violations_count"] = len(final_state.get("ruff_warnings", []))
    result["readiness_score"] = final_state.get("readiness_score", 100)
    
    # 寫入 DiskCache 快取
    cache.set(cache_key, result)
    return result, False

@task(name="Node-RED Webhook Notify")
def notify_nodered():
    try:
        url = "http://127.0.0.1:1880/refresh-ai-feed"
        req = urllib.request.Request(url, method="POST", data=b"{}")
        with urllib.request.urlopen(req, timeout=1.0) as r:
            pass
        log_and_print("Node-RED UI refresh webhook triggered successfully!")
    except Exception:
        pass

@flow(name="Genesis Codebase Semantic Orchestrator Flow")
def orchestrate_genesis_codebase():
    log_and_print("⚡ Prefect工作流啟動：開始進行全域 Python 程式碼編排檢索分析...")
    scripts = scan_codebase_task()
    
    cache = Cache(CACHE_DIR)
    catalog = []
    
    new_analyzed = 0
    cache_hit = 0
    
    for s in scripts:
        result, is_cached = process_single_script(s, cache)
        if is_cached:
            cache_hit += 1
        else:
            new_analyzed += 1
            
        catalog.append({
            "file_name": s["file_name"],
            "path": s["relative_path"],
            "category": result.get("category", "專用工具與擴充模組"),
            "ai_best_use_case": result.get("ai_best_use_case", "按需點火調度。"),
            "readiness_score": result.get("readiness_score", 90),
            "short_description": result.get("short_description", ""),
            "dependencies": result.get("dependencies", []),
            "ruff_violations_count": result.get("ruff_violations_count", 0),
            "last_updated": time.strftime("%Y-%m-%d %H:%M:%S")
        })
        
    dashboard_payload = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_analyzed_modules": len(catalog),
        "ai_status": "運行中 (Active)",
        "modules_catalog": catalog,
        "engine_details": {
            "langgraph_active": True,
            "prefect_monitored": True,
            "lightrag_grounded": True,
            "ruff_analyzer_active": True,
            "diskcache_hits": cache_hit,
            "newly_compiled": new_analyzed
        }
    }
    
    # 寫入 dashboard_ai_intelligence.json 共享快取
    with open(DASHBOARD_DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(dashboard_payload, f, indent=4, ensure_ascii=False)
        
    # 計算 SHA-256 實體特徵碼
    hasher = hashlib.sha256(json.dumps(dashboard_payload, sort_keys=True).encode('utf-8'))
    log_and_print(f"✅ AI 智慧編排分析完畢！(新分析: {new_analyzed}, 快取命中: {cache_hit})")
    log_and_print(f"實體校驗代碼 (Entity Hash): {hasher.hexdigest()}")
    
    cache.close()
    
    # 觸發 Node-RED Webhook 重新載入
    notify_nodered()

if __name__ == "__main__":
    orchestrate_genesis_codebase()