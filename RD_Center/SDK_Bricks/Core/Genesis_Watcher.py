# -*- coding: utf-8 -*-
# Compiled Brick from: Genesis_Watcher.py
# Category: Core

class GenesisWatcherBrick:
    def run(self, ctx=None):
        try:
            # -*- coding: utf-8 -*-
            import os
            import sqlite3
            import time
            from watchdog.observers import Observer
            from watchdog.events import FileSystemEventHandler

            # 核心路徑與資料庫定義
            ROOT_DIR = r"C:\Genesis"
            DB_PATH = r"C:\Genesis\Database\Path_Registry.db"

            class GenesisRegistryHandler(FileSystemEventHandler):
                """即時監控事件處理器"""
                def __init__(self, conn):
                    self.conn = conn

                def on_created(self, event):
                    if not event.is_directory:
                        self._update_db(event.src_path)

                def _update_db(self, file_path):
                    module_name = os.path.basename(file_path).split('.')[0]
                    cursor = self.conn.cursor()
                    cursor.execute("INSERT OR REPLACE INTO path_map (module_name, physical_path) VALUES (?, ?)", 
                                   (module_name, file_path))
                    self.conn.commit()
                    print(f"[AUTO-SYNC] 新檔案入庫: {module_name} -> {file_path}")

            def init_registry():
                """初始化資料庫與全域掃描"""
                os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute("CREATE TABLE IF NOT EXISTS path_map (module_name TEXT PRIMARY KEY, physical_path TEXT)")

                # 第一次全域掃描
                print("[INIT] 執行全域掃描...")
                for root, _, files in os.walk(ROOT_DIR):
                    for file in files:
                        if file.endswith((".py", ".md", ".json")):
                            full_path = os.path.join(root, file)
                            module_name = file.split('.')[0]
                            cursor.execute("INSERT OR REPLACE INTO path_map (module_name, physical_path) VALUES (?, ?)", 
                                           (module_name, full_path))
                conn.commit()
                return conn

            if __name__ == "__main__":
                conn = init_registry()

                # 啟動即時監控
                event_handler = GenesisRegistryHandler(conn)
                observer = Observer()
                observer.schedule(event_handler, ROOT_DIR, recursive=True)
                observer.start()

                print(f"[STATUS] Genesis 監控節點已啟動，監控路徑: {ROOT_DIR}")
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    observer.stop()
                observer.join()
        except Exception as e:
            print(f"[GenesisWatcherBrick] 運行失敗: {e}")
            return False
        return True
