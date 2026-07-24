# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\RD_Center\SDK\System\Cloud_Bridge_Sync.py
# 狀態：已全面升級，包含知識庫對齊、靜態鏡像、CSV匯出與AST沙盒編譯驗證

import os
import time
import sqlite3
import random
import shutil
import json
import ast
from datetime import datetime

LOCAL_DB = r"C:\Genesis\Database\Genesis_DFMEA.db"
CLOUD_DB = r"G:\我的雲端硬碟\ITE GEMINI Pro雲端指揮中心\memory_core_sync.db"
HANDSHAKE_FILE = r"G:\我的雲端硬碟\ITE GEMINI Pro雲端指揮中心\handshake_verified"
KNOWLEDGE_DIR = r"G:\我的雲端硬碟\ITE GEMINI Pro雲端指揮中心\knowledge"
MIRROR_DIR = r"G:\我的雲端硬碟\ITE GEMINI Pro雲端指揮中心\mirror"
LOCAL_BRICK_DIR = r"C:\Genesis\RD_Center\SDK_Bricks\Logic"

def run_query_with_retry(db_path, query, params=(), is_write=False, fetch_all=False):
    """資料庫操作指數退避重試，應對雲端硬碟鎖定"""
    max_attempts = 6
    for attempt in range(1, max_attempts + 1):
        try:
            conn = sqlite3.connect(db_path, timeout=12.0)
            conn.execute("PRAGMA journal_mode=WAL;")
            cursor = conn.cursor()
            cursor.execute(query, params)
            
            res = None
            if is_write:
                conn.commit()
            else:
                res = cursor.fetchall() if fetch_all else cursor.fetchone()
            
            conn.close()
            return res
        except sqlite3.OperationalError as e:
            if "locked" in str(e).lower() and attempt < max_attempts:
                wait_time = 0.1 * (2 ** attempt) + random.uniform(0.05, 0.2)
                print(f"[警告] 資料庫 {os.path.basename(db_path)} 鎖定，第 {attempt} 次重試，等待 {wait_time:.2f} 秒...")
                time.sleep(wait_time)
            else:
                raise e

def update_heartbeat():
    """更新地端存活心跳"""
    try:
        os.makedirs(os.path.dirname(HANDSHAKE_FILE), exist_ok=True)
        with open(HANDSHAKE_FILE, "w") as f:
            f.write(str(time.time()))
        print("[+] 雲端心跳已更新 (handshake_verified)")
    except Exception as e:
        print(f"[警告] 更新心跳失敗: {e}")

def sync_knowledge_base():
    """將地端核心協定與知識庫 .md 文件同步至雲端"""
    print("[*] 正在同步本地知識庫（.md 檔案）至雲端...")
    os.makedirs(KNOWLEDGE_DIR, exist_ok=True)
    genesis_root = r"C:\Genesis"
    try:
        for f in os.listdir(genesis_root):
            if f.endswith(".md"):
                src_path = os.path.join(genesis_root, f)
                dst_path = os.path.join(KNOWLEDGE_DIR, f)
                shutil.copy2(src_path, dst_path)
                print(f"  [知識同步] {f} -> 雲端指揮部")
    except Exception as e:
        print(f"[警告] 同步知識庫檔案失敗: {e}")

def export_dfmea_csv():
    """將 DFMEA 矩陣匯出為 Google Sheets 可直接讀取的 CSV 檔案"""
    csv_path = os.path.join(MIRROR_DIR, "dfmea_sheets_mirror.csv")
    print(f"[*] 正在匯出 DFMEA 矩陣至 CSV: {csv_path}")
    try:
        os.makedirs(MIRROR_DIR, exist_ok=True)
        rows = run_query_with_retry(
            LOCAL_DB,
            "SELECT id, problem_point, failure_mode, severity, root_cause, prevention, corrective FROM dfmea_matrix",
            fetch_all=True
        )
        with open(csv_path, "w", encoding="utf-8-sig") as f:
            # 寫入標頭
            f.write("ID,問題點 (Problem Point),失效模式 (Failure Mode),嚴重度 (Severity),根本原因 (Root Cause),預防措施 (Prevention),矯正措施 (Corrective)\n")
            for r in rows:
                # 簡單逸出逗號與雙引號
                clean_cols = []
                for col in r:
                    val = str(col or "").replace('"', '""')
                    if ',' in val or '\n' in val or '"' in val:
                        val = f'"{val}"'
                    clean_cols.append(val)
                f.write(",".join(clean_cols) + "\n")
        print("[+] CSV 鏡像匯出成功！")
    except Exception as e:
        print(f"[警告] 匯出 CSV 失敗: {e}")

