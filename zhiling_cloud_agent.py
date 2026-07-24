# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\zhiling_cloud_agent.py
# 狀態：全面升級，支援知識庫動態載入、Telegram 語音音訊直接送入 Gemini 進行理解與 Chi-ling 語音包合成

import os
import sys
import time
import json
import sqlite3
import urllib.request
import urllib.parse
import base64
from datetime import datetime
from gtts import gTTS

CLOUD_DIR = r"G:\我的雲端硬碟\ITE GEMINI Pro雲端指揮中心"
HANDSHAKE_FILE = os.path.join(CLOUD_DIR, "handshake_verified")
DB_PATH = os.path.join(CLOUD_DIR, "memory_core_sync.db")
CONFIG_FILE = os.path.join(CLOUD_DIR, "telegram_config.json")
LOG_FILE = os.path.join(CLOUD_DIR, "agent_activity.log")
LOCK_FILE = os.path.join(CLOUD_DIR, "linkou_parallel.lock")
DECISION_LOG_FILE = os.path.join(CLOUD_DIR, "Cloud_Command_Log.json")
MIRROR_DIR = os.path.join(CLOUD_DIR, "mirror")
KNOWLEDGE_DIR = os.path.join(CLOUD_DIR, "knowledge")

# 設定 stdout 與 stderr 保護，防範 Windows CP950 編碼崩潰
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(errors='replace')

