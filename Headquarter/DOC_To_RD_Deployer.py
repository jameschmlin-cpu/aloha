import os
import re

# 定義路徑
DOC_DIR = r"C:\Genesis\Headquarter\DOC"
RD_DIR = r"C:\Genesis\Headquarter\RD"

class Deployer:
    def __init__(self):
        os.makedirs(RD_DIR, exist_ok=True)

    def extract_and_save(self, md_filename):
        md_path = os.path.join(DOC_DIR, md_filename)
        if not os.path.exists(md_path):
            print(f"[ERROR] 找不到檔案: {md_path}")
            return

        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 抓取所有 Markdown 代碼區塊
        # 支援 ```python ... ``` 以及 ```yaml ... ```
        pattern = re.compile(r"```(?P<lang>\w+)\n(?P<code>.*?)```", re.DOTALL)
        
        for match in pattern.finditer(content):
            lang = match.group('lang')
            code = match.group('code').strip()
            
            # 自動命名檔案 (以內容特徵或序號命名)
            ext = ".py" if lang == "python" else ".yaml"
            filename = f"Generated_Asset_{match.start()}{ext}"
            
            target_path = os.path.join(RD_DIR, filename)
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(code)
            print(f"[SUCCESS] 實體化部署: {filename}")

if __name__ == "__main__":
    deployer = Deployer()
    # 自動抓取 DOC 目錄下所有的 MD 檔案
    for file in os.listdir(DOC_DIR):
        if file.endswith(".md"):
            deployer.extract_and_save(file)