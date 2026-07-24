# -*- coding: utf-8 -*-
# Compiled Brick from Plugin_Loader for EXT_MS_Azure_Blob_Storage
# Category: External_Wrapper

import sys
import os

GENESIS_BASE = r"C:\Genesis"
if os.path.join(GENESIS_BASE, "RD_Center") not in sys.path:
    sys.path.insert(0, os.path.join(GENESIS_BASE, "RD_Center"))

from SDK.External_Modules.EXT_MS_Azure_Blob_Storage import EXT_MS_Azure_Blob_Storage
from SDK.Core.SDK_Core import Dashboard_Update_Hook

class EXT_MS_Azure_Blob_Storage_Brick:
    def run(self, ctx=None):
        print("[*] Running compiled external brick wrapper for EXT_MS_Azure_Blob_Storage")
        try:
            wrapper = EXT_MS_Azure_Blob_Storage()
            result = wrapper.run(file_path='C:\\Genesis\\Genesis_Core\\System_Audit.log', container='telemetry-logs')
            print(f"[EXT_MS_Azure_Blob_Storage_Brick Success] Result: {result}")
            Dashboard_Update_Hook("EXT_MS_Azure_Blob_Storage.py", "SUCCESS", f"Result: {result}")
            return True
        except Exception as e:
            print(f"[Error] EXT_MS_Azure_Blob_Storage_Brick failed: {e}")
            Dashboard_Update_Hook("EXT_MS_Azure_Blob_Storage.py", "FAILED", str(e))
            return False
