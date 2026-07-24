# -*- coding: utf-8 -*-

# 檔案：C:\Genesis\Genesis_Core\Test_Defense_Logic.py

# 狀態：失效模式與效果模擬測試 (DFMEA Stress Test)



class DefenseSimulator:

    def __init__(self, doctor):

        self.doctor = doctor



    def run_stress_test(self, mock_virus_path):

        # 模擬 DFMEA 風險偵測

        risk = self.doctor.dfmea_guard.check_risk(mock_virus_path)

        print(f"[模擬] 偵測到路徑: {mock_virus_path}, 風險等級: {risk}")

        

        if risk > 0.8:

            # 必須同時調用 Audit 與 Guardian

            self.doctor.report("TEST", "執行防禦協議")

            self.doctor._dispatch_audit(mock_virus_path)

            self.doctor._dispatch_guardian(mock_virus_path)

            return True

        return False