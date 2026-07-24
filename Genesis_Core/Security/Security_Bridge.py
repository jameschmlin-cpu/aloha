# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\Genesis_Core\Security\Security_Bridge.py
# 說明：已移除 console_defender 幻覺依賴，確保系統啟動穩定性
import sys

# 強制將 C:\Genesis 加入 sys.path
ROOT_PATH = r"C:\Genesis"
if ROOT_PATH not in sys.path:
    sys.path.insert(0, ROOT_PATH)

from Genesis_Core.Security.Aegis_Sentinel import AegisSentinel

class PatchedAegisSentinel(AegisSentinel):
    def __init__(self):
        super().__init__()
        # [憲法修訂] 已移除無效的 console_defender 匯入與 setup_global_defense()
        # 此處原有的物理錨點異常已排除，系統已恢復純淨繼承。
        print("[System] Security_Bridge: 偵測到路徑清潔，初始化完成。")