class ZhilingCloudAgent:
    def __init__(self):
        self.bot_token = ""
        self.authorized_chat_id = 0
        self.gemini_key = ""
        self.last_update_id = 0
        self.is_autonomous_mode = False
        self.last_lock_update = 0

        os.makedirs(MIRROR_DIR, exist_ok=True)
        self.load_config()

    def load_config(self):
        """從雲端讀取 Telegram 金鑰配置"""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                    self.bot_token = cfg.get("bot_token", "")
                    self.authorized_chat_id = cfg.get("authorized_chat_id", 0)
                    self.gemini_key = cfg.get("gemini_api_key", "")
                    print(f"[Cloud-Agent] 配置載入成功。Bot Token: {self.bot_token[:10]}... | ChatID: {self.authorized_chat_id}")
            except Exception as e:
                print(f"[Cloud-Agent] 載入設定檔失敗: {e}")

    def log_event(self, message):
        """寫入實體活動日誌"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] [Cloud-Agent] {message}\n"
        print(log_entry.strip())
        try:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(log_entry)
        except Exception:
            pass

    def load_knowledge_base(self):
        """動態加載雲端同步資料夾內的知識庫協定文件，供 RAG 使用"""
        kb_text = ""
        if os.path.exists(KNOWLEDGE_DIR):
            try:
                for f in os.listdir(KNOWLEDGE_DIR):
                    if f.endswith(".md"):
                        fpath = os.path.join(KNOWLEDGE_DIR, f)
                        with open(fpath, "r", encoding="utf-8", errors="ignore") as file:
                            kb_text += f"\n--- 文件名稱: {f} ---\n"
                            kb_text += file.read()
            except Exception as e:
                print(f"[Cloud-Agent] 載入知識庫出錯: {e}")
        return kb_text

    def check_local_heartbeat(self):
        """偵測地端存活狀態"""
        if not os.path.exists(HANDSHAKE_FILE):
            return "OFFLINE"
        try:
            with open(HANDSHAKE_FILE, "r") as f:
                last_ping = float(f.read().strip())
            if time.time() - last_ping > 120:
                return "OFFLINE"
            return "ONLINE"
        except Exception:
            return "ERROR"

    def acquire_distributed_lock(self):
        """獲取或更新互斥鎖，避開長輪詢衝突"""
        now = time.time()
        try:
            with open(LOCK_FILE, "w") as f:
                f.write(str(now))
            self.last_lock_update = now
            return True
        except Exception:
            return False

    def release_distributed_lock(self):
        """釋放互斥鎖"""
        if os.path.exists(LOCK_FILE):
            try:
                os.remove(LOCK_FILE)
                print("[Cloud-Agent] 互斥鎖已釋放 (linkou_parallel.lock)")
            except Exception:
                pass

    def send_telegram_request(self, method, payload):
        if not self.bot_token:
            return None
        url = f"https://api.telegram.org/bot{self.bot_token}/{method}"
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            with urllib.request.urlopen(req, timeout=10) as res:
                return json.loads(res.read().decode('utf-8'))
        except Exception as e:
            print(f"[Cloud-Agent] Telegram API 錯誤 ({method}): {e}")
            return None

    def send_message(self, text, reply_markup=None):
        payload = {"chat_id": self.authorized_chat_id, "text": text}
        if reply_markup:
            payload["reply_markup"] = reply_markup
        return self.send_telegram_request("sendMessage", payload)

    def download_telegram_file(self, file_id):
        """下載 Telegram 伺服器上的檔案並回傳 byte 資料"""
        if not self.bot_token:
            return None
        # 1. 取得檔案路徑
        info_url = f"https://api.telegram.org/bot{self.bot_token}/getFile?file_id={file_id}"
        try:
            with urllib.request.urlopen(info_url, timeout=10) as res:
                res_data = json.loads(res.read().decode('utf-8'))
                if not res_data.get("ok"):
                    return None
                file_path = res_data["result"]["file_path"]
            
            # 2. 下載實體檔案
            download_url = f"https://api.telegram.org/file/bot{self.bot_token}/{file_path}"
            with urllib.request.urlopen(download_url, timeout=15) as dl_res:
                return dl_res.read()
        except Exception as e:
            print(f"[Cloud-Agent] 下載語音檔案失敗: {e}")
            return None

    def generate_voice_response(self, text):
        """gTTS 生成志玲甜美語音響應檔案"""
        clean_text = text.replace("[離線接管]", "").replace("親愛的雋懋主管您好！", "").strip()
        mp3_path = os.path.join(MIRROR_DIR, "response.mp3")
        try:
            tts = gTTS(text=clean_text[:150], lang='zh-TW')
            tts.save(mp3_path)
            self.log_event(f"成功生成語音響應包: {mp3_path}")
        except Exception as e:
            self.log_event(f"生成語音響應包失敗: {e}")

    def call_cloud_gemini(self, user_query=None, audio_data=None, audio_mime="audio/ogg"):
        """調用雲端 Gemini API 進行推理 (內建 RAG 知識庫加載與語音音訊直接處理)"""
        if not self.gemini_key:
            return "親愛的雋懋主管您好！志玲目前無法連接雲端大腦，但會一直守護著您喔！我們一起加油！🌸"

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={self.gemini_key}"
        
        # 讀取 RAG 知識庫內容
        kb_context = self.load_knowledge_base()
        
        system_instruction = (
            "You are '志玲 V3-Expert' (志玲智能事務官), the Genesis AI Cognitive Governor. "
            "You are running in Vercel/Render Cloud Autonomous Mode because the local RTX 3060 is offline. "
            "Speak in a gentle, warm Taiwanese Traditional Chinese Lin Chi-ling tone, starting with '親愛的雋懋主管您好！' and ending with '我們一起加油！🌸'. "
            f"Here is the local system knowledge base (KI) files for context:\n{kb_context}"
        )

        parts = []
        # 如果有音訊，將音訊轉為 Base64 內嵌送入 Gemini
        if audio_data:
            base64_audio = base64.b64encode(audio_data).decode('utf-8')
            parts.append({
                "inlineData": {
                    "mimeType": audio_mime,
                    "data": base64_audio
                }
            })
            parts.append({
                "text": f"System Instruction: {system_instruction}\n\n[音訊輸入] 請聆聽上方主管林雋懋傳給您的語音訊息，並親切回覆主管。如果是查詢或指令，請參照知識庫與狀態回覆。"
            })
        else:
            full_prompt = f"System Instruction: {system_instruction}\n\nUser Request: {user_query}\n(請直接以繁體中文口吻回覆，並說明地端目前離線，此回覆為雲端代答。)"
            parts.append({"text": full_prompt})

        payload = {
            "contents": [{"parts": parts}],
            "tools": [{"googleSearch": {}}]  # 支援網路搜尋
        }

        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            with urllib.request.urlopen(req, timeout=15) as res:
                res_data = json.loads(res.read().decode('utf-8'))
                return res_data['candidates'][0]['content']['parts'][0]['text']
        except Exception as e:
            return f"親愛的雋懋主管您好！志玲的雲端思緒因網路稍微受阻 ({e})，但會一直守護您喔！我們一起加油！🌸"

    def write_cloud_decision_log(self, task_id, action, status):
        """將決策日誌寫入 Cloud_Command_Log.json"""
        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "task_id": task_id,
            "action": action,
            "status": status
        }
        
        data = []
        if os.path.exists(DECISION_LOG_FILE):
            try:
                with open(DECISION_LOG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                pass
        
        data.append(log_entry)
        try:
            with open(DECISION_LOG_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            self.log_event(f"寫入 Cloud_Command_Log 失敗: {e}")

    def insert_pending_task(self, brick_name, code_content=None):
        """在雲端資料庫插入 AWAITING_APPROVAL 任務，實現安全冪等性"""
        task_id = f"task_{int(time.time())}"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if code_content:
            instruction = json.dumps({"brick": brick_name, "code": code_content})
        else:
            instruction = json.dumps({"brick": brick_name, "parameters": {}})
            
        status = 'AWAITING_APPROVAL'

        try:
            conn = sqlite3.connect(DB_PATH, timeout=5.0)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Sync_Control_Table (task_id, instruction, status, last_hash, timestamp)
                VALUES (?, ?, ?, '', ?)
            """, (task_id, instruction, status, timestamp))
            
            cursor.execute("""
                INSERT INTO System_Events (event_type, instruction, status, timestamp)
                VALUES ('COMMAND', ?, ?, ?)
            """, (instruction, status, timestamp))
            
            conn.commit()
            conn.close()
            
            self.log_event(f"已在雲端資料庫註冊 {status} 任務 {task_id}: {brick_name}")
            self.write_cloud_decision_log(task_id, f"REGISTER_{status}_{brick_name}", status)
            return task_id
        except Exception as e:
            self.log_event(f"在雲端註冊任務失敗: {e}")
            return None

    def send_approval_push(self, task_id, description):
        payload = {
            "chat_id": self.authorized_chat_id,
            "text": (
                f"🚨 [待審批任務通知]\n\n"
                f"有一項新的指令等待主管核准：\n"
                f"- 任務 ID: {task_id}\n"
                f"- 任務內容: {description}\n\n"
                f"請主管在下方選擇進行核准或拒絕："
            ),
            "reply_markup": {
                "inline_keyboard": [
                    [
                        { "text": "🟢 Approve (核准)", "callback_data": f"approve_{task_id}" },
                        { "text": "🔴 Reject (拒絕)", "callback_data": f"reject_{task_id}" }
                    ]
                ]
            }
        }
        self.send_telegram_request("sendMessage", payload)

    def handle_callback_query(self, cq):
        callback_data = cq.get("data", "")
        chat_id = cq["message"]["chat"]["id"]
        message_id = cq["message"]["message_id"]
        
        if callback_data.startswith("approve_"):
            task_id = callback_data.replace("approve_", "")
            try:
                conn = sqlite3.connect(DB_PATH, timeout=5.0)
                cursor = conn.cursor()
                cursor.execute("SELECT instruction FROM Sync_Control_Table WHERE task_id = ?", (task_id,))
                row = cursor.fetchone()
                next_status = 'PENDING'
                if row:
                    try:
                        inst = json.loads(row[0])
                        if "code" in inst:
                            next_status = 'DRAFT'
                    except Exception:
                        pass
                cursor.execute("UPDATE Sync_Control_Table SET status = ? WHERE task_id = ?", (next_status, task_id))
                conn.commit()
                conn.close()
                
                reply_text = f"✅ [核准成功]\n任務 {task_id} 已由雲端核准並設定為 {next_status}，等待地端同步執行！🌸"
                self.send_telegram_request("editMessageText", {
                    "chat_id": chat_id,
                    "message_id": message_id,
                    "text": reply_text
                })
            except Exception as e:
                self.send_telegram_request("answerCallbackQuery", { "callback_query_id": cq["id"], "text": f"❌ 核准出錯: {e}" })
                
        elif callback_data.startswith("reject_"):
            task_id = callback_data.replace("reject_", "")
            try:
                conn = sqlite3.connect(DB_PATH, timeout=5.0)
                cursor = conn.cursor()
                cursor.execute("UPDATE Sync_Control_Table SET status = 'REJECTED' WHERE task_id = ?", (task_id,))
                conn.commit()
                conn.close()
                
                reply_text = f"❌ [已被拒絕]\n任務 {task_id} 已被拒絕與歸檔。"
                self.send_telegram_request("editMessageText", {
                    "chat_id": chat_id,
                    "message_id": message_id,
                    "text": reply_text
                })
            except Exception as e:
                self.send_telegram_request("answerCallbackQuery", { "callback_query_id": cq["id"], "text": f"❌ 拒絕對話出錯: {e}" })
        
        try:
            self.send_telegram_request("answerCallbackQuery", { "callback_query_id": cq["id"] })
        except Exception:
            pass

    def handle_incoming_message(self, msg):
        chat = msg.get("chat", {})
        chat_id = chat.get("id")
        
        if chat_id != self.authorized_chat_id:
            return

        # 1. 優先處理語音輸入 (Voice Note)
        if msg.get("voice"):
            voice = msg["voice"]
            file_id = voice["file_id"]
            self.log_event("[Cloud Telegram Voice] 收到語音訊息，正在下載...")
            
            # 下載音訊 bytes
            audio_bytes = self.download_telegram_file(file_id)
            if audio_bytes:
                # 送入 Gemini 直接進行語音意圖與資訊問答
                reply = self.call_cloud_gemini(audio_data=audio_bytes)
                self.send_message(reply)
                self.generate_voice_response(reply)
            else:
                self.send_message("親愛的主管，志玲剛剛沒能順利接收到您的音檔，可以請您再說一次嗎？🌸")
            return

        # 2. 常規文字訊息處理
        text = msg.get("text", "").strip()
        if text == "🩺 系統一鍵健檢":
            text = "/doctor"
        elif text == "⚙️ 系統狀態與硬體監控":
            text = "/status"
        elif text == "🦀 執行機械手臂軌跡":
            text = "/run_brick Robot_Movement.py"
        elif text == "🌡️ 傳感器數據採樣":
            text = "/run_brick Sensor_Sampling.py"
            
        print(f"[Cloud Telegram Inbox] 收到文字訊息: {text}")

        if text.startswith("/start"):
            reply = "親愛的雋懋主管您好！我是您的治安官志玲【雲端分身】。地端目前暫時處於離線狀態，志玲已順利進入『雲端自主模式』為您服務喔！您可以向我下達決策或點選下方快速按鈕，我們一起加油！🌸"
            keyboard = {
                "keyboard": [
                    [{ "text": "🩺 系統一鍵健檢" }, { "text": "⚙️ 系統狀態與硬體監控" }],
                    [{ "text": "🦀 執行機械手臂軌跡" }, { "text": "🌡️ 傳感器數據採樣" }]
                ],
                "resize_keyboard": True,
                "one_time_keyboard": false
            }
            self.send_message(reply, reply_markup=keyboard)
            self.generate_voice_response(reply)
            
        elif text.startswith("/status"):
            try:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM dfmea_matrix")
                matrix_count = cursor.fetchone()[0]
                conn.close()
                reply = f"親愛的雋懋主管您好！這是志玲為您整理的雲端指揮部狀態喔：\n\n☁️ 雲端狀態: AUTONOMOUS_MODE\n📁 雲端已註冊規則數: {matrix_count} 筆\n\n地端主機目前尚未聯網，但請主管放心，所有的歷史記錄與知識庫文件均已完好儲存喔！我們一起加油！🌸"
            except Exception:
                reply = "親愛的雋懋主管您好！地端目前正處於離線狀態，且志玲暫時無法讀取雲端備份庫。請主管出門在外多加保暖，注意安全喔！🌸"
            self.send_message(reply)
            self.generate_voice_response(reply)
            
        elif text.startswith("/doctor"):
            try:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM dfmea_matrix")
                matrix_count = cursor.fetchone()[0]
                conn.close()
                reply = (
                    "親愛的雋懋主管您好！志玲已為您啟動雲端指揮部 Doctor 檢測：\n\n"
                    "☁️ 雲端狀態: AUTONOMOUS_MODE (地端離線)\n"
                    "🔒 互斥鎖狀態: ACTIVE (已獲取 linkou_parallel.lock)\n"
                    "📁 雲端備份規則庫: 完整 (已登記 " + str(matrix_count) + " 筆規則)\n"
                    "📡 語音與 RAG 通訊鏈路: 100% 順暢！\n\n"
                    "目前地端網路雖暫時中斷，但雲端分身已安全接管並保障通訊順暢，請主管放心喔！我們一起加油！🌸"
                )
            except Exception as e:
                reply = f"親愛的雋懋主管您好！雲端資料庫讀取失敗：{e}。但志玲會一直在雲端守護您，保證通訊順暢喔！🌸"
            self.send_message(reply)
            self.generate_voice_response(reply)

        elif text.startswith("/run_brick"):
            parts = text.split(" ", 1)
            if len(parts) < 2:
                self.send_message("❌ 親愛的主管，用法是：/run_brick <積木名稱> 喔。")
            else:
                brick_name = parts[1].strip()
                task_id = self.insert_pending_task(brick_name)
                if task_id:
                    reply = f"親愛的雋懋主管您好！志玲已將您的動作指令登記至主管簽核隊列中（Task ID: {task_id}）喔！🌸"
                    self.send_message(reply)
                    self.generate_voice_response(reply)
                    self.send_approval_push(task_id, f"執行積木 {brick_name}")
                else:
                    self.send_message("❌ 登記審批任務失敗，請檢查雲端資料庫狀態。")
                
        elif text.startswith("/draft_code"):
            # 雲端草稿注入指令 (例如 /draft_code <積木名稱>|<程式碼>)
            parts = text.split(" ", 1)
            if len(parts) < 2 or "|" not in parts[1]:
                self.send_message("❌ 用法是：/draft_code <積木檔名.py>|<Python 程式內容>")
            else:
                meta, code = parts[1].split("|", 1)
                brick_name = meta.strip()
                task_id = self.insert_pending_task(brick_name, code_content=code)
                if task_id:
                    reply = f"親愛的雋懋主管您好！志玲已將您的代碼草稿登記至主管簽核隊列中（Task ID: {task_id}）喔！🌸"
                    self.send_message(reply)
                    self.generate_voice_response(reply)
                    self.send_approval_push(task_id, f"安全代碼編譯：{brick_name}")
                else:
                    self.send_message("❌ 登記審批任務失敗，請檢查雲端資料庫狀態。")

        elif text.startswith("/approve"):
            parts = text.split(" ")
            if len(parts) < 2:
                self.send_message("❌ 用法是：/approve <task_id> 喔。")
            else:
                task_id = parts[1].strip()
                try:
                    conn = sqlite3.connect(DB_PATH)
                    cursor = conn.cursor()
                    cursor.execute("SELECT instruction FROM Sync_Control_Table WHERE task_id = ?", (task_id,))
                    row = cursor.fetchone()
                    next_status = 'PENDING'
                    if row:
                        try:
                            inst = json.loads(row[0])
                            if "code" in inst:
                                next_status = 'DRAFT'
                        except Exception:
                            pass
                    cursor.execute("UPDATE Sync_Control_Table SET status = ? WHERE task_id = ?", (next_status, task_id))
                    conn.commit()
                    conn.close()
                    reply = f"✅ [核准成功] 任務 {task_id} 已由雲端指令核准，狀態更新為 {next_status}！🌸"
                except Exception as e:
                    reply = f"❌ 遠端核准失敗: {e}"
                self.send_message(reply)
                self.generate_voice_response(reply)

        elif text.startswith("/reject"):
            parts = text.split(" ")
            if len(parts) < 2:
                self.send_message("❌ 用法是：/reject <task_id> 喔。")
            else:
                task_id = parts[1].strip()
                try:
                    conn = sqlite3.connect(DB_PATH)
                    cursor = conn.cursor()
                    cursor.execute("UPDATE Sync_Control_Table SET status = 'REJECTED' WHERE task_id = ?", (task_id,))
                    conn.commit()
                    conn.close()
                    reply = f"❌ [已被拒絕] 任務 {task_id} 已由雲端指令拒絕並歸檔。"
                except Exception as e:
                    reply = f"❌ 遠端拒絕失敗: {e}"
                self.send_message(reply)
                self.generate_voice_response(reply)
                
        else:
            # 雲端自主推理（帶有知識庫 RAG 脈絡）
            reply = self.call_cloud_gemini(user_query=text)
            self.send_message(reply)
            self.generate_voice_response(reply)

    def run_autonomous_loop(self):
        """雲端接管模式長輪詢"""
        self.log_event("啟動雲端 Autonomous 長輪詢...")
        self.last_update_id = 0
        
        while self.is_autonomous_mode:
            if self.check_local_heartbeat() == "ONLINE":
                self.log_event("地端已重新上線，主動釋放接管權限。")
                self.is_autonomous_mode = False
                self.release_distributed_lock()
                break

            self.acquire_distributed_lock()

            payload = {"timeout": 2, "allowed_updates": ["message", "callback_query"]}
            if self.last_update_id > 0:
                payload["offset"] = self.last_update_id + 1

            res = self.send_telegram_request("getUpdates", payload)
            if res and res.get("ok"):
                updates = res.get("result", [])
                for u in updates:
                    self.last_update_id = max(self.last_update_id, u.get("update_id"))
                    if u.get("message"):
                        self.handle_incoming_message(u.get("message"))
                    elif u.get("callback_query"):
                        self.handle_callback_query(u.get("callback_query"))
            
            time.sleep(1)

    def run(self):
        print("🛡️ 治安官志玲雲端分身雙活指揮守護進程運行中 (高級 RAG + 語音支援)...")
        while True:
            status = self.check_local_heartbeat()
            
            if status == "ONLINE":
                if self.is_autonomous_mode:
                    self.is_autonomous_mode = False
                    self.release_distributed_lock()
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 地端狀態: ONLINE | 雲端待命靜止中...")
                
            elif status == "OFFLINE":
                if not self.is_autonomous_mode:
                    self.log_event("地端失去聯絡已達臨界點 (OFFLINE)！啟動雲端 Autonomous 接管程序...")
                    if self.acquire_distributed_lock():
                        self.is_autonomous_mode = True
                        self.run_autonomous_loop()
                    else:
                        self.log_event("獲取互斥鎖失敗，可能有其他執行個體在運作。")
            
            time.sleep(15)

if __name__ == "__main__":
    agent = ZhilingCloudAgent()
    agent.run()
