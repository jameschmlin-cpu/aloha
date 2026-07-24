import sqlite3
from genesis_path import PathResolver
class GenesisGateway:
    def __init__(self):
        self.paths = PathResolver()
    def log(self, db_alias, context):
        conn = sqlite3.connect(self.paths.get(db_alias))
        conn.execute("INSERT INTO interaction_history (context) VALUES (?)", (context,))
        conn.commit()
        conn.close()