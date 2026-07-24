# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\RD_Center\SDK\AI_Core\Gemini_Agent.py
# 狀態：全系統資源管理擴充版 (完整實體代碼)
# 實體 Hash: 0xGEN-AGENT-STRICT-20260711-D

import os
import json
import urllib.request
import urllib.error
import sys

class GeminiAgent:
    def __init__(self, prefer_local=True, model_name="qwen2.5-coder:7b", ollama_host="http://localhost:11434"):
        self.prefer_local = prefer_local
        self.model_name = model_name
        self.ollama_host = ollama_host
        self.gemini_key = os.environ.get("GEMINI_API_KEY", "")
        self.development_mode = "HYBRID"
        config_path = r"C:\Genesis\Config\telegram_config.json"
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                    self.development_mode = cfg.get("development_mode", "HYBRID").strip().upper()
                    key = cfg.get("gemini_api_key", "")
                    if key and "YOUR_GEMINI_API_KEY" not in key:
                        self.gemini_key = key
            except Exception:
                pass

        self.schema = {
            "type": "OBJECT",
            "properties": {
                "response_type": {"type": "STRING"},
                "conversational_answer": {"type": "STRING"},
                "decision": {"type": "STRING"},
                "target_brick": {"type": "STRING"},
                "parameters": {"type": "OBJECT"},
                "patch_code": {"type": "STRING"}
            },
            "required": ["response_type", "conversational_answer", "decision", "target_brick", "parameters", "patch_code"]
        }

    def _call_local_ollama(self, prompt, system_instruction):
        url = f"{self.ollama_host}/api/chat"
        messages = [{"role": "system", "content": system_instruction}, {"role": "user", "content": prompt}]
        payload = {"model": self.model_name, "messages": messages, "stream": False, "format": "json"}
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=12) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            return res_data['message']['content']

    def _call_cloud_gemini(self, prompt, system_instruction):
        if not self.gemini_key:
            raise ValueError("[ERROR] GEMINI_API_KEY Missing")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={self.gemini_key}"
        payload = {
            "contents": [{"parts": [{"text": f"System: {system_instruction}\nUser: {prompt}"}]}],
            "generationConfig": {"responseMimeType": "application/json", "responseSchema": self.schema}
        }
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=30) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            return res_data['candidates'][0]['content']['parts'][0]['text']

    def execute_free_instruction(self, user_instruction, telemetry_context=None):
        """核心分流方法：接收自然語言指令，輸出結構化自癒決策"""
        # 嚴格初始化變數，防禦 NameError
        decision = {
            "response_type": "TEXT",
            "conversational_answer": "系統認知大腦暫時無法響應，請主管核查基礎連線。",
            "decision": "NONE",
            "target_brick": "",
            "parameters": {},
            "patch_code": ""
        }
        
        system_instruction = (
            "You are Genesis AI Cognitive Governor (志玲 V3-Expert).\n"
            "CRITICAL RULE: You must check the 'services_status' dictionary in the telemetry context before answering any query about service status or offline errors. "
            "If the user claims a service (like Node-RED, Dashboard, ClawLibrary, Ollama) is down or lost, but the context shows it is 'ONLINE', do NOT confirm that it has a problem. "
            "Instead, politely inform the supervisor that the service is running normally and there is no need to restart it. "
            "Output valid, raw JSON only matching the schema exactly:\n"
            "{\n"
            "  \"response_type\": \"TEXT\" or \"ACTION\",\n"
            "  \"conversational_answer\": \"your friendly Taiwanese Traditional Chinese response in Lin Chi-ling tone (starting with '親愛的雋懋主管您好！' and ending with '我們一起加油！🌸')\",\n"
            "  \"decision\": \"NONE\" or \"EXECUTE\",\n"
            "  \"target_brick\": \"name of python brick to run (e.g. Robot_Movement or Sensor_Sampling) if response_type is ACTION, else empty string\",\n"
            "  \"parameters\": {},\n"
            "  \"patch_code\": \"the python code content to be written/patched to the brick if code modifications/creations are requested, else empty string\"\n"
            "}"
        )
        prompt = f"User Request: {user_instruction}\nContext: {json.dumps(telemetry_context)}"
        
        # 根據指令複雜度決定優先路由策略
        is_complex = False
        complex_keywords = ["code", "patch", "write", "class", "def", "import", "修補", "代碼", "重構", "自癒", "修復", "編譯", "cwe", "dfmea"]
        instruction_lower = user_instruction.lower()
        if any(kw in instruction_lower for kw in complex_keywords):
            is_complex = True
            
        if self.development_mode == "LOCAL":
            engines = [("Local RTX 3060", self._call_local_ollama, 3)]
        else:
            if is_complex:
                # 複雜代碼/修復任務：優先由高智能的 Cloud Gemini 3.5 處理，Local Ollama 備份
                engines = [("Cloud Gemini", self._call_cloud_gemini, 3), ("Local RTX 3060", self._call_local_ollama, 2)]
            else:
                # 簡單查詢與路由：優先由地端 Ollama 處理以節省 API，Gemini 備份
                engines = [("Local RTX 3060", self._call_local_ollama, 2), ("Cloud Gemini", self._call_cloud_gemini, 2)]
        
        for name, run_engine, max_attempts in engines:
            current_prompt = prompt
            for attempt in range(1, max_attempts + 1):
                try:
                    print(f"[Node B] 正在向 {name} 發送決策請求 (嘗試 {attempt}/{max_attempts})...")
                    response_text = run_engine(current_prompt, system_instruction)
                    decision = json.loads(response_text)
                    required_keys = ["response_type", "conversational_answer", "decision", "target_brick", "parameters", "patch_code"]
                    missing_keys = [k for k in required_keys if k not in decision]
                    if missing_keys:
                        raise ValueError(f"Missing required JSON schema keys: {missing_keys}")
                    return decision
                except Exception as e:
                    print(f"[Node D] {name} (嘗試 {attempt}/{max_attempts}) 驗證失敗: {e}")
                    current_prompt = (
                        f"User Request: {user_instruction}\n"
                        f"Context: {json.dumps(telemetry_context)}\n"
                        f"\n[SYSTEM RETRY NOTE] Your previous response failed validation: {e}. "
                        f"Please output strictly valid raw JSON matching the required schema: {self.schema}"
                    )
                    
        return decision # 若皆失敗，回傳已初始化的防禦性變數

if __name__ == "__main__":
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(errors='replace')
    agent = GeminiAgent()
    res = agent.execute_free_instruction("系統健檢", {"status": "init"})
    print(f"\n[Node C 回傳狀態]:\n{json.dumps(res, indent=4, ensure_ascii=False)}")