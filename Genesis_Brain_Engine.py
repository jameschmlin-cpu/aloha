import openai
import os
import ollama

# 初始化 AI 接口 (請確保您的環境變數已設定 OPENAI_API_KEY)
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_ai_cmd(task_name):
    """將自然語言任務轉譯為 Windows CLI 指令"""
    prompt = f"你是一個專業的 DevOps 工程師，請將任務 '{task_name}' 轉譯為一條 Windows PowerShell 可執行的指令。只回傳指令本身，不要有註解或引號。"
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "你是一個 Genesis 系統的決策層模組。"},
                      {"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return "SKIP"



def get_ai_cmd(task_name):
    """本地 RTX 3060 推理引擎"""
    prompt = f"請將任務 '{task_name}' 轉譯為一條 Windows CLI 指令。只回傳指令，不要輸出任何額外文字。"
    
    try:
        response = ollama.chat(model='llama3', messages=[
            {'role': 'user', 'content': prompt},
        ])
        return response['message']['content'].strip()
    except Exception:
        return "SKIP"