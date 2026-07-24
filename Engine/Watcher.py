# C:\Genesis\Engine\Watcher.py
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class GenesisHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory: return
        if event.src_path.endswith(".py"):
            print(f"[監控器] 偵測到新任務: {event.src_path}")
            # 自動呼叫引擎進行指紋識別與歸位
            os.system("python C:\Genesis\Engine\Genesis_Core_Engine.py")

def start_watcher():
    path = r"C:\Genesis"
    event_handler = GenesisHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    print("[啟動] 監控系統已就緒，即時偵測中...")
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    start_watcher()