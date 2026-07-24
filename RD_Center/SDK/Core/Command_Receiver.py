# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\RD_Center\SDK\Core\Command_Receiver.py
# 狀態：AG Command_Receiver 遙控命令接收端 - 支援緊急重啟與任務重試

import sys
import os
import subprocess

GENESIS_BASE = r"C:\Genesis"

def handle_command(cmd_type, payload=None):
    print(f"[Command_Receiver] Processing command: {cmd_type}")
    
    if cmd_type == "EMERGENCY_RESTART":
        log_file = os.path.join(GENESIS_BASE, "Genesis_Core", "DFMEA_Monitor.log")
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        with open(log_file, "a", encoding="utf-8") as f:
            f.write("[INFO] [Remote Command] EMERGENCY_RESTART triggered.\n")
            
        boot_script = os.path.join(GENESIS_BASE, "Genesis_Bootstrapper.bat")
        if os.path.exists(boot_script):
            # Run bootstrapper batch in a new console asynchronously
            subprocess.Popen([boot_script], creationflags=subprocess.CREATE_NEW_CONSOLE)
            return True, "Emergency restart sequence successfully dispatched."
        else:
            return False, f"Bootstrapper script not found at: {boot_script}"
            
    elif cmd_type == "TASK_RETRY":
        log_file = os.path.join(GENESIS_BASE, "Genesis_Core", "DFMEA_Monitor.log")
        last_failed_brick = None
        
        # Method A: check DFMEA_Monitor.log for failed runs
        if os.path.exists(log_file):
            try:
                with open(log_file, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                for line in reversed(lines):
                    if "[執行失敗]" in line or "Error" in line or "failed" in line:
                        # Simple name check e.g. EXT_MS_Azure_IoT_Device.py
                        import re
                        match = re.search(r"(\w+\.py)", line)
                        if match:
                            last_failed_brick = match.group(1)
                            break
            except Exception:
                pass
                
        # Method B: fallback to checking empire_execution.log
        if not last_failed_brick:
            execution_log = os.path.join(GENESIS_BASE, "Logs", "empire_execution.log")
            if os.path.exists(execution_log):
                try:
                    with open(execution_log, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                    for line in reversed(lines):
                        if "[執行失敗]" in line:
                            parts = line.strip().split()
                            for part in parts:
                                if part.endswith(".py") or part.replace(".py", ""):
                                    last_failed_brick = part
                                    if not last_failed_brick.endswith(".py"):
                                        last_failed_brick += ".py"
                                    break
                            if last_failed_brick:
                                break
                except Exception:
                    pass

        if not last_failed_brick:
            # Absolute default fallback
            last_failed_brick = "Robot_Movement.py"
            
        # Strip path prefix if any
        last_failed_brick = os.path.basename(last_failed_brick)
        print(f"[Command_Receiver] Last failed brick resolved to: {last_failed_brick}")
        
        # Locate files in SDK_Bricks
        bricks_dir = os.path.join(GENESIS_BASE, "RD_Center", "SDK_Bricks")
        found_path = None
        for root, _, files in os.walk(bricks_dir):
            for f in files:
                if f.lower() == last_failed_brick.lower() or f.lower().replace(".py", "") == last_failed_brick.lower().replace(".py", ""):
                    found_path = os.path.join(root, f)
                    break
            if found_path:
                break
                
        if found_path:
            subprocess.Popen([sys.executable, found_path])
            return True, f"Retrying task execution for brick: {last_failed_brick}"
        else:
            return False, f"Could not find brick script file: {last_failed_brick}"
            
    return False, "Invalid command code."

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        ok, msg = handle_command(cmd)
        print(f"Status: {ok} | Message: {msg}")
