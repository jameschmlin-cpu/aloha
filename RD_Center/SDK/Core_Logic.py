# Category: Logic
# 物理層指令：初始化 Webmcp 接管通道
import subprocess

def activate_webmcp_bridge():
    mcp_script = r"C:\Genesis\Library\SDK\Webmcp_Core.py"
    # 使用 Python 物理執行，確保 Webmcp 保持運作並掛載 SDK
    proc = subprocess.Popen(["python", mcp_script], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    print(f"[MOUNTED] Webmcp PID: {proc.pid} | 通道已對接至 ITE 本地端")

activate_webmcp_bridge()