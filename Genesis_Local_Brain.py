import ollama
import re

# 初始化 Client，統一連接至本地節點
client = ollama.Client(host='http://127.0.0.1:11434')

def get_ai_cmd(task_name):
    """
    使用 RTX 3060 本地 Qwen2.5-Coder 引擎進行工程任務解析
    """
    # 1. 任務名稱正規化
    clean_task = re.sub(r'\(.*?\)', '', task_name).strip()
    
    # 2. 強力限制 System Instruction
    system_instruction = (
        "你是一個 Genesis 系統的工程核心。請將任務轉譯為一條 Windows PowerShell 或 CMD 指令。"
        "輸出準則：僅回傳指令字串。禁止任何 Markdown 標記、禁止反引號、禁止文字說明、禁止換行。"
        "若任務無法轉譯為安全可執行的單行指令，請僅回傳字串 'SKIP'。"
    )
    
    try:
        # 使用全域 client 進行呼叫
        response = client.chat(model='qwen2.5-coder:7b', messages=[
            {'role': 'system', 'content': system_instruction},
            {'role': 'user', 'content': f"任務: {clean_task}"},
        ])
        
        raw_cmd = response['message']['content'].strip()
        
        # 3. 強制格式清洗
        cmd = re.sub(r'```[a-zA-Z]*', '', raw_cmd)
        cmd = cmd.replace('`', '').replace('bash', '').replace('powershell', '').strip()
        cmd = cmd.split('\n')[0].strip()
        
        # 4. 安全性檢核
        if len(cmd) < 3 or cmd.upper() == "SKIP":
            return "SKIP"
            
        return cmd
        
    except Exception as e:
        print(f"Node C AI 決策異常: {e}")
        return "SKIP"