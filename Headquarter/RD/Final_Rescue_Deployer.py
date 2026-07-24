import os
import re

def rescue_code():
    doc_path = r"C:\Genesis\Headquarter\DOC\Conversation_Log.md"
    rd_dir = r"C:\Genesis\Headquarter\RD"
    os.makedirs(rd_dir, exist_ok=True)
    
    with open(doc_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 抓取所有 MD 代碼塊
    blocks = re.findall(r"```(\w+)\n(.*?)```", content, re.DOTALL)
    for i, (lang, code) in enumerate(blocks):
        ext = ".py" if lang in ['python', 'py'] else ".yaml"
        filename = f"Skill_{i:02d}{ext}"
        with open(os.path.join(rd_dir, filename), 'w', encoding='utf-8') as f:
            f.write(code.strip())
    print(f"[SUCCESS] 已救回所有程式至: {rd_dir}")

if __name__ == "__main__":
    rescue_code()