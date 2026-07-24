# -*- coding: utf-8 -*-
# Compiled Brick from Plugin_Loader for EXT_Google_Search_Grounding
# Category: External_Wrapper

import sys
import os

GENESIS_BASE = r"C:\Genesis"
if os.path.join(GENESIS_BASE, "RD_Center") not in sys.path:
    sys.path.insert(0, os.path.join(GENESIS_BASE, "RD_Center"))

from SDK.External_Modules.EXT_Google_Search_Grounding import EXT_Google_Search_Grounding
from SDK.Core.SDK_Core import Dashboard_Update_Hook

class EXT_Google_Search_Grounding_Brick:
    def run(self, ctx=None):
        print("[*] Running compiled external brick wrapper for EXT_Google_Search_Grounding")
        try:
            wrapper = EXT_Google_Search_Grounding()
            result = wrapper.run(query='rtx 3060 latest driver windows')
            print(f"[EXT_Google_Search_Grounding_Brick Success] Result: {result}")
            Dashboard_Update_Hook("EXT_Google_Search_Grounding.py", "SUCCESS", f"Result: {result}")
            return True
        except Exception as e:
            print(f"[Error] EXT_Google_Search_Grounding_Brick failed: {e}")
            Dashboard_Update_Hook("EXT_Google_Search_Grounding.py", "FAILED", str(e))
            return False
