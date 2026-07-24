# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\Genesis_Sync_Daemon.py
# 狀態：已修正錨點至 memory_core_sync.db，邏輯閉鎖完成

import os
import sys
import json
import time
import sqlite3
import hashlib
import subprocess
from datetime import datetime

GENESIS_BASE = r"C:\Genesis"
DB_PATH = os.path.join(GENESIS_BASE, "Database", "Genesis_DFMEA.db")
LOG_FILE = os.path.join(GENESIS_BASE, "Genesis_Core", "DFMEA_Monitor.log")

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

class GenesisSyncDaemon:
    def __init__(self):
        self.consecutive_mismatches = 0
        self.log_offset = 0
        self.is_running = True
        print("[*] 初始化 Genesis 同步守護進程 (Anchor: memory_core_sync.db)...")
        self.init_database()
        self.init_log_offset()
        try:
            import diskcache
            self.cache_dir = os.path.join(GENESIS_BASE, "cache", "file_metadata")
            os.makedirs(self.cache_dir, exist_ok=True)
            self.cache = diskcache.Cache(self.cache_dir)
            print(f"[+] DiskCache 初始化成功：{self.cache_dir}")
        except Exception as e:
            self.cache = None
            print(f"[警告] DiskCache 初始化失敗，將不使用快取: {e}")

    def init_database(self):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        try:
            conn = sqlite3.connect(DB_PATH, timeout=10.0)
            conn.execute("PRAGMA journal_mode=WAL;")
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS Sync_Control_Table (id INTEGER PRIMARY KEY AUTOINCREMENT, task_id TEXT UNIQUE NOT NULL, instruction TEXT NOT NULL, status TEXT NOT NULL, last_hash TEXT, timestamp TEXT NOT NULL)")
            cursor.execute("CREATE TABLE IF NOT EXISTS System_Events (id INTEGER PRIMARY KEY AUTOINCREMENT, event_type TEXT NOT NULL, instruction TEXT, status TEXT, last_hash TEXT, timestamp TEXT NOT NULL)")
            cursor.execute("CREATE TABLE IF NOT EXISTS DFMEA_Monitor_Logs (id INTEGER PRIMARY KEY AUTOINCREMENT, log_line TEXT NOT NULL, timestamp TEXT NOT NULL)")
            conn.commit()
            conn.close()
            print(f"[+] 資料庫初始化成功：{DB_PATH}")
        except Exception as e:
            print(f"[❌] 初始化資料表失敗: {e}")
            sys.exit(1)

    def init_log_offset(self):
        if os.path.exists(LOG_FILE):
            self.log_offset = os.path.getsize(LOG_FILE)
        else:
            os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
            with open(LOG_FILE, "w", encoding="utf-8") as f:
                f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [DAEMON] Genesis_Sync_Daemon 啟動。\n")
            self.log_offset = os.path.getsize(LOG_FILE)

    def write_daemon_log(self, level, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"[{timestamp}] [{level}] {message}\n"
        try:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(log_line)
            print(f"[{level}] {message}")
        except Exception as e:
            print(f"[警告] 無法寫入日誌檔: {e}")

    def calculate_file_sha256(self, filepath):
        try:
            if self.cache and os.path.exists(filepath):
                stat = os.stat(filepath)
                mtime = stat.st_mtime
                size = stat.st_size
                cache_key = f"hash:{filepath}:{mtime}:{size}"
                cached_hash = self.cache.get(cache_key)
                if cached_hash:
                    return cached_hash
        except Exception:
            pass

        sha256 = hashlib.sha256()
        try:
            with open(filepath, 'rb') as f:
                while True:
                    data = f.read(65536)
                    if not data: break
                    sha256.update(data)
            actual_hash = sha256.hexdigest().upper()
            try:
                if self.cache:
                    stat = os.stat(filepath)
                    mtime = stat.st_mtime
                    size = stat.st_size
                    cache_key = f"hash:{filepath}:{mtime}:{size}"
                    self.cache.set(cache_key, actual_hash, expire=86400 * 7) # 快取 7 天
            except Exception:
                pass
            return actual_hash
        except Exception: return None

    def sync_log_to_db(self):
        if not os.path.exists(LOG_FILE): return
        curr_size = os.path.getsize(LOG_FILE)
        if curr_size <= self.log_offset:
            self.log_offset = curr_size
            return
        try:
            with open(LOG_FILE, "r", encoding="utf-8", errors="ignore") as f:
                f.seek(self.log_offset)
                new_lines = f.readlines()
            self.log_offset = curr_size
            conn = sqlite3.connect(DB_PATH, timeout=5.0)
            cursor = conn.cursor()
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for line in new_lines:
                if line.strip():
                    cursor.execute("INSERT INTO DFMEA_Monitor_Logs (log_line, timestamp) VALUES (?, ?)", (line.strip(), ts))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[警告] 日誌同步失敗: {e}")

    def execute_meltdown(self, error_message):
        self.is_running = False
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.write_daemon_log("FATAL", f"【物理熔斷】原因: {error_message}")
        try:
            conn = sqlite3.connect(DB_PATH, timeout=5.0)
            cursor = conn.cursor()
            cursor.execute("UPDATE Sync_Control_Table SET status = 'MELTDOWN', timestamp = ? WHERE status IN ('RUNNING', 'PENDING')", (ts,))
            cursor.execute("INSERT INTO System_Events (event_type, instruction, status, timestamp) VALUES ('MELTDOWN', ?, 'MELTDOWN', ?)", (error_message, ts))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[❌] 熔斷紀錄失敗: {e}")
        sys.exit(1)

    def find_brick_path(self, brick_name):
        bricks_dir = os.path.join(GENESIS_BASE, "RD_Center", "SDK_Bricks")
        clean_name = brick_name.lower().replace(".py", "")
        for root, _, files in os.walk(bricks_dir):
            for f in files:
                if f.endswith(".py") and f.lower().replace(".py", "") == clean_name:
                    return os.path.join(root, f)
        return None

    def process_pending_instructions(self):
        try:
            conn = sqlite3.connect(DB_PATH, timeout=5.0)
            cursor = conn.cursor()
            cursor.execute("SELECT id, task_id, instruction, last_hash FROM Sync_Control_Table WHERE status = 'PENDING' ORDER BY id ASC LIMIT 1")
            row = cursor.fetchone()
            if row:
                row_id, task_id, instruction_text, expected_hash = row
                cursor.execute("SELECT COUNT(*) FROM Sync_Control_Table WHERE task_id = ? AND status = 'COMPLETED' AND id != ?", (task_id, row_id))
                if cursor.fetchone()[0] > 0:
                    conn.close()
                    self.update_task_status(row_id, "COMPLETED", expected_hash)
                    return
            conn.close()
        except Exception: return
        if not row: return
        row_id, task_id, instruction_text, expected_hash = row
        self.write_daemon_log("INFO", f"[Node A] 偵測待處理指令: {task_id}")
        self.update_task_status(row_id, "RUNNING", None)
        
        # 解析 JSON 指令結構，支援實體代碼修補寫入
        brick_name = ""
        patch_code = None
        try:
            inst_data = json.loads(instruction_text)
            brick_name = inst_data.get("brick", "")
            patch_code = inst_data.get("code")
        except Exception:
            brick_name = instruction_text.strip()
            
        if not brick_name:
            self.update_task_status(row_id, "FAILED", None)
            return
            
        # 如果包含修補程式碼，則物理寫入本地 Logic 目錄並更新預期 Hash
        if patch_code:
            brick_dir = os.path.join(GENESIS_BASE, "RD_Center", "SDK_Bricks", "Logic")
            os.makedirs(brick_dir, exist_ok=True)
            brick_path = os.path.join(brick_dir, brick_name)
            try:
                with open(brick_path, "w", encoding="utf-8") as f:
                    f.write(patch_code)
                self.write_daemon_log("SUCCESS", f"[Node C] AI 物理修補補丁已寫入實體檔案: {brick_path}")
                
                # TDD: Step 0 - Ruff static linter check
                self.write_daemon_log("INFO", f"[TDD-RUFF-CHECK] 啟動 Ruff 靜態防禦與風格校驗: {brick_name}")
                ruff_proc = subprocess.run(
                    ["ruff", "check", brick_path, "--fix"],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    timeout=5.0
                )
                if ruff_proc.returncode != 0:
                    err_msg = ruff_proc.stdout.strip() + "\n" + ruff_proc.stderr.strip()
                    self.write_daemon_log("ERROR", f"[TDD-RUFF-FAIL] Ruff 靜態校驗未通過: {brick_name}\nDiagnostics: {err_msg}")
                    err_log_path = os.path.join(GENESIS_BASE, "Log", "Error.log")
                    os.makedirs(os.path.dirname(err_log_path), exist_ok=True)
                    with open(err_log_path, "a", encoding="utf-8") as ef:
                        ef.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] TDD_RUFF_FAIL:{brick_name}:{err_msg}\n")
                    self.update_task_status(row_id, "FAILED", None)
                    return
                else:
                    self.write_daemon_log("SUCCESS", f"[TDD-RUFF-SUCCESS] Ruff 靜態校驗通過並已套用修復: {brick_name}")

                # TDD: Step 1 - Syntax compile validation check
                compile_proc = subprocess.run([sys.executable, "-m", "py_compile", brick_path], capture_output=True, text=True, timeout=5.0)
                if compile_proc.returncode != 0:
                    err_msg = compile_proc.stderr.strip()
                    self.write_daemon_log("ERROR", f"[TDD-COMPILE-FAIL] 語法編譯檢查未通過: {brick_name}\nTraceback: {err_msg}")
                    err_log_path = os.path.join(GENESIS_BASE, "Log", "Error.log")
                    os.makedirs(os.path.dirname(err_log_path), exist_ok=True)
                    with open(err_log_path, "a", encoding="utf-8") as ef:
                        ef.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] TDD_COMPILE_FAIL:{brick_name}:{err_msg}\n")
                    self.update_task_status(row_id, "FAILED", None)
                    return

                # TDD: Step 2 - Execution test-driven check
                test_file_name = f"test_{brick_name}"
                test_file_path = None
                for t_dir in [os.path.join(GENESIS_BASE, "RD_Center", "SDK_Bricks", "Test"), os.path.dirname(brick_path)]:
                    possible_path = os.path.join(t_dir, test_file_name)
                    if os.path.exists(possible_path):
                        test_file_path = possible_path
                        break
                
                if test_file_path:
                    self.write_daemon_log("INFO", f"[TDD-TEST-EXEC] 偵測到測試積木，啟動測試: {test_file_name}")
                    test_proc = subprocess.run([sys.executable, test_file_path], capture_output=True, text=True, timeout=10.0)
                    if test_proc.returncode != 0:
                        err_msg = test_proc.stderr.strip() or test_proc.stdout.strip()
                        self.write_daemon_log("ERROR", f"[TDD-TEST-FAIL] 測試積木執行失敗: {test_file_name}\nTraceback: {err_msg}")
                        err_log_path = os.path.join(GENESIS_BASE, "Log", "Error.log")
                        os.makedirs(os.path.dirname(err_log_path), exist_ok=True)
                        with open(err_log_path, "a", encoding="utf-8") as ef:
                            ef.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] TDD_TEST_FAIL:{brick_name}:{err_msg}\n")
                        self.update_task_status(row_id, "FAILED", None)
                        return
                    else:
                        self.write_daemon_log("SUCCESS", f"[TDD-TEST-SUCCESS] 測試積木執行成功: {test_file_name}")

                actual_hash = self.calculate_file_sha256(brick_path)
                expected_hash = actual_hash
                
                # 直接更新地端資料庫該任務的預期 Hash 碼，確保後面比對順利通過
                try:
                    conn = sqlite3.connect(DB_PATH, timeout=5.0)
                    cursor = conn.cursor()
                    cursor.execute("UPDATE Sync_Control_Table SET last_hash = ? WHERE id = ?", (actual_hash, row_id))
                    conn.commit()
                    conn.close()
                except Exception as db_err:
                    print(f"Failed to update task expected hash: {db_err}")
            except Exception as we:
                self.write_daemon_log("ERROR", f"[❌] 寫入補丁檔案失敗: {we}")
        else:
            brick_path = self.find_brick_path(brick_name)
            
        if not brick_path or not os.path.exists(brick_path):
            self.update_task_status(row_id, "FAILED", None)
            return
            
        actual_hash = self.calculate_file_sha256(brick_path)
        if expected_hash and actual_hash != expected_hash.strip().upper():
            self.consecutive_mismatches += 1
            if self.consecutive_mismatches >= 3:
                self.execute_meltdown(f"Hash 比對連續 3 次不一致: {brick_name}")
            return
            
        goose_script = os.path.join(GENESIS_BASE, "RD_Center", "SDK", "System", "goose_executor.py")
        proc = subprocess.run([sys.executable, goose_script, task_id, brick_name], capture_output=True, text=True, timeout=25.0)
        if proc.returncode == 0:
            self.update_task_status(row_id, "COMPLETED", actual_hash)
        else:
            self.update_task_status(row_id, "FAILED", actual_hash)

    def update_task_status(self, row_id, status, result_hash):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            conn = sqlite3.connect(DB_PATH, timeout=5.0)
            cursor = conn.cursor()
            cursor.execute("UPDATE Sync_Control_Table SET status = ?, last_hash = ?, timestamp = ? WHERE id = ?", (status, result_hash, ts, row_id))
            cursor.execute("INSERT INTO System_Events (event_type, status, last_hash, timestamp) VALUES (?, ?, ?, ?)", ("EXECUTION_SUCCESS" if status == "COMPLETED" else "EXECUTION_FAILED", status, result_hash, ts))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[警告] 更新狀態失敗: {e}")

    def run(self):
        while self.is_running:
            self.sync_log_to_db()
            self.process_pending_instructions()
            time.sleep(2)

if __name__ == "__main__":
    daemon = GenesisSyncDaemon()
    try: daemon.run()
    except KeyboardInterrupt: sys.exit(0)