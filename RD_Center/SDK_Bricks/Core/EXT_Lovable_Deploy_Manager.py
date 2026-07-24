# -*- coding: utf-8 -*-
# Compiled Brick from Plugin_Loader for EXT_Lovable_Deploy_Manager
# Category: External_Wrapper

import sys
import os

GENESIS_BASE = r"C:\Genesis"
if os.path.join(GENESIS_BASE, "RD_Center") not in sys.path:
    sys.path.insert(0, os.path.join(GENESIS_BASE, "RD_Center"))

from SDK.External_Modules.EXT_Lovable_Deploy_Manager import EXT_Lovable_Deploy_Manager
from SDK.Core.SDK_Core import Dashboard_Update_Hook

class EXT_Lovable_Deploy_Manager_Brick:
    def run(self, ctx=None):
        print("[*] Running compiled external brick wrapper for EXT_Lovable_Deploy_Manager")
        try:
            wrapper = EXT_Lovable_Deploy_Manager()
            result = wrapper.run(project_id='genesis-dashboard-pro', commit_msg='Deploy hotfix for SSE push connection delay')
            print(f"[EXT_Lovable_Deploy_Manager_Brick Success] Result: {result}")
            Dashboard_Update_Hook("EXT_Lovable_Deploy_Manager.py", "SUCCESS", f"Result: {result}")
            return True
        except Exception as e:
            print(f"[Error] EXT_Lovable_Deploy_Manager_Brick failed: {e}")
            Dashboard_Update_Hook("EXT_Lovable_Deploy_Manager.py", "FAILED", str(e))
            return False
