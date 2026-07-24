# C:\Genesis\docker_auto_repair.py
import subprocess
import os
import psutil

class DockerAutoRepairAgent:
    def __init__(self):
        self.target_path = r"C:\Genesis"

    def execute_command(self, cmd: str):
        print(f"[執行指令]: {cmd}")
        process = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if process.stdout:
            print(process.stdout)
        if process.stderr:
            print(f"[訊息/錯誤]: {process.stderr}")
        return process.returncode

    def repair_docker_backend(self):
        print("[自動修復] 偵測到 Docker 後端異常 (exit status 1)，正在啟動自動修復程序...")
        
        # 1. 強制終止所有背景 Docker 行程
        print("[處理 1/4] 清理殘留的 Docker 背景行程...")
        for proc in psutil.process_iter(['name', 'pid']):
            try:
                name = proc.info['name']
                if name and any(keyword in name.lower() for keyword in ['docker', 'com.docker']):
                    print(f"終止行程: {name} (PID: {proc.info['pid']})")
                    proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        # 2. 執行 WSL 關閉與解除註冊損毀的虛擬機器
        print("[處理 2/4] 重置 WSL 2 容器發行版狀態...")
        self.execute_command("wsl --shutdown")
        self.execute_command("wsl --unregister docker-desktop")
        self.execute_command("wsl --unregister docker-desktop-data")

        # 3. 確保核心虛擬化服務運行
        print("[處理 3/4] 啟動 Windows 虛擬化核心服務...")
        self.execute_command("net start vmcompute")
        self.execute_command("net start com.docker.service")

        # 4. 完成提示
        print("[處理 4/4] Docker 後端重置完成。")
        print("[Node C 實體驗證] 請以系統管理員身分重新開啟 Docker Desktop，系統將自動重建乾淨的後端環境。")

if __name__ == "__main__":
    agent = DockerAutoRepairAgent()
    agent.repair_docker_backend()