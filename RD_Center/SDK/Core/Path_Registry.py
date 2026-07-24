# -*- coding: utf-8 -*-

# 檔案：C:\Genesis\Genesis_Core\Path_Registry.py

# 狀態：路徑唯一真值來源 (Single Source of Truth)



class PathRegistry:

    # 定義帝國全系統實體路徑映射

    PATHS = {

        "ROOT": r"C:\Genesis",

        "SECURITY": r"C:\Genesis\Genesis_Core\Security",

        "MODULES": r"C:\Genesis\Genesis_Core\Modules",

        "DATA": r"C:\Genesis\Genesis_Core\Data",

        "LOGS": r"C:\Genesis\Genesis_Core\Logs",

        "GUARDIAN_BOT": r"Genesis_Core.Security.Guardian_Bot",

         "BASE": r"C:\Genesis\SDK\Base",

         "DOCTOR": r"C:\Genesis\SDK\Doctor",

         "LIBRARY": r"C:\Genesis\Library\LibrarySystem",

        "SECRETARY_MODULE": r"Genesis_Core.Modules.Secretary_Module"

    }



    @classmethod

    def get(cls, key):

        return cls.PATHS.get(key)