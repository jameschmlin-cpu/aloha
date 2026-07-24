# -*- coding: utf-8 -*-
# Compiled Brick from Plugin_Loader for EXT_HWiNFO_Reader
# Category: External_Wrapper

import sys
import os

GENESIS_BASE = r"C:\Genesis"
if os.path.join(GENESIS_BASE, "RD_Center") not in sys.path:
    sys.path.insert(0, os.path.join(GENESIS_BASE, "RD_Center"))

from SDK.External_Modules.EXT_HWiNFO_Reader import EXT_HWiNFO_Reader
from SDK.Core.SDK_Core import Dashboard_Update_Hook

class EXT_HWiNFO_Reader_Brick:
    def run(self, ctx=None):
        print("[*] Running compiled external brick wrapper for EXT_HWiNFO_Reader")
        try:
            wrapper = EXT_HWiNFO_Reader()
            result = wrapper.run()
            print(f"[EXT_HWiNFO_Reader_Brick Success] Result: {result}")
            Dashboard_Update_Hook("EXT_HWiNFO_Reader.py", "SUCCESS", f"Result: {result}")
            return True
        except Exception as e:
            print(f"[Error] EXT_HWiNFO_Reader_Brick failed: {e}")
            Dashboard_Update_Hook("EXT_HWiNFO_Reader.py", "FAILED", str(e))
            return False
