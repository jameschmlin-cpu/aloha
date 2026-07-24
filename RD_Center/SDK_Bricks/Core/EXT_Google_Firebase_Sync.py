# -*- coding: utf-8 -*-
# Compiled Brick from Plugin_Loader for EXT_Google_Firebase_Sync
# Category: External_Wrapper

import sys
import os

GENESIS_BASE = r"C:\Genesis"
if os.path.join(GENESIS_BASE, "RD_Center") not in sys.path:
    sys.path.insert(0, os.path.join(GENESIS_BASE, "RD_Center"))

from SDK.External_Modules.EXT_Google_Firebase_Sync import EXT_Google_Firebase_Sync
from SDK.Core.SDK_Core import Dashboard_Update_Hook

class EXT_Google_Firebase_Sync_Brick:
    def run(self, ctx=None):
        print("[*] Running compiled external brick wrapper for EXT_Google_Firebase_Sync")
        try:
            wrapper = EXT_Google_Firebase_Sync()
            result = wrapper.run(key='device_status', value='ONLINE')
            print(f"[EXT_Google_Firebase_Sync_Brick Success] Result: {result}")
            Dashboard_Update_Hook("EXT_Google_Firebase_Sync.py", "SUCCESS", f"Result: {result}")
            return True
        except Exception as e:
            print(f"[Error] EXT_Google_Firebase_Sync_Brick failed: {e}")
            Dashboard_Update_Hook("EXT_Google_Firebase_Sync.py", "FAILED", str(e))
            return False
