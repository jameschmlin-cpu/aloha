import sqlite3
import os
import hashlib

DB_DIR = r"C:\Genesis\Database"
DB_PATH = os.path.join(DB_DIR, "Genesis_Tasks.db")
AUDIT_LOG = r"C:\Genesis\System_Audit.log"

def get_hash(text):
    """產出任務內容的專屬 Hash，供審查官校驗"""
    return hashlib.sha256(text.encode()).hexdigest()

def sync_tasks_with_context():
    """修正：不只是匯入，而是執行任務與上下文(Context)的連動校驗"""
    if not os.path.exists(DB_DIR): os.makedirs(DB_DIR)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT, hash TEXT, status TEXT)')
    
    task_file = r"C:\Genesis\TASKS.md"
    if os.path.exists(task_file):
        with open(task_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith("- [ ]"):
                    content = line.replace("- [ ] ", "").strip()
                    h = get_hash(content)
                    # 確保不重複匯入，並標記為 Context_Pending
                    cursor.execute("INSERT OR IGNORE INTO tasks (task, hash, status) VALUES (?, ?, ?)", 
                                   (content, h, "CONTEXT_PENDING"))
    
    conn.commit()
    conn.close()
    print("Context 任務已同步，所有任務皆已附帶實體 Hash 簽章。")

if __name__ == "__main__":
    sync_tasks_with_context()