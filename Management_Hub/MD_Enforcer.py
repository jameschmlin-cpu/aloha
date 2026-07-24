import os

# 強制讀取 MD 憲法
PREF_PATH = r"C:\Genesis\Management_Hub\Preference.md"

def enforce_md_compliance(file_content):
    """
    MD 強制驗收：若發現程式碼未達「完整交付」標準，強制拒絕輸出。
    """
    if not os.path.exists(PREF_PATH):
        return False, "憲法文件不存在，請先建立 Preference.md。"
    
    with open(PREF_PATH, 'r', encoding='utf-8') as f:
        md_content = f.read()
        # 強制執行條款：檢查內容是否包含完整結構
        if "嚴禁產出部分程式碼" in md_content:
            # 檢查代碼片段是否過短或帶有省略符號
            if len(file_content) < 500 or "..." in file_content or "省略" in file_content:
                return False, "違反 MD 憲法：偵測到部分代碼或省略內容。"
                
    return True, "符合規範。"

# 測試用：在生成回覆前調用
if __name__ == "__main__":
    print("[MD Enforcer] 系統運作中，隨時待命執行強制檢查。")