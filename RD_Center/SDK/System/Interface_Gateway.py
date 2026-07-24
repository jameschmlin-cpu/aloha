# 上層：確保用戶介面 (Gemini/Telegram) 與底層邏輯實體對接
class InterfaceGateway:
    def bridge(self, user_input):
        # 實體對接測試
        print(f"指令已掛載: {user_input}")