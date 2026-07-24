# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\RD_Center\SDK\System\lobster_bridge_32.py
# 需由 32-bit Python 執行，對接 32-bit lobster_core.pyd 並提供 JSON-RPC Over Stdin/Stdout IPC
import sys
import json
import os

# 將當前目錄加入 sys.path 以利載入 lobster_core
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import lobster_core
    has_lobster = True
except Exception as e:
    has_lobster = False
    error_msg = str(e)

def main():
    if not has_lobster:
        sys.stderr.write(f"FATAL: Unable to import lobster_core: {error_msg}\n")
        sys.exit(1)
        
    # 循環讀取 stdin 進行 IPC 通訊
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            request = json.loads(line.strip())
            cmd = request.get("cmd")
            payload = request.get("payload")
            
            if hasattr(lobster_core, cmd):
                func = getattr(lobster_core, cmd)
                # 執行指令並獲取結果
                result = func(payload)
                response = {"status": "SUCCESS", "payload": result}
            else:
                response = {"status": "ERROR", "message": f"Symbol {cmd} not found in lobster_core"}
        except Exception as e:
            response = {"status": "ERROR", "message": str(e)}
            
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()