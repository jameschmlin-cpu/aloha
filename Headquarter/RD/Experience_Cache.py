# C:\Genesis\Headquarter\RD\Experience_Cache.py
import sqlite3
import hashlib

class ExperienceCache:
    def __init__(self, db_path=r"C:\\Genesis\\Genesis_History.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Experience_Cache (
                error_hash TEXT PRIMARY KEY,
                error_message TEXT,
                context_code TEXT,
                successful_patch TEXT,
                prevention_rule TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        conn.close()

    def _hash_error(self, error_message):
        # Normalize: strip spaces, convert to lowercase, take md5
        normalized = str(error_message).strip().lower()
        return hashlib.md5(normalized.encode('utf-8')).hexdigest()

    def cache_experience(self, error_message, context_code, successful_patch, prevention_rule):
        error_hash = self._hash_error(error_message)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO Experience_Cache 
            (error_hash, error_message, context_code, successful_patch, prevention_rule)
            VALUES (?, ?, ?, ?, ?);
        """, (error_hash, error_message, context_code, successful_patch, prevention_rule))
        conn.commit()
        conn.close()
        print(f"[CACHE] 成功存檔專家級經驗 (Hash: {error_hash})")

    def query_experience(self, current_error_message):
        """
        比對當前錯誤訊息，查詢相似的防錯規則與補丁
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT error_message, prevention_rule, successful_patch FROM Experience_Cache;")
        rows = cursor.fetchall()
        conn.close()

        # 基於單字重合度 (Jaccard Similarity) 計算相似度
        current_words = set(str(current_error_message).lower().split())
        best_match = None
        highest_score = 0

        for error_message, prevention_rule, successful_patch in rows:
            db_words = set(error_message.lower().split())
            if not db_words:
                continue
            intersection = current_words.intersection(db_words)
            score = len(intersection) / len(db_words)
            # 閥值設定為 0.35 確保關聯性
            if score > 0.35 and score > highest_score:
                highest_score = score
                best_match = {
                    "error_message": error_message,
                    "prevention_rule": prevention_rule,
                    "successful_patch": successful_patch,
                    "similarity": score
                }

        return best_match

    def inject_rules_into_prompt(self, base_prompt, current_error_message=None):
        """
        將查詢到的防錯規則動態注入 Prompt 中
        """
        rules_text = ""
        if current_error_message:
            match = self.query_experience(current_error_message)
            if match:
                rules_text = (
                    f"\n[⚠️ 偵測到歷史相似錯誤 (相似度: {match['similarity']:.2f})]\n"
                    f"歷史錯誤訊息: {match['error_message']}\n"
                    f"防錯提示與規範: {match['prevention_rule']}\n"
                    f"歷史修復補丁參考:\n```python\n{match['successful_patch']}\n```\n"
                )
        
        # 尋找 {{EXPERIENCE_RULES}} 佔位符進行注入
        placeholder = "{{EXPERIENCE_RULES}}"
        if placeholder in base_prompt:
            return base_prompt.replace(placeholder, rules_text)
        return base_prompt + "\n" + rules_text

if __name__ == "__main__":
    # 測試腳本
    cache = ExperienceCache()
    print("[System] Experience Cache 初始化成功，已建立對接表結構。")
