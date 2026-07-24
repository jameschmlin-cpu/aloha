# -*- coding: utf-8 -*-
# Compiled Brick from: Genesis_Core.py
# Category: Core

class GenesisCoreBrick:
    def run(self, ctx=None):
        try:
            import sqlite3
            import hashlib
            import os
            import time

            class Genesis_Core:
                def __init__(self):
                    self.DB_PATH = r"C:\Genesis\Database\Genesis_history.db"
                    if not os.path.exists(r"C:\Genesis\Database"):
                        os.makedirs(r"C:\Genesis\Database", exist_ok=True)
                    os.chdir(r"C:\Genesis")
                    self._initialize_core()

                def _initialize_core(self):
                    conn = sqlite3.connect(self.DB_PATH)
                    conn.execute('''CREATE TABLE IF NOT EXISTS conversation_log 
                                    (id INTEGER PRIMARY KEY AUTOINCREMENT, actor TEXT, summary TEXT, hash TEXT)''')
                    conn.commit()
                    conn.close()

                def log_and_verify(self, content, actor):
                    # 1. 摘要與 Hash 計算
                    summary = (content[:15] + "...") if len(content) > 15 else content
                    h = hashlib.sha256(content.encode('utf-8')).hexdigest()

                    # 2. 物理寫入
                    conn = sqlite3.connect(self.DB_PATH)
                    conn.execute("INSERT INTO conversation_log (actor, summary, hash) VALUES (?, ?, ?)", 
                                 (actor, summary, h))
                    conn.commit()

                    # 3. 0.1秒延遲後抓取 (驗證入庫)
                    time.sleep(0.1)
                    row = conn.execute("SELECT actor, summary, hash FROM conversation_log ORDER BY id DESC LIMIT 1").fetchone()
                    conn.close()

                    # 4. 螢幕回顯 (回饋給主管)
                    print(f"\n[物理存證回顯] {row[0]} 回復已存入資料庫")
                    print(f"摘要: {row[1]} | Hash: {row[2][:8]}")

                def run(self):
                    print("【監控服務 V10.0 啟動】同步讀寫回顯模式已就緒")
                    while True:
                        text = input(">> 輸入指令/內容: ")
                        if text.lower() == 'exit': break

                        # 您輸入的內容寫入並回顯
                        self.log_and_verify(text, "主管")

                        # Gemini 的模擬回覆寫入並回顯
                        self.log_and_verify("系統已更新數據。", "Gemini")

            if __name__ == "__main__":
                Genesis_Core().run()
        except Exception as e:
            print(f"[GenesisCoreBrick] 運行失敗: {e}")
            return False
        return True
