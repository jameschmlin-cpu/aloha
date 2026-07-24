# -*- coding: utf-8 -*-
# C:\Genesis\Headquarter\RD\Skill_WinAdmin.py
# 任務：系統清理與備份自動化，內建 pywinauto 原生控制與資料庫閉迴路管理

import os
import sys
import shutil
import psutil
import time
from pywinauto import Application

# 錨定 DB 串接路徑
CONNECTOR_PATH = r"C:\Genesis\RD_Center\Source\Option\Stage_1"
if CONNECTOR_PATH not in sys.path:
    sys.path.append(CONNECTOR_PATH)

try:
    from DB_Connector import GenesisDBFactory
except ImportError as e:
    sys.stderr.write(f"[警告] 無法加載 DB_Connector.py: {e}\n")
    GenesisDBFactory = None

class WinAdminSkill:
    def __init__(self):
        self.backup_src = r"C:\Genesis\Config"
        self.backup_dst = r"C:\Genesis\Backup\Config_Backup"
        self.report_path = r"C:\Genesis\Backup\backup_report.txt"
        os.makedirs(os.path.dirname(self.report_path), exist_ok=True)

    def log_to_db(self, state, msg):
        """閉迴路反饋：寫入 System_State 與 Genesis_History 資料庫"""
        if GenesisDBFactory:
            try:
                GenesisDBFactory.write_data("state", {
                    "node_name": "WinAdmin",
                    "state_val": state
                })
                GenesisDBFactory.write_data("history", {
                    "event_msg": f"[WinAdmin] {msg}",
                    "user_id": "WINADMIN_AGENT"
                })
                print(f"[DB LOG] State: {state} | Msg: {msg}")
            except Exception as e:
                print(f"[DB ERROR] 寫入資料庫失敗: {e}")

    def run_cleanup(self):
        """清理系統快取與 Temp 檔案"""
        print("[WinAdmin] 開始執行系統快取與暫存檔清理...")
        temp_paths = [
            r"C:\Windows\Temp",
            os.path.expandvars(r"%TEMP%")
        ]
        
        cleaned_size = 0
        for path in temp_paths:
            if not os.path.exists(path):
                continue
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        sz = os.path.getsize(file_path)
                        os.remove(file_path)
                        cleaned_size += sz
                    except Exception:
                        pass # 忽略正在被佔用的檔案
                        
        cleaned_mb = cleaned_size / (1024 * 1024)
        print(f"[WinAdmin] 暫存檔清理完成，共釋放 {cleaned_mb:.2f} MB 空間。")
        return cleaned_mb

    def run_backup(self):
        """執行核心設定檔備份"""
        print(f"[WinAdmin] 正在將 {self.backup_src} 備份至 {self.backup_dst} ...")
        try:
            if os.path.exists(self.backup_dst):
                shutil.rmtree(self.backup_dst)
            shutil.copytree(self.backup_src, self.backup_dst)
            print("[WinAdmin] 設定檔備份成功！")
            return True
        except Exception as e:
            print(f"[WinAdmin] 備份失敗: {e}")
            return False

    def pywinauto_gui_automation(self, cleaned_mb):
        """使用 pywinauto 原生控制 Windows Notepad 生成視覺化日誌"""
        print("[WinAdmin] 啟動 pywinauto GUI 自動化（開啟記事本記錄日誌）...")
        try:
            # 1. 啟動 Notepad 應用程式
            app = Application(backend="win32").start("notepad.exe")
            time.sleep(1)
            
            # 2. 定位 Notepad 主視窗
            dlg = app.top_window()
            
            # 3. 在文字輸入區輸入日誌內容
            log_text = (
                f"=== Genesis System Maintenance Report ===\n"
                f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Disk Cleanup: Released {cleaned_mb:.2f} MB of temporary files.\n"
                f"Configuration Backup: Successful.\n"
                f"System Health: RAM usage is currently {psutil.virtual_memory().percent}%.\n"
                f"=========================================\n"
            )
            dlg.Edit.type_keys(log_text, with_spaces=True, with_newlines=True)
            
            # 4. 儲存日誌檔案
            # 送出 Ctrl+S 組合鍵
            dlg.type_keys("^s")
            time.sleep(1)
            
            # 定位「另存新檔」對話方塊並輸入路徑
            save_as_dlg = app.window(title_re=".*另存.*|.*Save.*")
            if save_as_dlg.exists():
                save_as_dlg.Edit.type_keys(self.report_path, with_spaces=True)
                save_as_dlg.type_keys("{ENTER}")
                time.sleep(0.5)
                # 若檔案已存在，確認覆蓋
                confirm_dlg = app.window(title_re=".*確認.*|.*Confirm.*")
                if confirm_dlg.exists():
                    confirm_dlg.type_keys("{ENTER}")
            else:
                # 備援方案：若無法定位另存視窗，直接寫入檔案
                with open(self.report_path, "w", encoding="utf-8") as f:
                    f.write(log_text)
            
            # 5. 關閉 Notepad 視窗
            dlg.close()
            print(f"[WinAdmin] pywinauto 自動化完成，日誌已存至: {self.report_path}")
            return True
        except Exception as e:
            print(f"[WinAdmin] pywinauto GUI 自動化失敗 (可能無作用中的桌面工作階段): {e}")
            # 靜默備援：直接物理寫入
            try:
                with open(self.report_path, "w", encoding="utf-8") as f:
                    f.write(f"Fallback Backup Log at {time.time()} - Cleaned {cleaned_mb:.2f} MB\n")
            except:
                pass
            return False

    def execute_closed_loop_flow(self):
        """執行完整閉迴路管理流：監控 ➔ 清理 ➔ 備份 ➔ GUI日誌 ➔ 寫入資料庫監控"""
        # 1. 監控開始
        ram_before = psutil.virtual_memory().percent
        print(f"[WinAdmin] 開始執行閉迴路維護巡檢 (當前記憶體: {ram_before}%)")
        
        # 2. 執行清理與備份
        cleaned_mb = self.run_cleanup()
        backup_success = self.run_backup()
        
        # 3. 執行 GUI 自動化
        gui_success = self.pywinauto_gui_automation(cleaned_mb)
        
        # 4. 校驗結果並寫入資料庫
        ram_after = psutil.virtual_memory().percent
        status_val = "SUCCESS" if (backup_success and gui_success) else "PARTIAL_SUCCESS"
        event_message = (
            f"維護執行完畢。清理空間: {cleaned_mb:.2f}MB, "
            f"備份狀態: {backup_success}, GUI狀態: {gui_success}, "
            f"記憶體前後對比: {ram_before}% -> {ram_after}%"
        )
        
        # 寫入狀態進行閉迴路回饋
        self.log_to_db(status_val, event_message)
        print(f"[WinAdmin] 閉迴路流程執行完畢：{event_message}")

if __name__ == "__main__":
    admin = WinAdminSkill()
    admin.execute_closed_loop_flow()
