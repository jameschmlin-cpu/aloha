# 模擬執行閉環審計：C:\Genesis\RD_Center\Source\Audit_Engine.py
from Source.Gemini_Secretary import Gemini_Secretary

def run_closed_loop_audit():
    print("--- [Audit] 啟動系統閉環審計 ---")
    app = Gemini_Secretary()
    
    # 模擬 S1-S4 完整調用
    try:
        app.S1_Communication()
        app.S2_Registry()
        app.S3_Command_Center()
        
        # 核心審計：檢查 S4 是否能成功讀取並防禦
        status = app.S4_Monitor_Defense()
        
        if status:
            print("--- [Audit] 審計結果：閉環完整，邏輯無漏洞 ---")
        else:
            print("--- [Audit] 審計結果：偵測到邏輯熔斷 (防禦機制啟動) ---")
            
    except Exception as e:
        print(f"--- [Audit] 偵測到架構漏洞: {str(e)} ---")

if __name__ == "__main__":
    run_closed_loop_audit()