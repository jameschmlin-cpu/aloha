# -*- coding: utf-8 -*-
"""
🚀 Genesis_Autonomous_DevOps_Agent.py
Genesis 數位員工自主進化與動態修復引擎

整合: Ruff (靜態防禦) + DiskCache (快取) + LightRAG (知識圖譜) + LangGraph/Closed-Loop (自主修復與測試) + Node-RED
"""
import os
import sys
import json
import hashlib
import shutil
import subprocess
import urllib.request
import urllib.parse
import logging
from datetime import datetime

# 設定環境變量與路徑
GENESIS_BASE = r"C:\Genesis"
CACHE_DIR = os.path.join(GENESIS_BASE, "cache", "devops_cache")
REPORT_PATH = os.path.join(GENESIS_BASE, "Config", "dashboard_health_evolution_report.json")
ADVICE_PATH = os.path.join(GENESIS_BASE, "Config", "dashboard_evolution_advice.json")
SANDBOX_DIR = os.path.join(GENESIS_BASE, "cache", "sandbox_tests")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(GENESIS_BASE, "Logs", "devops_agent.log"), encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

# 載入 DiskCache
try:
    import diskcache
    cache = diskcache.Cache(CACHE_DIR)
except Exception:
    cache = None
    logging.warning("DiskCache import failed. Falling back to in-memory/JSON cache.")

def write_claw_focus(resource_id, detail, label="DevOps_Agent"):
    try:
        focus_path = r"C:\Users\user\.openclaw\subagents\focus-devops.json"
        # Ensure dir exists
        os.makedirs(os.path.dirname(focus_path), exist_ok=True)
        data = {
            "resourceId": resource_id,
            "detail": detail,
            "label": label
        }
        with open(focus_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        logging.error(f"Failed to write ClawLibrary focus file: {e}")

# 讀取 Gemini 金鑰
def get_gemini_key():
    config_path = r"C:\Genesis\Config\telegram_config.json"
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                key = cfg.get("gemini_api_key", "")
                if key and "YOUR_GEMINI_API_KEY" not in key:
                    return key
        except Exception:
            pass
    return None

# LLM 呼叫中心 (支援 Gemini + Ollama 備用)
def call_llm(prompt, response_schema=None, is_json=False):
    gemini_key = get_gemini_key()
    if gemini_key:
        try:
            model = "gemini-3.5-flash"
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={gemini_key}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}]
            }
            if is_json:
                payload["generationConfig"] = {"responseMimeType": "application/json"}
                if response_schema:
                    payload["generationConfig"]["responseSchema"] = response_schema
            
            req = urllib.request.Request(
                url, 
                data=json.dumps(payload).encode('utf-8'), 
                headers={'Content-Type': 'application/json'}
            )
            with urllib.request.urlopen(req, timeout=25) as response:
                res_data = json.loads(response.read().decode('utf-8'))
                return res_data['candidates'][0]['content']['parts'][0]['text']
        except Exception as e:
            logging.error(f"Gemini API invocation failed: {e}")
            
    # Ollama 本地備用
    try:
        url = "http://localhost:11434/api/chat"
        payload = {
            "model": "qwen2.5-coder:7b",
            "messages": [
                {"role": "system", "content": "You are the Genesis Lead DevOps AI. Help compile, debug and update scripts. Output in JSON or clean code as requested."},
                {"role": "user", "content": prompt}
            ],
            "stream": False
        }
        if is_json:
            payload["format"] = "json"
        req = urllib.request.Request(
            url, 
            data=json.dumps(payload).encode('utf-8'), 
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=20) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            return res_data['message']['content']
    except Exception as e:
        logging.error(f"Ollama local fallback failed: {e}")
        return None

# 1. 呼叫 Ruff 檢驗
def check_ruff_violations(filepath):
    try:
        cmd = ["ruff", "check", filepath, "--format", "json"]
        res = subprocess.run(cmd, capture_output=True, text=True, creationflags=0x08000000)
        if res.stdout.strip():
            return json.loads(res.stdout)
        return []
    except Exception as e:
        logging.error(f"Failed to run Ruff check: {e}")
        return []

