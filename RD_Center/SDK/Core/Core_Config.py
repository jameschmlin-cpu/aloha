# -*- coding: utf-8 -*-

# 檔案：C:\Genesis\Genesis_Core\Core_Config.py

import os



class CoreConfig:

    ROOT = r"C:\Genesis\Genesis_Core"

    DATA = os.path.join(ROOT, "Data")

    DB_MEMORY = os.path.join(DATA, "Memory_Core")

    DB_LOG = os.path.join(DATA, "Unified_Empire_Memory")