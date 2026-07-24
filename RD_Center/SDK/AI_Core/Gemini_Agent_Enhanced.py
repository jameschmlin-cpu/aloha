# 檔案：C:\Genesis\RD_Center\SDK\AI_Core\Gemini_Agent_Enhanced.py
import json
import datetime
from Gemini_Agent import GeminiAgent

class GeminiAgentEnhanced(GeminiAgent):
    def execute_free_instruction(self, user_instruction, telemetry_context=None):
        # 自動路由邏輯：檢查日期是否小於 2026-07-14
        now = datetime.datetime.now()
        limit_date = datetime.datetime(2026, 7, 14)
        
        if now < limit_date:
            print(f"[Node A] 系統偵測：雲端限制期間 ({now.strftime('%m/%d')} < 07/14)，強制啟動 RTX 3060 本地接管。")
            return self._call_local_ollama(user_instruction, "You are Genesis AI Cognitive Governor.")
        
        # 若過了 7/14，恢復原有的自動分流機制
        print("[Node A] 系統偵測：雲端服務恢復，啟用自動路由。")
        return super().execute_free_instruction(user_instruction, telemetry_context)

if __name__ == "__main__":
    agent = GeminiAgentEnhanced()
    print("[Node C] 執行自動路由測試...")
    res = agent.execute_free_instruction("系統狀態檢測")
    print(f"\n[Node C 回傳狀態]:\n{json.dumps(res, indent=4, ensure_ascii=False)}")