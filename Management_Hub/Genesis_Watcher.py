# -*- coding: utf-8 -*-
# - C:\Genesis\Management_Hub\Genesis_Watcher.py
import os
import sqlite3
from watchdog.events import FileSystemEventHandler

DB_PATH = r"C:\Genesis\Database\Path_Registry.db"

class RegistryHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith((".py", ".json", ".md")):
            self._update_db(event.src_path)

    def _update_db(self, file_path):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        mod_name = os.path.basename(file_path).split('.')[0]
        cursor.execute("INSERT OR REPLACE INTO path_map (module_name, physical_path) VALUES (?, ?)", 
                       (mod_name, file_path))
        conn.commit()
        conn.close()

def full_scan():
    """執行全機路徑初次建置"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS path_map (module_name TEXT PRIMARY KEY, physical_path TEXT)")
    for root, _, files in os.walk(r"C:\Genesis"):
        for f in files:
            if f.endswith((".py", ".json", ".md")):
                path = os.path.join(root, f)
                cursor.execute("INSERT OR REPLACE INTO path_map VALUES (?, ?)", (f.split('.')[0], path))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    full_scan()
    print("[SYSTEM] 基礎路徑庫已建立。")