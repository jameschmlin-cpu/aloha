import sqlite3
class PathResolver:
    def __init__(self, db_path=r"C:\Genesis\Database\Path_Register.db"):
        self.db_path = db_path
    def get(self, alias):
        conn = sqlite3.connect(self.db_path)
        res = conn.execute("SELECT full_path FROM path_table WHERE alias = ?", (alias,)).fetchone()
        conn.close()
        return res[0] if res else None