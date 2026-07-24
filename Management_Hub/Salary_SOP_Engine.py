# C:\Genesis\Management_Hub\Salary_SOP_Engine.py
import pandas as pd
import os

class SalarySOPEngine:
    def __init__(self, data_path):
        self.data_path = data_path

    def load_files(self, file_patterns):
        """標準化載入機制：自動掃描指定目錄的 CSV 檔案"""
        data_frames = {}
        for pattern in file_patterns:
            # 這裡整合了您提到的「抓取i仁寶Excel資料」的標準程序
            file_path = os.path.join(self.data_path, pattern)
            if os.path.exists(file_path):
                data_frames[pattern] = pd.read_csv(file_path)
        return data_frames

    def process_payroll_logic(self, df_service, df_split, df_total):
        """核心標準化程序 (Stored Procedure)"""
        # 1. 邏輯對接：將三張表以「姓名」合併
        merged_df = pd.merge(df_service, df_split, on="姓名", how="outer")
        
        # 2. 公式邏輯化 (在此處編寫標準化公式)
        # 未來若有新專案，僅需在此更換公式字典
        merged_df['應領總額'] = merged_df['本薪'] + merged_df['服務產值'] + merged_df['加班費']
        merged_df['應扣總額'] = merged_df['勞保'] + merged_df['健保'] + merged_df['所得稅']
        merged_df['實發薪資'] = merged_df['應領總額'] - merged_df['應扣總額']
        
        return merged_df

# 使用範例 (未來自動化流程的一部分)
if __name__ == "__main__":
    engine = SalarySOPEngine(r"C:\Genesis\Data\Payroll_Inbox")
    print("[SOP] 標準薪資引擎已初始化，準備進行舉一反三的邏輯運算。")