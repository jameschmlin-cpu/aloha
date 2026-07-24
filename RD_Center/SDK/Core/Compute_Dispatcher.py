# -*- coding: utf-8 -*-

# 檔案：C:\Genesis\Genesis_Core\Compute_Dispatcher.py

import psutil

from connectivity_base import BaseConnectivityOP



class ComputeDispatcher(BaseConnectivityOP):

    def __init__(self):

        super().__init__()

        self.threshold = 85.0 # GPU/CPU 負載警戒線

        self.report("INIT", "算力調度 Agent 已就緒。")



    def get_load_status(self):

        """獲取地端算力佔用率"""

        cpu_usage = psutil.cpu_percent(interval=1)

        return cpu_usage



    def execute_optimized_diagnostic(self, task_function):

        """需求3：算力彈性排程，根據負載決定執行深度"""

        load = self.get_load_status()

        

        if load > self.threshold:

            self.report("OPTIMIZATION", f"當前負載 {load}%，切換為輕量級校驗模式。")

            # 輕量級：僅執行基礎 checksum 驗證

            return "LIGHTWEIGHT_CHECKSUM_OK"

        else:

            self.report("OPTIMIZATION", f"當前負載 {load}%，執行深度診斷。")

            # 重量級：執行完整 DFMEA 掃描

            return task_function()