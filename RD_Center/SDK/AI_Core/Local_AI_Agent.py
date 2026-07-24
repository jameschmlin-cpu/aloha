# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\RD_Center\SDK\AI_Core\Local_AI_Agent.py
# 狀態：本機運算優先（RTX 3060）之 AI 認知模組，整合 Ollama 並以 Gemini API 為備援

import os
import json
import urllib.request
import urllib.error

class LocalAIAgent:
    def __init__(self, model_name="qwen2.5-coder:7b", ollama_host="http://localhost:11434"):
        self.model_name = model_name
        self.ollama_host = ollama_host
        self.gemini_key = os.environ.get("GEMINI_API_KEY", "")
        if not self.gemini_key:
            config_path = r"C:\Genesis\Config\telegram_config.json"
            if os.path.exists(config_path):
                try:
                    with open(config_path, "r", encoding="utf-8") as f:
                        cfg = json.load(f)
                        key = cfg.get("gemini_api_key", "")
                        if key and "YOUR_GEMINI_API_KEY" not in key:
                            self.gemini_key = key
                except Exception:
                    pass

    def _call_local_ollama(self, prompt, system_instruction=None):
        """物理調用本機 RTX 3060 算力進行推理"""
        url = f"{self.ollama_host}/api/chat"
        
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": self.model_name,
            "messages": messages,
            "stream": False,
            "format": "json"  # 強制 Ollama 回傳結構化 JSON
        }
        
        req = urllib.request.Request(
            url, 
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        
        # 設置超時時間為 10 秒，若超時則自動切換至雲端備援
        with urllib.request.urlopen(req, timeout=10) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            return res_data['message']['content']

    def _call_cloud_gemini(self, prompt, system_instruction=None):
        """雲端備援：調用 Gemini API"""
        if not self.gemini_key:
            raise ValueError("[ERROR] 本機 Ollama 離網且未設定 GEMINI_API_KEY，無法啟用備援大腦")
            
        # 使用 Gemini API 3.5 flash REST 接口，免除套件依賴
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={self.gemini_key}"
        
        contents = []
        if system_instruction:
            prompt = f"System Instruction: {system_instruction}\n\nUser Request: {prompt}"
            
        contents.append({
            "parts": [{"text": prompt}]
        })
        
        payload = {
            "contents": contents,
            "generationConfig": {
                "responseMimeType": "application/json"  # 強制 Gemini 回傳 JSON
            }
        }
        
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req, timeout=15) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            return res_data['candidates'][0]['content']['parts'][0]['text']

    def analyze_and_decide(self, telemetry_data):
        """
        傳入系統遥測數據，輸出結構化決策
        """
        system_instruction = (
            "You are the Genesis AI Cognitive Governor. Analyze the system state and telemetry, "
            "and output a structured JSON response indicating the next healing action. "
            "CRITICAL: You MUST write the 'analysis' field in Traditional Chinese as used in Taiwan (台灣繁體中文). "
            "Do not include any thinking text or comments. Output ONLY the raw JSON object."
        )
        
        # Load Orchestration Guide context if available
        prompt_file = r"C:\Genesis\Config\Orchestration_Prompt.txt"
        if os.path.exists(prompt_file):
            try:
                with open(prompt_file, 'r', encoding='utf-8') as pf:
                    orchestration_guide = pf.read()
                system_instruction += "\n\n[Orchestration & Creative Bricks Guide]:\n" + orchestration_guide
            except Exception:
                pass
        
        prompt = f"""
        當前系統遙測資料:
        {json.dumps(telemetry_data, indent=4)}
        
        請分析上述資料。若有錯誤或系統資源異常（如負載超載或服務離線），決定修復或調度方法。回傳 JSON 格式如下:
        {{
            "analysis": "簡短的故障原因或資源分析",
            "decision": "EXECUTE_BRICK" 或 "HEAL_CODE" 或 "START_SERVICE" 或 "THROTTLE_RESOURCES" 或 "NONE",
            "target_brick": "要執行的積木檔案名稱（若是 START_SERVICE 則是服務名稱對應的啟動程式名稱）",
            "parameters": {{}},
            "patch_code": "若需要自癒，請在此輸出修補程式碼，否則為空"
        }}
        """
        
        def clean_json_text(text):
            text = text.strip()
            if text.startswith("```json"):
                text = text[7:]
            elif text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            return text.strip()

        # 1. 優先嘗試本機 RTX 3060 GPU
        try:
            print("[AI 認知] 優先調用本機 RTX 3060 算力...")
            response_text = self._call_local_ollama(prompt, system_instruction)
            cleaned = clean_json_text(response_text)
            return json.loads(cleaned)
        except Exception as local_err:
            print(f"[警告] 本地算力調用失敗或未啟動: {local_err}")
            
            # 2. 觸發雲端 Gemini 備援
            try:
                print("[AI 認知] 啟動雲端 Gemini 備援大腦...")
                response_text = self._call_cloud_gemini(prompt, system_instruction)
                cleaned = clean_json_text(response_text)
                return json.loads(cleaned)
            except Exception as cloud_err:
                print(f"[嚴重錯誤] 本地與雲端雙重推理通道中斷！: {cloud_err}")
                return {
                    "analysis": f"本地異常: {local_err} | 雲端異常: {cloud_err}",
                    "decision": "NONE",
                    "target_brick": "",
                    "parameters": {},
                    "patch_code": ""
                }

if __name__ == "__main__":
    agent = LocalAIAgent()
    mock_telemetry = {
        "status": "ERROR",
        "error_log": "FileNotFoundError: [Errno 2] No such file or directory: 'C:\\Genesis\\Database\\Genesis_DFMEA.db'",
        "temperature": "42 C"
    }
    decision = agent.analyze_and_decide(mock_telemetry)
    print(f"\n[AI 決策回傳]:\n{json.dumps(decision, indent=4, ensure_ascii=False)}")
