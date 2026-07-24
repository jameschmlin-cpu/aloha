# C:\Genesis\Headquarter\RD\Solo_Empire_Orchestrator.py
# 用於一人公司的一鍵自動化啟動
import subprocess

def launch_empire():
    print("[System] 董事長，一人公司帝國指揮系統啟動中...")
    # 1. 自動啟動審計監控視窗
    subprocess.Popen(['start', 'python', r'C:\\Genesis\\Headquarter\\RD\\Audit_Monitor.py'], shell=True)
    # 2. 自動啟動指揮引擎
    subprocess.call(['python', r'C:\\Genesis\\Headquarter\\RD\\Main_Engine.py'])

if __name__ == "__main__":
    launch_empire()