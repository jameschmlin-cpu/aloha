# C:\Genesis\Genesis_Fix_Deployer.py
import os

def fix_and_deploy():
    root = r"C:\Genesis"
    sdk_ai_core = os.path.join(root, "SDK", "AI_Core")
    
    # 修正：加入 root 到 sys.path，確保 import 不會中斷
    prefix_code = "import sys\nimport os\nsys.path.append(r'C:\\Genesis')\n"
    
    files = {
        "Gemini_Command_Center.py": os.path.join(root, "Management_Hub", "Gemini_Command_Center.py"),
        "Orchestrator.py": os.path.join(root, "Engine", "Orchestrator.py")
    }

    for name, src in files.items():
        if os.path.exists(src):
            dest = os.path.join(sdk_ai_core, name)
            # 讀取原檔並注入 path 修正
            with open(src, "r", encoding="utf-8") as f:
                content = f.read()
            with open(dest, "w", encoding="utf-8") as f:
                f.write(prefix_code + content)
            
            # 測試編譯
            try:
                compile(open(dest, "r", encoding="utf-8").read(), dest, 'exec')
                print(f"[修正通過] {name} 路徑依賴已修復。")
            except Exception as e:
                print(f"[嚴重錯誤] {name} 依然失敗: {e}")
                return

    print("--- [沙盒修復完成，請再次驗證] ---")

if __name__ == "__main__":
    fix_and_deploy()