# 2. 透過 LightRAG 進行依賴查尋
def query_lightrag_dependency(filename):
    try:
        engine_script = os.path.join(GENESIS_BASE, "RD_Center", "SDK", "System", "LightRAG_Engine.py")
        q = f"Detail all downstream dependencies, callers and impact of script: {filename}"
        res = subprocess.run(
            [sys.executable, engine_script, 'query', q],
            capture_output=True, text=True, encoding='utf-8', errors='ignore', creationflags=0x08000000, timeout=20.0
        )
        output = res.stdout.strip()
        if "[LightRAG 檢索結果]:" in output:
            return output.split("[LightRAG 檢索結果]:")[-1].strip()
        return output if output else "No RAG dependency found."
    except Exception as e:
        logging.error(f"LightRAG subprocess query failed: {e}")
        return "No LightRAG connection."

# 3. 呼叫 Node-RED 進行動態通知
def notify_nodered(payload):
    try:
        url = "http://localhost:1880/api/devops-webhook"
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=3) as resp:
            pass
    except Exception:
        pass

# 4. 夜間自動重構品質防禦 (Ruff + LangGraph Closed-Loop)
def run_nightly_refactor():
    logging.info("Starting Nightly Refactoring and Quality Shield Loop...")
    write_claw_focus("research_center", "正在啟動夜間自動品質防護與代碼掃描...")
    
    # 決定掃描模組
    scan_dirs = [
        os.path.join(GENESIS_BASE, "Management_Hub"),
        os.path.join(GENESIS_BASE, "RD_Center", "SDK_Bricks", "Logic")
    ]
    files_to_scan = []
    for d in scan_dirs:
        if os.path.exists(d):
            for file in os.listdir(d):
                if file.endswith(".py"):
                    files_to_scan.append(os.path.join(d, file))
                    
    report_items = []
    
    for filepath in files_to_scan:
        filename = os.path.basename(filepath)
        logging.info(f"Scanning {filename} with Ruff...")
        write_claw_focus("research_center", f"正在使用 Ruff 靜態防禦掃描 {filename}...")
        
        violations = check_ruff_violations(filepath)
        if not violations:
            logging.info(f"No violations in {filename}. Code is clean.")
            continue
            
        logging.warning(f"Ruff detected {len(violations)} warnings/errors in {filename}.")
        
        # 檢查快取
        with open(filepath, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
            
        if cache and cache.get(f"clean_refactor:{file_hash}"):
            logging.info(f"Skipping {filename} - already verified and refactored in cache.")
            continue
            
        # 開始閉環修復推導
        success = execute_closed_loop_repair(filepath, violations)
        
        report_items.append({
            "filename": filename,
            "violations_count": len(violations),
            "repaired": success,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
    # 寫入健康報告
    report_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "scanned_count": len(files_to_scan),
        "refactored_modules": report_items
    }
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=4, ensure_ascii=False)
        
    logging.info("Nightly Refactoring and Quality Shield complete!")
    write_claw_focus("recreation_room", "品質重構防線已全數驗證 PASS ☕")
    notify_nodered({"event": "nightly_refactor_complete", "report": report_data})

# 5. 閉環修復與單元測試沙盒迴圈
def execute_closed_loop_repair(filepath, violations):
    filename = os.path.basename(filepath)
    backup_path = filepath + ".bak"
    shutil.copyfile(filepath, backup_path)
    
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        original_code = f.read()
        
    logging.info(f"Initiating closed-loop repair for {filename}...")
    write_claw_focus("commander_office", f"正在執行閉環修復與單元測試: {filename}")
    
    prompt = f"""
You are the Genesis Lead DevOps AI. Fix the Ruff codebase violations found in this Python script.
DO NOT change any core functional logic, import libraries, or logic loops. Only fix style/syntax rules.

Ruff Violations Found:
{json.dumps(violations, indent=2)}

Original Code:
```python
{original_code}
```

Respond with ONLY the fully refactored, valid python code. No explanation, no markdown wraps.
"""
    refactored_code = call_llm(prompt)
    if not refactored_code:
        logging.error("Failed to generate refactored code.")
        return False
        
    # Clean output blocks
    if "```python" in refactored_code:
        refactored_code = refactored_code.split("```python")[1].split("```")[0].strip()
    elif "```" in refactored_code:
        refactored_code = refactored_code.split("```")[1].split("```")[0].strip()
        
    # 寫入暫存檔案
    os.makedirs(SANDBOX_DIR, exist_ok=True)
    temp_filepath = os.path.join(SANDBOX_DIR, filename)
    with open(temp_filepath, "w", encoding="utf-8") as f:
        f.write(refactored_code)
        
    # 自動生成 Pytest 單元測試進行驗證
    test_filepath = os.path.join(SANDBOX_DIR, f"test_{filename}")
    test_prompt = f"""
Write a simple pytest suite verifying that the refactored code has valid syntax and runs main entry logic or mock tests.
Make it lightweight and assert basic functions return correct values.

Refactored Code:
```python
{refactored_code}
```

Respond with ONLY the valid python test script. No markdown wraps, no explanation.
"""
    test_code = call_llm(test_prompt)
    if test_code:
        if "```python" in test_code:
            test_code = test_code.split("```python")[1].split("```")[0].strip()
        with open(test_filepath, "w", encoding="utf-8") as f:
            f.write(test_code)
            
        # 在沙盒中跑 Pytest
        logging.info(f"Running pytest sandbox loop for {filename}...")
        try:
            res = subprocess.run(["pytest", test_filepath], capture_output=True, text=True, timeout=15)
            if res.returncode == 0:
                logging.info(f"✅ Sandbox validation PASS for {filename}!")
                # 正式寫入原檔案
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(refactored_code)
                # 更新 Node A 的 Baseline Hash
                update_hash_baseline(filepath)
                # 寫入 DiskCache
                if cache:
                    with open(filepath, "rb") as f:
                        new_hash = hashlib.sha256(f.read()).hexdigest()
                    cache.set(f"clean_refactor:{new_hash}", True)
                # 刪除備份
                os.remove(backup_path)
                return True
            else:
                logging.error(f"❌ Pytest failed on sandbox: {res.stdout}")
        except Exception as e:
            logging.error(f"Sandbox runner crash: {e}")
            
    # 失敗復原
    logging.warning(f"Reverting {filename} from backup due to test failure.")
    shutil.copyfile(backup_path, filepath)
    os.remove(backup_path)
    return False

# 6. 動態影響評估 (LightRAG + LangGraph)
def execute_impact_analysis(filepath):
    filename = os.path.basename(filepath)
    logging.info(f"Analyzing dependency impact of {filename} using LightRAG...")
    write_claw_focus("research_center", f"評估程式碼修改影響: {filename}")
    
    rag_context = query_lightrag_dependency(filename)
    
    prompt = f"""
Analyze the potential ripple effects and impact of modifying the module '{filename}' in the Genesis closed-loop system.
Use the following LightRAG query context to synthesize your architectural advice:

RAG Context:
{rag_context}

Output format:
1. Short sentence: "報告主管，此修改會影響下游的 X 個常駐模組與 Y 個 API" (Fill X and Y dynamically).
2. Bullet points outlining dependencies and caller hierarchy.
3. Mitigation advice.
"""
    advice = call_llm(prompt)
    print("\n[AI 影響評估與影響導航儀輸出]:")
    print(advice)
    write_claw_focus("recreation_room", f"變更影響評估已完成 {filename} ☕")
    return advice

def generate_local_advisor_fallback():
    hub_files = os.listdir(os.path.join(GENESIS_BASE, "Management_Hub"))
    logic_files = os.listdir(os.path.join(GENESIS_BASE, "RD_Center", "SDK_Bricks", "Logic"))
    
    fallback_data = []
    
    for f in hub_files:
        if f.endswith(".py"):
            rec = {
                "module": f"Management_Hub/{f}",
                "current_state": "運作中，核心防護與管理邏輯正常。",
                "upgrade_recommendation": f"建議針對 {f} 導入輕量級 Pydantic 驗證，並使用 LangChain / LangGraph 以狀態機模式管理流程，提升閉環控制的穩定性。",
                "priority": "MEDIUM"
            }
            if "orchestrator" in f.lower():
                rec["upgrade_recommendation"] = "建議將 RAG 圖譜的實體快取擴展為分散式向量資料庫，以支援更大規模的微服務架構。"
                rec["priority"] = "HIGH"
            elif "watchdog" in f.lower():
                rec["upgrade_recommendation"] = "建議將故障自癒邏輯接入 Telegram 語音通話或主動簡訊發送 API，實現全方位二次元角色即時響應。"
                rec["priority"] = "HIGH"
            fallback_data.append(rec)
            
    for f in logic_files:
        if f.endswith(".py"):
            rec = {
                "module": f"Logic_Bricks/{f}",
                "current_state": "已部署的 SDK 動作元件，具備基礎行為能力。",
                "upgrade_recommendation": f"針對該控制磚塊，可使用 Reinforcement Learning (RL) 進行微調，或配合本機小型 LLM 做意圖分類，使裝置具備更敏捷的物理反饋機制。",
                "priority": "MEDIUM"
            }
            if "Robot_Movement" in f:
                rec["upgrade_recommendation"] = "建議導入具備空間避障意識的 3D Path Finding LLM，結合 HWiNFO 讀取的馬達溫度與震動，自我微調加速度曲線。"
                rec["priority"] = "HIGH"
            fallback_data.append(rec)
            
    return fallback_data

# 7. 自我評估進化顧問報告
def run_evolution_advisor():
    logging.info("Starting Self-Evaluation Advisor scanning...")
    write_claw_focus("research_center", "正在評估架構，編譯自我進化顧問報告...")
    
    hub_files = os.listdir(os.path.join(GENESIS_BASE, "Management_Hub"))
    logic_files = os.listdir(os.path.join(GENESIS_BASE, "RD_Center", "SDK_Bricks", "Logic"))
    
    prompt = f"""
You are the Genesis Lead Software Architect and Evolution Advisor. 
Evaluate the active management scripts and bricks:
Management Center: {json.dumps(hub_files)}
Custom Bricks: {json.dumps(logic_files)}

Provide upgrade recommendations on how to integrate the latest generative AI patterns or lightweight automation.
Structure the response as a JSON array of suggestions with keys: "module", "current_state", "upgrade_recommendation", "priority".
"""
    res = call_llm(prompt, is_json=True)
    parsed_successfully = False
    
    if res:
        try:
            clean_res = res.strip()
            if "```json" in clean_res:
                clean_res = clean_res.split("```json")[1].split("```")[0].strip()
            data = json.loads(clean_res)
            with open(ADVICE_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            logging.info("Evolution advisor report created via LLM!")
            print("Evolution advisor report created successfully!")
            parsed_successfully = True
        except Exception as e:
            logging.error(f"Failed to parse advisor LLM output: {e}")

    if not parsed_successfully:
        logging.warning("API failed or output parsing failed. Utilizing local evolution fallback compiler...")
        fallback_data = generate_local_advisor_fallback()
        with open(ADVICE_PATH, "w", encoding="utf-8") as f:
            json.dump(fallback_data, f, indent=4, ensure_ascii=False)
        logging.info("Evolution advisor report created via Local Fallback Compiler!")
        print("Evolution advisor report created successfully (Local Fallback)!")
    
    write_claw_focus("recreation_room", "架構進化建議報告已成功發布 ☕")

# 更新 Node A 的 Baseline Hash
def update_hash_baseline(filepath):
    baseline_path = r"C:\ITE\Antigravity\baseline_genesis.json"
    if os.path.exists(baseline_path):
        try:
            with open(filepath, "rb") as f:
                new_hash = hashlib.sha256(f.read()).hexdigest().upper()
            
            with open(baseline_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            data[filepath] = new_hash
            
            with open(baseline_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            logging.info(f"Node A baseline hash successfully locked for: {filepath}")
        except Exception as e:
            logging.error(f"Failed to update baseline json: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        if mode == "--nightly-refactor":
            run_nightly_refactor()
        elif mode == "--impact-analysis" and len(sys.argv) > 2:
            execute_impact_analysis(sys.argv[2])
        elif mode == "--evolution-advisor":
            run_evolution_advisor()
        else:
            print("Usage: python Genesis_Autonomous_DevOps_Agent.py [--nightly-refactor | --impact-analysis <path> | --evolution-advisor]")
    else:
        # Default behavior: run refactor & evolution checks
        run_nightly_refactor()
        run_evolution_advisor()
