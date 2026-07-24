# -*- coding: utf-8 -*-
# Compiled Brick from Plugin_Loader for EXT_MS_Azure_IoT_Device
# Category: External_Wrapper

import sys
import os

GENESIS_BASE = r"C:\Genesis"
if os.path.join(GENESIS_BASE, "RD_Center") not in sys.path:
    sys.path.insert(0, os.path.join(GENESIS_BASE, "RD_Center"))

from SDK.External_Modules.EXT_MS_Azure_IoT_Device import EXT_MS_Azure_IoT_Device
from SDK.Core.SDK_Core import Dashboard_Update_Hook

class EXT_MS_Azure_IoT_Device_Brick:
    def run(self, ctx=None):
        print("[*] Running compiled external brick wrapper for EXT_MS_Azure_IoT_Device")
        try:
            wrapper = EXT_MS_Azure_IoT_Device()
            result = wrapper.run(data_payload='{"temperature": 24.5}')
            print(f"[EXT_MS_Azure_IoT_Device_Brick Success] Result: {result}")
            Dashboard_Update_Hook("EXT_MS_Azure_IoT_Device.py", "SUCCESS", f"Result: {result}")
            return True
        except Exception as e:
            print(f"[Error] EXT_MS_Azure_IoT_Device_Brick failed: {e}")
            Dashboard_Update_Hook("EXT_MS_Azure_IoT_Device.py", "FAILED", str(e))
            return False
