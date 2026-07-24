# 邏輯預覽：薪資處理核心引擎
import pandas as pd

class LobsterPayrollEngine:
    def __init__(self, file_paths):
        self.files = file_paths
        
    def execute_merge(self):
        # 讀取三個 Excel
        df1 = pd.read_excel(self.files[0]) # 薪資原始數據
        df2 = pd.read_excel(self.files[1]) # 出勤數據
        df3 = pd.read_excel(self.files[2]) # 保險扣繳
        
        # 邏輯合併：嚴格依照員工 ID 進行 Inner Join
        final_table = pd.merge(df1, df2, on='Employee_ID').merge(df3, on='Employee_ID')
        
        # 產出最終報表
        final_table.to_excel("Final_Payroll_Master.xlsx", index=False)
        return "SUCCESS"