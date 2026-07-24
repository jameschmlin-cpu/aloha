# -*- coding: utf-8 -*-
import sys
import os
import sqlite3
import logging
import time
import importlib.util
import shutil

# 強制物理路徑導通
sys.path.insert(0, r"C:\Genesis")
sys.path.insert(0, r"C:\Genesis\RD_Center\Source\Option\Stage_1")
sys.path.insert(0, r"C:\Genesis\Genesis_Core")

class Doctor_Prime:
    def __init__(self):
        self.golden_mirror_path = r"D:\SystemBackUp\ITE_Mirror_Genesis"
        self.db_path = r"C:\Genesis\Database\Path_Registry.db"
        self.root_dir = r"C:\Genesis"
        self.core = None 
        
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - [DOCTOR] - %(message)s')
        self.report("INIT", "Doctor_Prime 核心引擎已啟動，備份/還原機制已就緒。")

    def _lazy_init_base(self):
        if self.core is None:
            spec = importlib.util.spec_from_file_location("Base_Template", r"C:\Genesis\Base_Template.py")
            base_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(base_module)
            self.core = base_module.Base_Template(brick_id="DOCTOR_PRIME_CORE")

    def report(self, level, message):
        logging.info(f"[{level}] {message}")
        print(f"[{level}] {message}")

    def run_guard(self):
        self._lazy_init_base()
        
        try:
            spec = importlib.util.spec_from_file_location("Guardian_Bot", r"C:\Genesis\RD_Center\Source\Option\Stage_1\Guardian_Bot.py")
            gb = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(gb)
            self.guardian = gb.GuardianEngine()
        except Exception as e:
            self.report("ERROR", f"無法啟動 Guardian: {e}")
            return

        self.report("GUARD", "Guardian 守護機制已接管系統...")
        while True:
            try:
                self.auto_verify_all_paths()
                self.guardian.scan_and_remediate()
                time.sleep(30)
            except Exception as e:
                self.report("ERROR", f"循環監控異常: {e}")
                time.sleep(10)

    def auto_verify_all_paths(self):
        """偵測路徑並執行自動修復"""
        if not os.path.exists(self.db_path): return
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # 需確保資料庫中有 backup_path 欄位
        cursor.execute("SELECT module_name, physical_path, backup_path FROM path_map")
        modules = cursor.fetchall()
        conn.close()
        
        for mod, phys_path, back_path in modules:
            if not os.path.exists(phys_path):
                self.report("WARNING", f"偵測到模組損毀或遺失: {mod}")
                self.repair_module(mod, phys_path, back_path)

    def repair_module(self, module_name, target_path, backup_source):
        """執行物理檔案還原"""
        self.report("REPAIR", f"正在啟動還原程序: {module_name}...")
        try:
            if not os.path.exists(backup_source):
                self.report("ERROR", f"還原失敗: 鏡像來源不存在 {backup_source}")
                return False
            
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            shutil.copy2(backup_source, target_path)
            self.report("SUCCESS", f"模組 {module_name} 已從 {backup_source} 還原成功。")
            return True
        except Exception as e:
            self.report("FATAL", f"執行還原指令時發生錯誤: {e}")
            return False

    def create_backup(self, module_name, source_path):
        """手動觸發備份功能"""
        dest_path = os.path.join(self.golden_mirror_path, f"{module_name}_backup")
        try:
            os.makedirs(self.golden_mirror_path, exist_ok=True)
            shutil.copy2(source_path, dest_path)
            self.report("BACKUP", f"模組 {module_name} 已成功備份至鏡像區。")
            return dest_path
        except Exception as e:
            self.report("ERROR", f"備份失敗: {e}")
            return None

if __name__ == "__main__":
    print("[SYSTEM] 正在執行 Doctor_Prime 物理層初始化...")
    try:
        doc = Doctor_Prime()
        print("[SUCCESS] Doctor_Prime 核心引擎已就緒。")
        doc.run_guard()
    except Exception as e:
        print(f"[FATAL ERROR] 系統初始化發生嚴重異常: {e}")
        sys.exit(1)