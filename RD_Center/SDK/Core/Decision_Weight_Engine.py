# 檔案：C:\Genesis\Genesis_Core\Decision_Weight_Engine.py

# 狀態：具備自動化權威判定的 AI 決策引擎



class DecisionEngine:

    def __init__(self):

        self.threshold = 80 # 決策閾值



    def evaluate_risk(self, cwe_id, system_context):

        # 根據 CWE 嚴重性與系統核心程度進行自動判定

        severity = self._get_cwe_severity(cwe_id) # 從資料庫提取權重

        context_weight = 10 if r"C:\Genesis" in system_context else 1

        

        final_score = severity * context_weight

        

        if final_score >= self.threshold:

            return "AUTO_EXECUTE", final_score

        else:

            return "LOG_AND_MONITOR", final_score



    def _get_cwe_severity(self, cwe_id):

        # 內建經驗法則數據庫

        return 90 if "Buffer" in cwe_id else 60

