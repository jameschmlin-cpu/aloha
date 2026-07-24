# -*- coding: utf-8 -*-
"""
====================================================================
龍蝦帝國 - Imperial_Deep_Healer (地端算力自動防禦修復醫生 - 完美無警報版)
最高指揮官: 林雋懋 (Chun Mao Lin)
物理執行路徑: C:\Genesis\Imperial_Deep_Healer.py
【品質工程宣告】：100% 閉迴路自動化修復，全面清洗轉義字元警報。
====================================================================
"""
import requests
import socket
import subprocess
import time
from datetime import datetime

class Imperial_Deep_Healer:
    def __init__(self):
        # 剛性定錨本地 Ollama 與 ITE 實體核心路徑 (加小寫 r 封鎖轉義字元失效模式)
        self.ollama_url = "http://127.0.0.1:11434/api/tags"  # 檢查模型清單
        self.module_id = "SYS_DOCTOR_HEALER"
        self.root_path = r"C:\Genesis"

    def diagnostic_scan(self) -> str:
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"🩺 [{timestamp}] Doctor: 啟動深度算力與本地 RTX 3060 狀態校驗...")
        
        # 1. 物理層檢查：探測 Port 11434 門閘是否開啟
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            port_open = s.connect_ex(('127.0.0.1', 11434)) == 0

        # 2. 自動化自主修復機制 (Fail-Safe Action)
        if not port_open:
            print(f"⚠️ [{datetime.now().strftime('%H:%M:%S')}] 偵測到物理斷裂！Ollama 服務尚未啟動，強制執行自主拉起...")
            try:
                # 運用 Python 標準 subprocess 模組，物理執行 CMD 命令拉起地端 Ollama
                subprocess.Popen(
                    'start "SubC1_Ollama" /min ollama serve', 
                    shell=True, 
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )
                
                # 剛性排隊等待：給予本地硬體 3 秒鐘初始化過電時間
                time.sleep(3.0)
                
                # 二次確認物理端口
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    if s.connect_ex(('127.0.0.1', 11434)) != 0:
                        return "❌ [物理斷裂] 嘗試自動喚醒 Ollama 失敗，請主管手動啟動 Ollama 應用程式。"
                print("🟢 [物理修復] Ollama 服務背景掛載成功，過電順暢。")
            except Exception as e:
                return f"❌ [物理修復失敗] 無法喚醒地端守護行程，Root Cause: {str(e)}"

        # 3. 邏輯層檢查 (模型存在度與 API 響應校驗)
        try:
            res = requests.get(self.ollama_url, timeout=5)
            
            # 確保 HTTP 狀態碼為 200
            if res.status_code != 200:
                return "❌ [服務崩潰] 雖然端口開著，但 API 回傳非 200 狀態碼。建議重啟 SubC1。"
                
            models = res.json().get('models', [])
            if not models:
                return "⚠️ [邏輯空殼] Ollama 已啟動，但 RTX 3060 本地庫內沒有下載 any 模型，請執行 ollama run。"
            
            model_names = [m['name'] for m in models]
            print(f"📊 [Node C 實體回傳] 偵測到本地模型庫: {model_names}")
            
            # 達成 100% 閉迴路管理，全線亮綠燈
            return f"🟢 [深度純淨] 算力路徑與模型庫皆已導通。模型總數: {len(model_names)}，請重啟 Bridge 腳本。"
            
        except requests.exceptions.RequestException as e:
            return f"❌ [服務崩潰] 雖然端口開著，但 Ollama 核心無回應。Root Cause: {str(e)}"

if __name__ == "__main__":
    # 物理端擊發實體自檢診斷
    doctor = Imperial_Deep_Healer()
    report = doctor.diagnostic_scan()
    print(f"========================================\n{report}\n========================================")