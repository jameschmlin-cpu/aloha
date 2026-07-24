# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\Plugin_Loader.py
# 狀態：Plugin Loader 插件裝載中樞 - 自動封裝並登載新外部積木

import os
import json

GENESIS_BASE = r"C:\Genesis"
MODULES_DIR = os.path.join(GENESIS_BASE, "SDK", "External_Modules")
BRICKS_DIR = os.path.join(GENESIS_BASE, "RD_Center", "SDK_Bricks", "Core")
MANIFEST_PATH = os.path.join(GENESIS_BASE, "SDK", "block_manifest.json")

# Mapping of brick signatures to default test arguments
MOCK_SIGNATURE_ARGS = {
    "EXT_MS_Azure_IoT_Device": "data_payload='{\"temperature\": 24.5}'",
    "EXT_MS_Azure_Blob_Storage": "file_path='C:\\\\Genesis\\\\Genesis_Core\\\\System_Audit.log', container='telemetry-logs'",
    "EXT_Anthropic_Claude_Logic_Engine": "context='{\"system_status\": \"ACTIVE\"}', user_prompt='Refine system self-healing threshold'",
    "EXT_OpenAI_Vision_API": "image_path='C:\\\\Genesis\\\\Temp\\\\camera_snap.png', prompt='Detect visual abnormalities in device panel'",
    "EXT_Google_Search_Grounding": "query='rtx 3060 latest driver windows'",
    "EXT_Google_Vertex_AI_Selector": "task_type='NLP_TRANSLATION'",
    "EXT_Google_Firebase_Sync": "key='device_status', value='ONLINE'",
    "EXT_Lovable_Deploy_Manager": "project_id='genesis-dashboard-pro', commit_msg='Deploy hotfix for SSE push connection delay'",
    "EXT_Replit_Code_Assist": "code_context='def execute_job(): pass', action='Add exception handling block'"
}

def compile_brick_wrapper(module_name):
    class_name = module_name
    brick_class_name = f"{module_name}_Brick"
    args = MOCK_SIGNATURE_ARGS.get(class_name, "")
    
    wrapper_code = f"""# -*- coding: utf-8 -*-
# Compiled Brick from Plugin_Loader for {class_name}
# Category: External_Wrapper

import sys
import os

GENESIS_BASE = r"C:\\Genesis"
if os.path.join(GENESIS_BASE, "RD_Center") not in sys.path:
    sys.path.insert(0, os.path.join(GENESIS_BASE, "RD_Center"))

from SDK.External_Modules.{class_name} import {class_name}
from SDK.Core.SDK_Core import Dashboard_Update_Hook

class {brick_class_name}:
    def run(self, ctx=None):
        print("[*] Running compiled external brick wrapper for {class_name}")
        try:
            wrapper = {class_name}()
            result = wrapper.run({args})
            print(f"[{brick_class_name} Success] Result: {{result}}")
            Dashboard_Update_Hook("{module_name}.py", "SUCCESS", f"Result: {{result}}")
            return True
        except Exception as e:
            print(f"[Error] {brick_class_name} failed: {{e}}")
            Dashboard_Update_Hook("{module_name}.py", "FAILED", str(e))
            return False
"""
    
    os.makedirs(BRICKS_DIR, exist_ok=True)
    brick_path = os.path.join(BRICKS_DIR, f"{module_name}.py")
    with open(brick_path, "w", encoding="utf-8") as f:
        f.write(wrapper_code)
    print(f"[Plugin_Loader] Generated brick wrapper: {brick_path}")
    return brick_path

def register_in_manifest(brick_absolute_path, module_name):
    # Normalize paths for Windows JSON manifest format
    normalized_path = os.path.abspath(brick_absolute_path)
    
    if os.path.exists(MANIFEST_PATH):
        try:
            with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
                manifest = json.load(f)
        except Exception:
            manifest = []
    else:
        manifest = []
        
    # Check if entry already exists
    exists = False
    for entry in manifest:
        if entry.get("path", "").lower() == normalized_path.lower():
            exists = True
            break
            
    if not exists:
        manifest.append({
            "path": normalized_path,
            "intent": {
                "classes": [f"{module_name}_Brick"],
                "methods": ["run"]
            }
        })
        try:
            with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
                json.dump(manifest, f, indent=4, ensure_ascii=False)
            print(f"[Plugin_Loader] Registered {module_name} in manifest database.")
        except Exception as e:
            print(f"[Plugin_Loader] Manifest write failed: {e}")

def run_loader():
    print("=== [Plugin Loader: External Wrapper Mounting Core] ===")
    if not os.path.exists(MODULES_DIR):
        print(f"[Warning] Modules directory not found: {MODULES_DIR}")
        return
        
    for filename in os.listdir(MODULES_DIR):
        if filename.startswith("EXT_") and filename.endswith(".py"):
            module_name = filename.replace(".py", "")
            brick_file_path = compile_brick_wrapper(module_name)
            register_in_manifest(brick_file_path, module_name)
            
    print("=== [Plugin Mounting Sequence Completed Successfully] ===")

if __name__ == "__main__":
    run_loader()
