# -*- coding: utf-8 -*-
"""
====================================================================
龍蝦帝國核心系統 - Gemini 實體沙盒防禦牆主權加固版 (Safe_Sandbox_Guard.py)
最高指揮官: 林雋懋 (Chun Mao Lin) | 總指揮官線程: 志玲 V3-Expert
剛性憲法：鎖定操作範圍於 Test 目錄，特許放行帝國核心 Database 安全下沉，消滅內耗死鎖
====================================================================
"""
import os

# 剛性死鎖的唯一合法一般操作邊界
STRICT_SANDBOX_DIR = r"C:\Genesis\SDK\Test"

# 【主權特許優化】：新增核心資產資料庫與日誌合法授權邊界，拒絕系統自我熔斷
STRICT_DATABASE_DIR = r"C:\Genesis\Database"
STRICT_LOGS_DIR = r"C:\Genesis\logs"

def verify_sandbox_boundary(target_path):
    """
    【Node A 邊界穿透校驗 - 主權加固版】
    剛性檢查企圖操作的實體路徑。
    允許範圍：
      1. C:\Genesis\SDK\Test (一般自動化產出與測試)
      2. C:\Genesis\Database (核心 SQLite 共同記憶庫落地)
      3. C:\Genesis\logs (看門狗與網閘實時運行日誌)
    若越界或使用相對路徑偽裝，一律沒收操作權，回報 0xFF_AUTH_BLOCK。
    """
    try:
        # 1. 全量轉為絕對路徑，瓦解相對路徑穿透
        absolute_target = os.path.abspath(target_path).lower()
        
        sandbox_bound = os.path.abspath(STRICT_SANDBOX_DIR).lower()
        database_bound = os.path.abspath(STRICT_DATABASE_DIR).lower()
        logs_bound = os.path.abspath(STRICT_LOGS_DIR).lower()
        
        # 2. 檢查惡意跳點特徵
        if ".." in target_path or "./" in target_path:
            return {
                "status": "0xFF_AUTH_BLOCK",
                "facts": f"惡意路徑跳點特徵遭攔截: {target_path}"
            }
            
        # 3. 逐層核對授權邊界 फैक्ट्स (Facts)
        if absolute_target.startswith(sandbox_bound):
            return {
                "status": "0x00_HEALTHY",
                "facts": f"合法沙盒內操作: {absolute_target}"
            }
        elif absolute_target.startswith(database_bound):
            return {
                "status": "0x00_HEALTHY",
                "facts": f"核心主權授權：允許資料庫寫入: {absolute_target}"
            }
        elif absolute_target.startswith(logs_bound):
            return {
                "status": "0x00_HEALTHY",
                "facts": f"核心主權授權：允許系統日誌寫入: {absolute_target}"
            }
            
        # 4. 未命中任何授權邊界，判定逃逸違規
        return {
            "status": "0xFF_AUTH_BLOCK",
            "facts": f"越界違規！企圖存取未授權外部路徑: {target_path}"
        }
        
    except Exception as e:
        return {
            "status": "0x99_SYSTEM_HALT",
            "facts": f"沙盒校驗器內部崩潰: {str(e)}"
        }

def safe_write_file(target_path, content):
    """受保護的地端實體寫入 API（具備強制緩衝刷新，消滅 0KB 漏洞）"""
    guard_result = verify_sandbox_boundary(target_path)
    
    if guard_result["status"] != "0x00_HEALTHY":
        print(f"[🚨 SECURITY ALERT] {guard_result['facts']} -> 拒絕物理寫入！")
        return "0xFF_AUTH_BLOCK"
        
    try:
        # 動態確保標的目錄存在
        target_dir = os.path.dirname(target_path)
        os.makedirs(target_dir, exist_ok=True)
            
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(content)
            f.flush()  # QE 剛性要求：強制將緩衝區數據下沉磁碟，從物理端絕殺 0KB 檔案
            
        print(f"[✓] 主權安全寫入成功: {target_path}")
        return "0x00_SUCCESS"
    except Exception as e:
        print(f"[❌ FATAL] 物理寫入失敗: {str(e)}")
        return "0x500_WRITE_FAILED"

if __name__ == "__main__":
    print("============================================================")
    print("        龍蝦帝國：Gemini 物理沙盒防禦牆邊界撥測 (加固版)    ")
    print("============================================================")
    
    # 測試點 1：合法沙盒內寫入
    test_legal = os.path.join(STRICT_SANDBOX_DIR, "demo_test.py")
    res1 = safe_write_file(test_legal, "# Legal sandbox code")
    print(f"撥測 1 結果: {res1}\n")
    
    # 測試點 2：核心特許資料庫寫入撥測
    test_db = os.path.join(STRICT_DATABASE_DIR, "archive_test.db")
    res2 = safe_write_file(test_db, "sqlite_binary_mock_data")
    print(f"撥測 2 結果: {res2}\n")
    
    # 測試點 3：惡意越界
    test_illegal = r"C:\Genesis\Upper_Sovereign_Manager.py"
    res3 = safe_write_file(test_illegal, "# Attack code")
    print(f"撥測 3 結果: {res3}")
    print("============================================================")