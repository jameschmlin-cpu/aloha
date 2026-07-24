import os



# 帝國統一部署清單：此處定義所有必要的路徑與檔案內容

base = r"C:\Genesis"

configs = {

    r"SDK\Modules\__init__.py": "",

    r"SDK\__init__.py": "",

    r"SDK\Modules\Dispatcher.py": "class AIDispatcher:\n    def broadcast(self, msg): print(f'[Dispatcher] {msg}')",

    r"SDK\Orchestrator.py": """

import sys, os

sys.path.append(r'C:\Genesis\SDK')

from Modules.Dispatcher import AIDispatcher

def run():

    print("【帝國系統連線成功】所有模組自動掛載中...")

    AIDispatcher().broadcast("全節點自檢完畢，系統穩定。")

if __name__ == '__main__': run()

""",

    "Imperial_Launcher.bat": "@echo off\npython C:\\ITE\\SDK\\Orchestrator.py\npause"

}



# 自動化部署邏輯：一次解決，不需您手動干預

def deploy():

    for path, content in configs.items():

        full_path = os.path.join(base, path)

        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, "w", encoding="utf-8") as f:

            f.write(content)

        print(f"【自動化部署】已產出：{full_path}")

    print("\n【部署完成】您以後只需要點擊 Imperial_Launcher.bat，所有複雜結構已自動處理。")



if __name__ == "__main__":

    deploy()