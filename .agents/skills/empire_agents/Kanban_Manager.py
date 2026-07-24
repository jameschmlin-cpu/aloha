# -*- coding: utf-8 -*-
# C:\Genesis\.agents\skills\empire_agents\Kanban_Manager.py
# Kanban Board Manager for the Corporate Agent System

import sqlite3

class KanbanManager:
    def __init__(self, db_path=r"C:\Genesis\Database\Genesis_History.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """建立 company_backlog 資料表，用於追蹤 Agent 企業級任務流動"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS company_backlog (
                task_id TEXT PRIMARY KEY,
                title TEXT,
                description TEXT,
                status TEXT,              -- TODO, IN_PROGRESS, PENDING_QA, PENDING_DEPLOY, COMPLETED, REJECTED, ESCALATED
                assigned_department TEXT, -- PM, RD, QA, SCM, MFG, Sales
                security_signed INTEGER DEFAULT 0,  -- SCM 安全審查標記 (0/1)
                qa_code TEXT,             -- QA 簽署的品質代碼
                artifacts TEXT,           -- JSON 格式的產出檔案路徑
                retry_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def add_task(self, task_id, title, description, assigned_department, status='TODO'):
        """向看板新增一個工作項目"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO company_backlog (task_id, title, description, status, assigned_department)
                VALUES (?, ?, ?, ?, ?)
            ''', (task_id, title, description, status, assigned_department))
            conn.commit()
            return True
        except Exception as e:
            print(f"[Kanban Error] 新增任務失敗: {e}")
            return False
        finally:
            conn.close()

    def get_tasks_by_dept_and_status(self, dept, status):
        """依據負責部門與狀態取得任務"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM company_backlog
            WHERE assigned_department = ? AND status = ?
        ''', (dept, status))
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows

    def get_task(self, task_id):
        """取得單一任務詳細內容"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM company_backlog WHERE task_id = ?', (task_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def update_task(self, task_id, status=None, assigned_department=None, qa_code=None, security_signed=None, artifacts=None):
        """更新任務欄位"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        updates = []
        params = []
        if status is not None:
            updates.append("status = ?")
            params.append(status)
        if assigned_department is not None:
            updates.append("assigned_department = ?")
            params.append(assigned_department)
        if qa_code is not None:
            updates.append("qa_code = ?")
            params.append(qa_code)
        if security_signed is not None:
            updates.append("security_signed = ?")
            params.append(security_signed)
        if artifacts is not None:
            updates.append("artifacts = ?")
            params.append(artifacts)
        
        if not updates:
            conn.close()
            return False

        updates.append("updated_at = CURRENT_TIMESTAMP")
        params.append(task_id)

        sql = f"UPDATE company_backlog SET {', '.join(updates)} WHERE task_id = ?"
        try:
            cursor.execute(sql, tuple(params))
            conn.commit()
            return True
        except Exception as e:
            print(f"[Kanban Error] 更新任務 {task_id} 失敗: {e}")
            return False
        finally:
            conn.close()

    def increment_retry(self, task_id):
        """增加重試次數"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE company_backlog 
                SET retry_count = retry_count + 1, updated_at = CURRENT_TIMESTAMP
                WHERE task_id = ?
            ''', (task_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"[Kanban Error] 增加重試次數失敗: {e}")
            return False
        finally:
            conn.close()

    def clear_board(self):
        """清空看板 (除錯測試用)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM company_backlog")
        conn.commit()
        conn.close()
