# C:\Genesis\Genesis_Core\Full_Empire_Integration.py

import sys

sys.path.append(r"C:\Genesis\Genesis_Core")



from Hermes_Kernel import HermesKernel

from Bridge.Empire_Unified_Bridge import Empire_Unified_Bridge



class FullEmpireSystem:

    def __init__(self):

        self.kernel = HermesKernel()

        self.bridge = Empire_Unified_Bridge()

    

    def full_power_on(self):

        # 啟動內核

        self.kernel.boot()

        # 驗證橋樑通訊

        status = self.bridge.bridge_handshake("SYS_FULL_INT")

        print(f"【系統狀態】{status}")

        print("【全功能運作】導通完成。")



if __name__ == "__main__":

    system = FullEmpireSystem()

    system.full_power_on()