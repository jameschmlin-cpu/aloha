# C:\Genesis\Startup_Loader.py

# 前端極簡：僅呼叫 SDK 總指揮官，不承載任何業務邏輯



import sys




# 將 C:\Genesis\SDK 加入系統路徑，確保模組可被呼叫

sys.path.append(r'C:\Genesis\SDK')



def start_empire_engine():

    try:

        from Orchestrator import EmpireOrchestrator

        # 啟動總指揮官，由 SDK 接管三大主題的調度

        engine = EmpireOrchestrator()

        engine.run()

    except Exception as e:

        # 若系統核心啟動失敗，記錄並觸發本地物理熔斷

        with open(r"C:\Genesis\Security\Audit\Startup_Error.log", "w") as f:

            f.write(f"Critical Failure: {str(e)}")



def start_empire_engine():

    try:

        from Orchestrator import EmpireOrchestrator

        # 初始化中央調度器，並同時掛載三大核心板塊

        engine = EmpireOrchestrator()

        engine.initialize_modules([

            "Monitoring_Core",    # 監控模組 (包含雲地/Telegram/Dashboard/秘書)

            "AI_Dispatcher",      # AI 中央調度器

            "Project_Engine"      # 帝國專案建設推進器

        ])

        engine.run_all_sync()     # 強制執行四位一體同步運行

    except Exception as e:

        # 實體熔斷，確保無效程式不會殘留

        with open(r"C:\Genesis\Security\Audit\Startup_Error.log", "w") as f:

            f.write(f"Critical System Coupling Error: {str(e)}")



if __name__ == "__main__":

    start_empire_engine()