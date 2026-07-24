# Category: Network
import subprocess
import os

def connect_webmcp():
    mcp_path = r'C:\Genesis\Library\SDK\Webmcp_Core.py'
    if os.path.exists(mcp_path):
        # 物理啟動掛載
        subprocess.Popen(['python', mcp_path], creationflags=subprocess.CREATE_NO_WINDOW)
        with open(r'C:\Genesis\activity.log', 'a') as f:
            f.write('[MOUNT] Webmcp Heartbeat: Online\n')
    else:
        with open(r'C:\Genesis\activity.log', 'a') as f:
            f.write('[ERROR] Webmcp Core missing during mount\n')

if __name__ == '__main__':
    connect_webmcp()
