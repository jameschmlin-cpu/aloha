# --- 練兵實驗：軍團職能聯調 ---
from Universal_Genesis_Agent import UniversalGenesisAgent

# 徵召參謀長麾下部隊
company_agent = UniversalGenesisAgent()

def run_training_mission():
    print(">>> [一人公司練兵] 任務啟動...")
    
    # 1. PM_Agent 需求定義
    company_agent.skill_analyst() # 分析任務需求
    
    # 2. RD_Agent 開發編譯
    company_agent.skill_compiler() # 實體邏輯編譯
    
    # 3. QC_Agent 物理斷言 (關鍵：拒絕虛幻寫入)
    company_agent.skill_tester() # 進行 IO 落盤檢查
    
    # 4. Master_Commander 閉環歸檔
    company_agent.skill_sync() # 將執行紀錄鎖定至 Genesis_History.db
    
    print(">>> [一人公司練兵] 階段性任務完成。")

if __name__ == "__main__":
    run_training_mission()