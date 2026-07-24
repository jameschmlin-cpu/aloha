# -*- coding: utf-8 -*-
# Compiled Brick from Plugin_Loader for EXT_Artistly_Image_Gen
# Category: External_Wrapper

import sys
import os

GENESIS_BASE = r"C:\Genesis"
if os.path.join(GENESIS_BASE, "RD_Center") not in sys.path:
    sys.path.insert(0, os.path.join(GENESIS_BASE, "RD_Center"))

from SDK.External_Modules.EXT_Artistly_Image_Gen import EXT_Artistly_Image_Gen
from SDK.Core.SDK_Core import Dashboard_Update_Hook

class EXT_Artistly_Image_Gen_Brick:
    def run(self, ctx=None):
        print("[*] Running compiled external brick wrapper for EXT_Artistly_Image_Gen")
        try:
            wrapper = EXT_Artistly_Image_Gen()
            result = wrapper.run()
            print(f"[EXT_Artistly_Image_Gen_Brick Success] Result: {result}")
            Dashboard_Update_Hook("EXT_Artistly_Image_Gen.py", "SUCCESS", f"Result: {result}")
            return True
        except Exception as e:
            print(f"[Error] EXT_Artistly_Image_Gen_Brick failed: {e}")
            Dashboard_Update_Hook("EXT_Artistly_Image_Gen.py", "FAILED", str(e))
            return False
