import os

import hashlib



# 嚴格定義路徑與名稱

base_path = r"C:\Genesis"

sdk_path = os.path.join(base_path, "SDK")

modules_path = os.path.join(sdk_path, "Modules")

launcher_name = "Imperial_Launcher.bat"

launcher_path = os.path.join(base_path, launcher_name)



# 建立完整路徑

for p in [sdk_path, modules_path]:

    os.makedirs(p, exist_ok=True)



# 1. 產生前端：Imperial_Launcher.bat (僅負責呼叫)

batch_content = f"""@echo off

:: 帝國啟動門戶：{launcher_name}

:: 嚴禁在此執行運算，僅負責呼叫 SDK 總指揮官

echo Initializing Imperial System...

python {base_path}\\SDK\\Orchestrator.py

"""



# 2. 產生後端：Orchestrator.py (SDK 總指揮官)

orchestrator_content = """

from Modules.Dispatcher import AIDispatcher

def run():

    print("帝國聯動架構啟動：監控、調度、推進器已綁定")

    dispatcher = AIDispatcher()

    dispatcher.broadcast("全系統連線成功")



if __name__ == "__main__":

    run()

"""



# 3. 產生後端：Dispatcher.py (AI 中央調度器)

dispatcher_content = "class AIDispatcher: \n    def broadcast(self, msg): print(f'[Dispatcher] {msg}')"



# 物理寫入所有模組

files = {

    launcher_path: batch_content,

    os.path.join(sdk_path, "Orchestrator.py"): orchestrator_content,

    os.path.join(modules_path, "Dispatcher.py"): dispatcher_content

}



for path, content in files.items():

    with open(path, "w", encoding="utf-8") as f:

        f.write(content)

    print(f"成功部署元件：{path}")



# 最後 Hash 驗證

with open(launcher_path, "rb") as f:

    print(f"【規格確認】{launcher_name} SHA-256: {hashlib.sha256(f.read()).hexdigest()}")