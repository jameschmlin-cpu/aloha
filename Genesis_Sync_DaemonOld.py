# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\Genesis_Sync_Daemon.py
# 狀態：已開發完成，負責雲地記憶同步、指令調度、Hash驗證與Node D熔斷保護

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

# 設定 stdout 與 stderr 保護，防範 Windows CP950 編碼崩潰
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(errors='replace')

class GenesisSyncDaemon:
    def __init__(self):
        self.consecutive_mismatches = 0
        self.log_offset = 0
        self.is_running = True

        print("[*] 初始化 Genesis 同步守護進程...")
        self.init_database()
        self.init_log_offset()

    def init_database(self):
        """1. 初始化與建立同步相關之資料表"""
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        try:
            conn = sqlite3.connect(DB_PATH, timeout=10.0)
            conn.execute("PRAGMA journal_mode=WAL;")
            cursor = conn.cursor()

            # A. 建立 Sync_Control_Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Sync_Control_Table (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id TEXT UNIQUE NOT NULL,
                    instruction TEXT NOT NULL,
                    status TEXT NOT NULL,
                    last_hash TEXT,
                    timestamp TEXT NOT NULL
                )
            """)

            # B. 建立 System_Events
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS System_Events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT NOT NULL,
                    instruction TEXT,
                    status TEXT,
                    last_hash TEXT,
                    timestamp TEXT NOT NULL
                )
            """)

            # C. 建立 DFMEA_Monitor_Logs
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS DFMEA_Monitor_Logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    log_line TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
            """)

            conn.commit()
            conn.close()
            print(f"[+] 資料庫同步資料表初始化成功：{DB_PATH}")
        except Exception as e:
            print(f"[❌] 初始化資料表失敗: {e}")
            sys.exit(1)

    def init_log_offset(self):
        """2. 初始化日誌監控偏置點，避免重播舊日誌"""
        if os.path.exists(LOG_FILE):
            self.log_offset = os.path.getsize(LOG_FILE)
        else:
            os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
            with open(LOG_FILE, "w", encoding="utf-8") as f:
                f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [DAEMON] Genesis_Sync_Daemon 已開啟啟動日誌監控。\n")
            self.log_offset = os.path.getsize(LOG_FILE)

    def write_daemon_log(self, level, message):
        """寫入本地監控日誌"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"[{timestamp}] [{level}] {message}\n"
        try:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(log_line)
            print(f"[{level}] {message}")
        except Exception as e:
            print(f"[警告] 無法寫入日誌檔: {e}")

    def calculate_file_sha256(self, filepath):
        """計算檔案的 SHA-256 值"""
        sha256 = hashlib.sha256()
        try:
            with open(filepath, 'rb') as f:
                while True:
                    data = f.read(65536)
                    if not data:
                        break
                    sha256.update(data)
            return sha256.hexdigest().upper()
        except Exception as e:
            self.write_daemon_log("ERROR", f"計算檔案 Hash 失敗 ({filepath}): {e}")
            return None

    def sync_log_to_db(self):
        """3. 自動將 DFMEA_Monitor.log 的最新增量數據寫入 SQLite 資料庫"""
        if not os.path.exists(LOG_FILE):
            return

        curr_size = os.path.getsize(LOG_FILE)
        if curr_size <= self.log_offset:
            # 無新日誌
            self.log_offset = curr_size
            return

        new_lines = []
        try:
            with open(LOG_FILE, "r", encoding="utf-8", errors="ignore") as f:
                f.seek(self.log_offset)
                new_lines = f.readlines()
            self.log_offset = curr_size
        except Exception as e:
            print(f"[警告] 讀取新日誌增量失敗: {e}")
            return

        if not new_lines:
            return

        # 寫入 SQLite
        try:
            conn = sqlite3.connect(DB_PATH, timeout=5.0)
            cursor = conn.cursor()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for line in new_lines:
                clean_line = line.strip()
                if clean_line:
                    cursor.execute("""
                        INSERT INTO DFMEA_Monitor_Logs (log_line, timestamp)
                        VALUES (?, ?)
                    """, (clean_line, timestamp))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[警告] 同步日誌到資料庫失敗: {e}")

    def execute_meltdown(self, error_message):
        """4. 執行 Node D 熔斷程序"""
        self.is_running = False
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.write_daemon_log("FATAL", f"【物理熔斷】系統發動安全熔斷防護！原因: {error_message}")

        # 寫入熔斷狀態至資料庫
        try:
            conn = sqlite3.connect(DB_PATH, timeout=5.0)
            cursor = conn.cursor()
            # 標記最新指令為熔斷狀態
            cursor.execute("""
                UPDATE Sync_Control_Table
                SET status = 'MELTDOWN', timestamp = ?
                WHERE status = 'RUNNING' OR status = 'PENDING'
            """, (timestamp,))

            # 記錄熔斷事件
            cursor.execute("""
                INSERT INTO System_Events (event_type, instruction, status, timestamp)
                VALUES ('MELTDOWN', ?, 'MELTDOWN', ?)
            """, (error_message, timestamp))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[❌] 寫入熔斷資料庫紀錄失敗: {e}")

        print("🚨 [Node D] 熔斷判定觸發，背景守護進程強制終止！")
        sys.exit(1)

    def find_brick_path(self, brick_name):
        """搜尋 SDK_Bricks 庫以取得積木實體絕對路徑"""
        bricks_dir = os.path.join(GENESIS_BASE, "RD_Center", "SDK_Bricks")
        if not os.path.exists(bricks_dir):
            return None

        # 去除 .py 尾碼以供比較
        clean_name = brick_name.lower().replace(".py", "")
        for root, _, files in os.walk(bricks_dir):
            for f in files:
                if f.endswith(".py") and f.lower().replace(".py", "") == clean_name:
                    return os.path.join(root, f)
        return None

    def process_pending_instructions(self):
        """5. 資料庫監聽與指令分派執行"""
        try:
            conn = sqlite3.connect(DB_PATH, timeout=5.0)
            cursor = conn.cursor()
            
            # A. 搜尋 Sync_Control_Table 與 System_Events 中的 PENDING 任務
            cursor.execute("""
                SELECT id, task_id, instruction, last_hash FROM Sync_Control_Table 
                WHERE status = 'PENDING' 
                ORDER BY id ASC LIMIT 1
            """)
            row = cursor.fetchone()
            
            if row:
                row_id, task_id, instruction_text, expected_hash = row
                
                # 冪等性檢查 (Idempotency check)
                # 檢查是否有其他相同 task_id 且狀態為 COMPLETED 的任務
                cursor.execute("""
                    SELECT COUNT(*) FROM Sync_Control_Table 
                    WHERE task_id = ? AND status = 'COMPLETED' AND id != ?
                """, (task_id, row_id))
                completed_count = cursor.fetchone()[0]
                if completed_count > 0:
                    conn.close()
                    self.write_daemon_log("INFO", f"[Idempotency] 指令 '{task_id}' 已經執行過，自動略過。")
                    self.update_task_status(row_id, "COMPLETED", expected_hash)
                    return
            conn.close()
        except Exception as e:
            print(f"[警告] 讀取指令表單或冪等性校驗失敗: {e}")
            return

        if not row:
            return

        row_id, task_id, instruction_text, expected_hash = row
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.write_daemon_log("INFO", f"[Node A] 偵測到待處理指令 [ID: {row_id}, TaskID: {task_id}]: {instruction_text}")

        # 標記狀態為執行中 (RUNNING)
        try:
            conn = sqlite3.connect(DB_PATH, timeout=5.0)
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Sync_Control_Table SET status = 'RUNNING' WHERE id = ?
            """, (row_id,))
            cursor.execute("""
                INSERT INTO System_Events (event_type, instruction, status, timestamp)
                VALUES ('COMMAND', ?, 'RUNNING', ?)
            """, (instruction_text, timestamp))
            conn.commit()
            conn.close()
        except Exception as e:
            self.write_daemon_log("ERROR", f"無法標記任務為執行中: {e}")
            return

        # 解析指令內容
        brick_name = ""
        try:
            inst_data = json.loads(instruction_text)
            brick_name = inst_data.get("brick") or inst_data.get("target_brick") or ""
        except json.JSONDecodeError:
            # 若非 JSON 則直接視為積木名稱
            brick_name = instruction_text.strip()

        if not brick_name:
            self.write_daemon_log("ERROR", "解析指令失敗，未指定目標積木。")
            self.update_task_status(row_id, "FAILED", None)
            return

        # 搜尋積木絕對路徑
        brick_path = self.find_brick_path(brick_name)
        if not brick_path:
            self.write_daemon_log("ERROR", f"[Node B] 在 SDK_Bricks 庫中找不到指定的積木 '{brick_name}'")
            self.update_task_status(row_id, "FAILED", None)
            return

        # 6. 計算與驗證 Hash (雙向安全校驗)
        actual_hash = self.calculate_file_sha256(brick_path)
        self.write_daemon_log("INFO", f"[Node B] 本地積木實體 Hash: {actual_hash}")

        if expected_hash and expected_hash.strip():
            expected_hash_upper = expected_hash.strip().upper()
            if actual_hash != expected_hash_upper:
                self.consecutive_mismatches += 1
                self.write_daemon_log("WARNING", f"[Node B] Hash 比對不符！預期: {expected_hash_upper} | 實際: {actual_hash} (連續不一致: {self.consecutive_mismatches}次)")
                
                # 3 次不對齊，發動防禦性熔斷
                if self.consecutive_mismatches >= 3:
                    self.execute_meltdown(f"兩端 Hash 檢核連續 3 次不一致。目標積木: {brick_name}")
                    return
            else:
                self.consecutive_mismatches = 0
                self.write_daemon_log("INFO", "[Node B] Hash 驗證通過，兩端程式版本一致。")

        # 7. Node C - 派發給 Goose AI 執行總管進行 Stage 3 (指令物理執行) 與 Stage 4 (自癒與防禦)
        self.write_daemon_log("INFO", f"[Node C] 安全校驗通過，正在指派 Goose AI 地端總管執行: {brick_name}")
        try:
            goose_script = os.path.join(GENESIS_BASE, "RD_Center", "SDK", "System", "goose_executor.py")
            proc = subprocess.run([sys.executable, goose_script, task_id, brick_name], capture_output=True, text=True, timeout=25.0)
            
            # 輸出 Goose AI 執行日誌
            if proc.stdout and proc.stdout.strip():
                self.write_daemon_log("STDOUT", f"\n{proc.stdout.strip()}")
            if proc.stderr and proc.stderr.strip():
                self.write_daemon_log("STDERR", f"\n{proc.stderr.strip()}")
                
            # 檢查 Goose AI 執行狀態結果
            if proc.returncode == 0:
                self.write_daemon_log("INFO", "[Node D] Goose AI 執行與 Stage 4 核對成功！")
            else:
                self.write_daemon_log("ERROR", f"[Node D] Goose AI 執行或 Stage 4 防禦判定失敗，返回碼: {proc.returncode}")
        except Exception as e:
            self.write_daemon_log("ERROR", f"[Node D] 調用 Goose AI 執行總管失敗: {e}")
            self.update_task_status(row_id, "FAILED", actual_hash)

    def update_task_status(self, row_id, status, result_hash):
        """更新指令執行結果回資料庫"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            conn = sqlite3.connect(DB_PATH, timeout=5.0)
            cursor = conn.cursor()
            
            # 更新 Sync_Control_Table
            cursor.execute("""
                UPDATE Sync_Control_Table 
                SET status = ?, last_hash = ?, timestamp = ? 
                WHERE id = ?
            """, (status, result_hash, timestamp, row_id))
            
            # 寫入事件日誌 (System_Events)
            event_type = "EXECUTION_SUCCESS" if status == "COMPLETED" else "EXECUTION_FAILED"
            cursor.execute("""
                INSERT INTO System_Events (event_type, status, last_hash, timestamp)
                VALUES (?, ?, ?, ?)
            """, (event_type, status, result_hash, timestamp))
            
            conn.commit()
            conn.close()
            self.write_daemon_log("INFO", f"已成功更新資料庫狀態回報：ID {row_id} -> {status}")
        except Exception as e:
            print(f"[警告] 無法更新任務狀態至資料庫: {e}")

    def run(self):
        """長輪詢主控 Loop"""
        print("==========================================================")
        print("      Genesis Common Memory Sync Daemon Running           ")
        print("      Node D Meltdown Monitor: ACTIVE                     ")
        print("==========================================================")
        
        while self.is_running:
            # 1. 同步日誌到資料庫
            self.sync_log_to_db()

            # 2. 檢索並處理待命指令
            self.process_pending_instructions()

            time.sleep(2)

if __name__ == "__main__":
    daemon = GenesisSyncDaemon()
    try:
        daemon.run()
    except KeyboardInterrupt:
        print("\nShutdown Sync Daemon.")
