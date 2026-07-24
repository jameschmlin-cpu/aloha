# -*- coding: utf-8 -*-

# 檔案路徑：C:\Genesis\Genesis_Core\Empire_Command_Center.py



import hashlib

import time



from Stage4.Safety_Referee import Safety_Referee

from Empire_Base_SDK import EmpireBaseSDK

from Memory_Interface import Memory_Interface



class Empire_Command_Center(Safety_Referee):

    def __init__(self, dispatcher, dfmea_engine):

        super().__init__()

        self.dispatcher = dispatcher

        self.dfmea_engine = dfmea_engine

        self.sdk = EmpireBaseSDK()

        self.memory = Memory_Interface() 

        

        # [修正] 使用 raw string 防止路徑轉義錯誤

        self.mirror_path = r"D:\SystemBackUp\ITE_Mirror_Golden"

        self.target_path = r"C:\Genesis\Genesis_Core"

        self.maintenance_active = False

        

        self.last_check_time = 0

        self.check_interval = 60

        self._start_guardian_thread()



    # [修復] 統一縮排層級，確保邏輯閉環

    def execute_empire_tasks(self, context, tid):

        """執行核心任務，並統一縮排標準"""

        def action_to_execute():

            # 物理調度邏輯

            strategy = self.process_reflex("EVENT_EXEC", context)

            agent_map = {"STP_HARDENED_SHIELD": "Guard Board", "STP_STANDARD_RUN": "Secretary"}

            target_agent = agent_map.get(strategy)



            if target_agent:

                result = self.sdk.invoke_agent(target_agent)

                if result != 0:

                    self.audit_and_evolve("AGENT_FAILURE", tid)

                    return False

                return True

            return self.dispatcher.execute(context, tid)



        trace_id = hashlib.sha256(str(time.time()).encode()).hexdigest()

        result = self.memory.execute_with_lock(

            service_name="Empire_Dispatcher",

            action_func=action_to_execute,

            context=context,

            trace_id=trace_id

        )

        

        if result is None:

            self.log_event("LOCK_DENIED", "系統鎖定中，拒絕調度。")

            return False

            

        return result