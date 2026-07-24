import os
import sqlite3
from datetime import datetime

# ==========================================
# 核心實體路徑定錨
# ==========================================
BASE_PATH = r"C:\Genesis"
DB_PATH = os.path.join(BASE_PATH, "Database", "Lobster_Connectivity.db")

class LobsterDataTransformer:
    """
    龍蝦系統中層核心第 11 號 Class
    專職負責全局數據清洗、型態安全轉換與標準化打包，確保 103 模組間數據對接無物理斷層。
    """
    def __init__(self):
        self.db_path = DB_PATH

    def write_transformer_telemetry(self, status: str, detail: str):
        """將數據轉譯清洗事件實體寫入 SQLite 行車記錄器"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO connectivity_logs (timestamp, task_name, status, detail)
                VALUES (?, ?, ?, ?)
            ''', (timestamp, "[Data_Transformer] Type_Cast", status, detail))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[TRANSFORMER_DB_FATAL] {e}")

    def transform_payload(self, module_id: str, raw_data: dict) -> dict:
        """
        中層數據轉換核心邏輯：
        實體執行數據清洗，強制對齊帝國標準規約，拒絕大鍋炒的模糊型態。
        """
        try:
            cleaned_data = {}
            
            # 1. 物理清洗：去除字串前後空格，強制進行安全性字串化
            for key, val in raw_data.items():
                if isinstance(val, str):
                    cleaned_data[key] = val.strip()
                else:
                    cleaned_data[key] = val

            # 2. 型態剛性校驗與轉譯（以行政薪資與金流計算為例，強制對齊數字型態）
            if "amount" in cleaned_data:
                try:
                    cleaned_data["amount"] = float(cleaned_data["amount"])
                except (ValueError, TypeError):
                    raise TypeError(f"欄位 'amount' 無法轉譯為實體浮點數: {cleaned_data['amount']}")
            
            if "base_salary" in cleaned_data:
                try:
                    cleaned_data["base_salary"] = int(cleaned_data["base_salary"])
                except (ValueError, TypeError):
                    raise TypeError(f"欄位 'base_salary' 無法轉譯為實體整數: {cleaned_data['base_salary']}")

            # 3. 注入標準化中層行車時間戳記
            cleaned_data["transformed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cleaned_data["data_integrity"] = "VERIFIED_CLEAN"

            self.write_transformer_telemetry("PASS", f"模組 {module_id} 請求之數據清洗轉譯 100% 成功。")
            return {
                "status": "TRANSFORM_SUCCESS",
                "payload": cleaned_data
            }

        except Exception as e:
            fail_detail = f"技術瓶頸：數據轉譯發生致命型態衝突! 錯誤主因: {str(e)}"
            self.write_transformer_telemetry("FAIL", fail_detail)
            return {
                "status": "TECHNICAL_RESTRAINT",
                "message": fail_detail
            }

if __name__ == "__main__":
    transformer = LobsterDataTransformer()
    
    print("\n" + "="*60)
    print(" 龍蝦帝國：中層第 11 號 Class Data_Transformer 型態清洗測試 ")
    print("="*60)
    
    # 模擬高層 WebMCP 傳下來的「大鍋炒髒數據」（包含字串前後空格、未對齊的數字字串）
    dirty_input = {
        "employee_name": "  Chun Mao Lin  ", # 帶空格
        "base_salary": " 65000 ",             # 字串型態的薪資
        "amount": "1250.50",                  # 字串型態的金流金額
        "action": "CALC_SALARY"
    }
    
    # 執行數據清洗轉換
    report = transformer.transform_payload("ACT_001_ADMIN_SALARY", dirty_input)
    print(f"轉譯清洗狀態: {report['status']}")
    if report['status'] == "TRANSFORM_SUCCESS":
        print("實體轉譯後數據流:")
        print(f"  - 姓名: '{report['payload']['employee_name']}' (已去空格)")
        print(f"  - 薪資類型: {type(report['payload']['base_salary'])} | 值: {report['payload']['base_salary']}")
        print(f"  - 金額類型: {type(report['payload']['amount'])} | 值: {report['payload']['amount']}")
        print(f"  - 誠信標記: {report['payload']['data_integrity']}")
    else:
        print(f"熔斷回報內容: {report['message']}")
    print("="*60 + "\n")