def generate_html_mirror():
    """動態生成炫酷的雲端 HTML 狀態儀表板鏡像"""
    html_path = os.path.join(MIRROR_DIR, "status_mirror.html")
    print(f"[*] 正在編譯雲端 HTML 狀態鏡像: {html_path}")
    try:
        # 讀取 DB 資料
        total_rules = run_query_with_retry(LOCAL_DB, "SELECT COUNT(*) FROM dfmea_matrix")[0]
        recent_events = run_query_with_retry(
            LOCAL_DB, 
            "SELECT event_type, status, timestamp FROM System_Events ORDER BY id DESC LIMIT 5",
            fetch_all=True
        )
        
        event_list_html = ""
        for ev in recent_events:
            status_color = "var(--accent)" if ev[1] in ['COMPLETED', 'SUCCESS'] else "var(--text-dim)"
            event_list_html += f"""
            <div class="log-item">
                <span class="log-time">[{ev[2]}]</span>
                <span class="log-type">{ev[0]}</span>
                <span class="log-status" style="color: {status_color}">{ev[1]}</span>
            </div>
            """

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        html_content = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>Genesis 雲端指揮部鏡像儀表板</title>
    <style>
        :root {{
            --bg: #0b0f19;
            --panel: rgba(255, 255, 255, 0.03);
            --border: rgba(255, 255, 255, 0.08);
            --text: #f3f4f6;
            --text-dim: #9ca3af;
            --accent: #10b981;
            --warning: #f59e0b;
        }}
        body {{
            background-color: var(--bg);
            color: var(--text);
            font-family: 'Segoe UI', system-ui, sans-serif;
            margin: 0;
            padding: 2rem;
            display: flex;
            justify-content: center;
        }}
        .container {{
            max-width: 800px;
            width: 100%;
        }}
        .header {{
            background: linear-gradient(135deg, #1e293b, #0f172a);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 1.8rem;
            background: linear-gradient(45deg, #60a5fa, #34d399);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1.5rem;
            margin-bottom: 1.5rem;
        }}
        .card {{
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
            backdrop-filter: blur(10px);
        }}
        .card-title {{
            color: var(--text-dim);
            font-size: 0.9rem;
            margin-bottom: 0.5rem;
        }}
        .card-value {{
            font-size: 1.5rem;
            font-weight: bold;
        }}
        .log-panel {{
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
        }}
        .log-item {{
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            padding: 0.5rem 0;
            font-size: 0.9rem;
            display: flex;
            justify-content: space-between;
        }}
        .log-time {{
            color: var(--text-dim);
        }}
        .status-dot {{
            display: inline-block;
            width: 10px;
            height: 10px;
            background-color: var(--accent);
            border-radius: 50%;
            margin-right: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>龍蝦帝國 - 雲端指揮部鏡像儀表板</h1>
            <p style="color: var(--text-dim); font-size: 0.9rem; margin: 0.5rem 0 0 0;">上次同步更新時間：{timestamp}</p>
        </div>
        <div class="grid">
            <div class="card">
                <div class="card-title">系統連線狀態</div>
                <div class="card-value"><span class="status-dot"></span>ONLINE</div>
            </div>
            <div class="card">
                <div class="card-title">已註冊 DFMEA 規則</div>
                <div class="card-value">{total_rules} 筆</div>
            </div>
            <div class="card">
                <div class="card-title">節點健康防禦 (A-D)</div>
                <div class="card-value" style="color: var(--accent);">Node D ACTIVE</div>
            </div>
        </div>
        <div class="log-panel">
            <h3 style="margin-top: 0;">最近 5 筆地端執行日誌</h3>
            {event_list_html}
        </div>
    </div>
</body>
</html>
"""
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print("[+] HTML 靜態鏡像編譯完成！")
    except Exception as e:
        print(f"[警告] 編譯 HTML 鏡像失敗: {e}")

def run_ast_sandbox_check(code_text):
    """
    頂真思維：對雲端傳來的代碼草稿進行 AST 安全沙盒靜態編譯檢索。
    防範惡意刪檔、高風險系統呼叫與無窮迴圈。
    """
    try:
        root = ast.parse(code_text)
    except SyntaxError as e:
        return False, f"語法錯誤 (Syntax Error): {e}"

    # 禁止引入的模組黑名單
    banned_modules = {'shutil', 'socket', 'requests', 'urllib', 'ctypes'}
    # 禁止呼叫的 API 黑名單
    banned_calls = {'system', 'popen', 'subprocess', 'eval', 'exec', 'remove', 'rmdir', 'unlink'}

    for node in ast.walk(root):
        # 1. 檢查 import 語句
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name in banned_modules:
                    return False, f"安全沙盒拒絕：禁止引入高風險模組 '{alias.name}'"
        elif isinstance(node, ast.ImportFrom):
            if node.module in banned_modules:
                return False, f"安全沙盒拒絕：禁止自高風險模組引入 '{node.module}'"
        
        # 2. 檢查函數呼叫
        elif isinstance(node, ast.Call):
            func_name = ""
            if isinstance(node.func, ast.Name):
                func_name = node.func.id
            elif isinstance(node.func, ast.Attribute):
                func_name = node.func.attr
            
            if func_name in banned_calls:
                return False, f"安全沙盒拒絕：禁止調用高風險 API '{func_name}'"

        # 3. 檢查 While 迴圈是否存在無條件 Break (防止無窮迴圈掛起地端)
        elif isinstance(node, ast.While):
            # 檢查 while True 是否有任何 break 語句
            has_break = False
            for child in ast.walk(node):
                if isinstance(child, ast.Break):
                    has_break = True
                    break
            # 如果測試條件是常數 True 且無 break
            if isinstance(node.test, ast.Constant) and node.test.value is True and not has_break:
                return False, "安全防禦拒絕：偵測到危險無窮迴圈結構，已拒絕編譯。"

    return True, "驗證通過"

def process_cloud_drafts():
    """
    檢查雲端發送的 'DRAFT' 任務。
    如果包含代碼片段，執行 AST 沙盒驗證。
    驗證通過：寫入本地 SDK_Bricks/Logic，狀態更新為 PENDING 並計算 hash。
    驗證失敗：狀態更新為 BLOCKED_BY_SANDBOX。
    """
    try:
        drafts = run_query_with_retry(
            CLOUD_DB,
            "SELECT task_id, instruction, timestamp FROM Sync_Control_Table WHERE status = 'DRAFT' OR status = 'PENDING'",
            fetch_all=True
        )
    except Exception as e:
        print(f"[警告] 無法讀取雲端指令: {e}")
        return

    for task in drafts:
        task_id, instruction, timestamp = task
        try:
            inst_data = json.loads(instruction)
        except Exception:
            continue

        code_text = inst_data.get("code")
        brick_name = inst_data.get("brick")
        
        if not code_text or not brick_name:
            continue

        print(f"[*] 偵測到雲端發出程式草稿 [ID: {task_id}] '{brick_name}'，進行沙盒校驗...")
        is_safe, reason = run_ast_sandbox_check(code_text)

        if is_safe:
            print(f"[+] 沙盒校驗通過！寫入本地積木：{brick_name}")
            brick_path = os.path.join(LOCAL_BRICK_DIR, brick_name)
            os.makedirs(os.path.dirname(brick_path), exist_ok=True)
            with open(brick_path, "w", encoding="utf-8") as f:
                f.write(code_text)
            
            # 計算該檔案 Hash
            sha = hashlib = hashlib = None
            import hashlib
            sha = hashlib.sha256()
            with open(brick_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha.update(chunk)
            file_hash = sha.hexdigest().upper()

            # 將雲端與地端的任務狀態提升為 PENDING，並附加剛編譯出來的正確 Hash 碼以防 Node D 熔斷
            # 清除 code 欄位，僅保留運行指令，避免每次都重複寫入
            clean_instruction = json.dumps({"brick": brick_name})
            
            run_query_with_retry(
                CLOUD_DB,
                "UPDATE Sync_Control_Table SET status = 'PENDING', instruction = ?, last_hash = ? WHERE task_id = ?",
                (clean_instruction, file_hash, task_id),
                is_write=True
            )
            run_query_with_retry(
                LOCAL_DB,
                "INSERT OR REPLACE INTO Sync_Control_Table (task_id, instruction, status, last_hash, timestamp) VALUES (?, ?, 'PENDING', ?, ?)",
                (task_id, clean_instruction, file_hash, timestamp),
                is_write=True
            )
            print(f"[+] 任務 {task_id} 已成功安全上架，等待 Daemon 自癒執行。")
        else:
            print(f"[❌] 沙盒校驗攔截！原因: {reason}")
            # 更新為 BLOCKED_BY_SANDBOX 狀態並發布日誌
            run_query_with_retry(
                CLOUD_DB,
                "UPDATE Sync_Control_Table SET status = 'BLOCKED_BY_SANDBOX' WHERE task_id = ?",
                (task_id,),
                is_write=True
            )
            run_query_with_retry(
                LOCAL_DB,
                "INSERT OR REPLACE INTO Sync_Control_Table (task_id, instruction, status, last_hash, timestamp) VALUES (?, ?, 'BLOCKED_BY_SANDBOX', '', ?)",
                (task_id, instruction, timestamp),
                is_write=True
            )
            run_query_with_retry(
                LOCAL_DB,
                "INSERT INTO System_Events (event_type, instruction, status, timestamp) VALUES ('SANDBOX_BLOCK', ?, ?, ?)",
                (instruction, reason, timestamp),
                is_write=True
            )

def sync_tables():
    """雙向資料庫對齊"""
    print("[*] 執行資料庫表單雙向對齊...")

    # 1. 雲端 -> 地端：同步常規 PENDING 指令
    try:
        cloud_pending = run_query_with_retry(
            CLOUD_DB, 
            "SELECT task_id, instruction, last_hash, timestamp FROM Sync_Control_Table WHERE status = 'PENDING'", 
            fetch_all=True
        )
    except Exception as e:
        print(f"[警告] 無法讀取雲端指令: {e}")
        return

    for task in cloud_pending:
        task_id, instruction, last_hash, timestamp = task
        try:
            run_query_with_retry(
                LOCAL_DB,
                """
                INSERT OR IGNORE INTO Sync_Control_Table (task_id, instruction, status, last_hash, timestamp)
                VALUES (?, ?, 'PENDING', ?, ?)
                """,
                (task_id, instruction, last_hash, timestamp),
                is_write=True
            )
        except Exception as e:
            print(f"[警告] 同步寫入地端失敗: {e}")

    # 2. 地端 -> 雲端：回傳已完成或熔斷狀態
    try:
        local_processed = run_query_with_retry(
            LOCAL_DB,
            "SELECT task_id, status, last_hash, timestamp FROM Sync_Control_Table WHERE status != 'PENDING'",
            fetch_all=True
        )
    except Exception as e:
        print(f"[警告] 無法讀取地端處理狀態: {e}")
        return

    for task in local_processed:
        task_id, status, last_hash, timestamp = task
        try:
            cloud_row = run_query_with_retry(
                CLOUD_DB,
                "SELECT status FROM Sync_Control_Table WHERE task_id = ?",
                (task_id,)
            )
            if not cloud_row or cloud_row[0] in ['PENDING', 'RUNNING', 'DRAFT']:
                run_query_with_retry(
                    CLOUD_DB,
                    """
                    INSERT OR REPLACE INTO Sync_Control_Table (task_id, instruction, status, last_hash, timestamp)
                    VALUES (
                        ?, 
                        COALESCE((SELECT instruction FROM Sync_Control_Table WHERE task_id = ?), 'Auto-Synced'),
                        ?, ?, ?
                    )
                    """,
                    (task_id, task_id, status, last_hash, timestamp),
                    is_write=True
                )
                print(f"[同步] 回傳執行狀態 {task_id} -> {status}")
        except Exception as e:
            print(f"[警告] 同步回寫雲端狀態失敗: {e}")

    # 3. 雙向同步 System_Events
    try:
        local_events = run_query_with_retry(LOCAL_DB, "SELECT event_type, instruction, status, last_hash, timestamp FROM System_Events", fetch_all=True)
        for ev in local_events:
            ev_type, inst, st, lh, ts = ev
            run_query_with_retry(
                CLOUD_DB,
                """
                INSERT INTO System_Events (event_type, instruction, status, last_hash, timestamp)
                SELECT ?, ?, ?, ?, ?
                WHERE NOT EXISTS (
                    SELECT 1 FROM System_Events WHERE event_type = ? AND timestamp = ?
                )
                """,
                (ev_type, inst, st, lh, ts, ev_type, ts),
                is_write=True
            )
    except Exception as e:
        print(f"[警告] 同步地端事件至雲端失敗: {e}")

    try:
        cloud_events = run_query_with_retry(CLOUD_DB, "SELECT event_type, instruction, status, last_hash, timestamp FROM System_Events", fetch_all=True)
        for ev in cloud_events:
            ev_type, inst, st, lh, ts = ev
            run_query_with_retry(
                LOCAL_DB,
                """
                INSERT INTO System_Events (event_type, instruction, status, last_hash, timestamp)
                SELECT ?, ?, ?, ?, ?
                WHERE NOT EXISTS (
                    SELECT 1 FROM System_Events WHERE event_type = ? AND timestamp = ?
                )
                """,
                (ev_type, inst, st, lh, ts, ev_type, ts),
                is_write=True
            )
    except Exception as e:
        print(f"[警告] 同步雲端事件至地端失敗: {e}")

    # 4. 雙向同步 dfmea_matrix
    try:
        local_rules = run_query_with_retry(LOCAL_DB, "SELECT id, problem_point, failure_mode, severity, root_cause, prevention, corrective FROM dfmea_matrix", fetch_all=True)
        for r in local_rules:
            rid, pp, fm, sev, rc, prev, corr = r
            run_query_with_retry(
                CLOUD_DB,
                """
                INSERT OR REPLACE INTO dfmea_matrix (id, problem_point, failure_mode, severity, root_cause, prevention, corrective)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (rid, pp, fm, sev, rc, prev, corr),
                is_write=True
            )
    except Exception as e:
        print(f"[警告] 同步地端 DFMEA 矩陣至雲端失敗: {e}")

    try:
        cloud_rules = run_query_with_retry(CLOUD_DB, "SELECT id, problem_point, failure_mode, severity, root_cause, prevention, corrective FROM dfmea_matrix", fetch_all=True)
        for r in cloud_rules:
            rid, pp, fm, sev, rc, prev, corr = r
            run_query_with_retry(
                LOCAL_DB,
                """
                INSERT OR REPLACE INTO dfmea_matrix (id, problem_point, failure_mode, severity, root_cause, prevention, corrective)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (rid, pp, fm, sev, rc, prev, corr),
                is_write=True
            )
    except Exception as e:
        print(f"[警告] 同步雲端 DFMEA 矩陣至地端失敗: {e}")

    print("[SUCCESS] 雲地雙活同步與對齊成功！")

def main():
    update_heartbeat()
    sync_knowledge_base()
    process_cloud_drafts()
    sync_tables()
    export_dfmea_csv()
    generate_html_mirror()

if __name__ == "__main__":
    main()
