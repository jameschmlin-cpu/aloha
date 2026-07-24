# -*- coding: utf-8 -*-

# 檔案：C:\Genesis\Genesis_Core\Kernel_Registry.py

# 狀態：實體化架構定義 (帝國系統的總指揮部)



import importlib

import logging



class KernelRegistry:

    """

    實作架構層級定義：

    1. Kernel 層：負責啟動與生命週期管理

    2. SDK 抽象層：定義模組必須遵循的介面 (perform_safety_check)

    3. 模組層：實際掛載的 SDK 物件

    """

    def __init__(self):

        self.registered_modules = {}

        logging.basicConfig(filename=r"C:\Genesis\Genesis_Core\logs\kernel.log", level=logging.INFO)



    def register_module(self, module_name, class_path):

        """將模組掛載進系統，不直接寫死在 Kernel 裡面"""

        try:

            module = importlib.import_module(module_name)

            module_class = getattr(module, class_path)

            self.registered_modules[module_name] = module_class()

            logging.info(f"[*] 模組 {module_name} 已透過 SDK 介面掛載成功。")

        except Exception as e:

            logging.error(f"[!] 模組掛載失敗: {e}")



    def dispatch_task(self, module_name, task_name):

        """Kernel 分發任務，透過 SDK 橋接器與模組對接"""

        if module_name in self.registered_modules:

            # 這裡實作了 SDK 抽象層的呼叫規範

            return self.registered_modules[module_name].perform_safety_check(task_name)

        return False



# 實體化註冊中心

registry = KernelRegistry()