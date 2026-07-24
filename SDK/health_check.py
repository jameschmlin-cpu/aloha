# -*- coding: utf-8 -*-
# C:\Genesis\SDK\health_check.py
# Genesis 系統健康診斷與自癒觸發模組

import subprocess
import os
import sys
import logging
import datetime
import socket

# --- 核心配置 ---
GENESIS_BASE = r"C:\Genesis"
LOG_FILE = os.path.join(GENESIS_BASE, "Logs", "patch_audit.log")
TARGET_MODULE = os.path.join(GENESIS_BASE, "SDK", "target_module.py")
TEST_SCRIPT = os.path.join(GENESIS_BASE, "tests", "test_module.py")

# 確保日誌路徑存在
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    encoding='utf-8')

def run_cmd(cmd, cwd=GENESIS_BASE):
    """執行 Shell 指令的標準輔助函數"""
    try:
        return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=5.0)
    except Exception as e:
        class DummyProc:
            returncode = -1
            stdout = ""
            stderr = str(e)
        return DummyProc()

def check_directories():
    """確認系統必備目錄完整性"""
    required_paths = [
        os.path.join(GENESIS_BASE, "RD_Center"),
        os.path.join(GENESIS_BASE, "Library"),
        os.path.join(GENESIS_BASE, "Database"),
        os.path.join(GENESIS_BASE, "dashboard_static")
    ]
    for p in required_paths:
        if not os.path.exists(p):
            logging.error(f"[HEALTH] 缺失必要目錄: {p}")
            return False, f"Missing directory: {p}"
    return True, "All required directories exist."

def check_databases():
    """驗證 SQLite 資料庫健康度與連線狀態"""
    db_path = os.path.join(GENESIS_BASE, "Database", "Genesis_DFMEA.db")
    if not os.path.exists(db_path):
        logging.error("[HEALTH] 缺失 DFMEA 資料庫")
        return False, "Missing SQLite database"
    
    import sqlite3
    try:
        conn = sqlite3.connect(db_path, timeout=3.0)
        conn.execute("SELECT 1 FROM dfmea_matrix LIMIT 1")
        conn.close()
    except Exception as e:
        logging.error(f"[HEALTH] 資料庫連線或讀取失敗: {e}")
        return False, f"Database query failed: {e}"
    return True, "Databases are queryable and active."

def check_dashboard_port():
    """檢測控制台 Port 8000 伺服器響應"""
    try:
        with socket.create_connection(("127.0.0.1", 8000), timeout=2.0):
            pass
    except Exception as e:
        logging.warning(f"[HEALTH] 儀表板 Port 8000 未響應: {e}")
        return False, f"Dashboard server offline (Port 8000): {e}"
    return True, "Dashboard server is responsive."

def trigger_doctor_prime(reason=""):
    """載入自癒大腦 Doctor_Prime 執行閉環恢復"""
    print(f"\n[ALERT] 系統狀態異常 ({reason})。正在調用 Doctor_Prime 診斷自癒機制...")
    logging.warning(f"[HEALTH] 觸發 Doctor_Prime 診斷自癒機制。原因: {reason}")
    
    try:
        sys.path.insert(0, os.path.join(GENESIS_BASE, "RD_Center", "SDK", "Core"))
        sys.path.insert(0, os.path.join(GENESIS_BASE, "RD_Center", "SDK", "Base"))
        from Doctor_Prime import Doctor_Prime
        
        doctor = Doctor_Prime()
        doctor.execute_closed_loop_recovery(reason=reason)
        print("[SUCCESS] Doctor_Prime 閉環診斷修復程序執行完畢。")
        logging.info("[HEALTH] Doctor_Prime 閉環修復程序已完成調用。")
        return True
    except Exception as e:
        print(f"[FATAL] 調用 Doctor_Prime 失敗: {e}")
        logging.critical(f"[HEALTH] 無法加載 Doctor_Prime: {e}")
        return False

def apply_patch(patch_code):
    """核心修復邏輯：整合 Git 版本控管與自動回滾"""
    logging.info("開始執行自動修復程序...")
    try:
        # 1. 檢查 Git 狀態
        status = run_cmd(["git", "status", "--porcelain"])
        if status.returncode == 0 and status.stdout.strip():
            run_cmd(["git", "stash", "save", f"auto_patch_{datetime.datetime.now().strftime('%Y%m%d%H%M')}"])

        # 2. 物理寫入 Patch 內容
        with open(TARGET_MODULE, "w", encoding="utf-8") as f:
            f.write(patch_code)
        logging.info(f"成功物理寫入 Patch 至 {TARGET_MODULE}")

        # 3. 執行測試驗證 (Unit Testing)
        if os.path.exists(TEST_SCRIPT):
            test_result = run_cmd([sys.executable, "-m", "unittest", TEST_SCRIPT])
            if test_result.returncode != 0:
                raise Exception(f"單元測試失敗: {test_result.stderr}")
        else:
            # 語法檢查備用方案
            import py_compile
            py_compile.compile(TARGET_MODULE, doraise=True)
            logging.info("未檢測到測試腳本，已通過 py_compile 語法編譯檢查")

        # 4. 驗證成功，進行版本提交
        run_cmd(["git", "add", TARGET_MODULE])
        run_cmd(["git", "commit", "-m", f"Auto-Patch Success at {datetime.datetime.now()}"])
        logging.info("Patch 驗證成功，Git 已提交變更。")
        print("[SUCCESS] System updated and committed.")
        return True
        
    except Exception as e:
        logging.error(f"Patch 失敗，執行回滾: {e}")
        # 5. 強制回滾邏輯
        run_cmd(["git", "checkout", "."])
        run_cmd(["git", "stash", "pop"])
        print(f"[ROLLBACK] System reverted. Error: {e}")
        
        # 6. 調用 Doctor_Prime 自癒
        trigger_doctor_prime(reason=f"Patch deployment failure: {str(e)}")
        return False

def execute_health_check():
    """執行全套系統健康診斷"""
    print("=========================================")
    print("      GENESIS SYSTEM HEALTH DIAGNOSIS     ")
    print("=========================================")
    
    steps = [
        ("Directories Integrity", check_directories),
        ("SQLite Databases Connectivity", check_databases),
        ("Control Panel Server Status", check_dashboard_port)
    ]
    
    anomalies = []
    for name, func in steps:
        success, info = func()
        status_str = "OK" if success else "FAIL"
        print(f"[*] {name:<30}: [{status_str}] - {info}")
        if not success:
            anomalies.append(info)
            
    print("-----------------------------------------")
    if anomalies:
        print(f"[STATUS] SYSTEM UNHEALTHY. Detected {len(anomalies)} anomalies.")
        trigger_doctor_prime(reason=", ".join(anomalies))
        return False
    else:
        print("[STATUS] SYSTEM HEALTHY. All core modules operational.")
        return True

if __name__ == "__main__":
    execute_health_check()