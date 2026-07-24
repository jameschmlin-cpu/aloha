# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\RD_Center\SDK\System\LightRAG_Engine.py
# 狀態：LightRAG 圖譜檢索引擎 (完整實體版)
# 實體 Hash: 0xGEN-LIGHTRAG-ENGINE-V4

import os
import sys
import json
import time
import asyncio
from lightrag import LightRAG, QueryParam
from lightrag.llm.gemini import gemini_model_complete, gemini_embed
from lightrag.utils import wrap_embedding_func_with_attrs

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

GENESIS_BASE = r"C:\Genesis"
RAG_STORAGE_DIR = os.path.join(GENESIS_BASE, "rag_storage")
LOG_FILE = os.path.join(GENESIS_BASE, "Logs", "LightRAG_Engine.log")

def log_msg(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] [LightRAG Engine] {msg}"
    print(entry)
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry + "\n")

def load_gemini_key():
    key = os.environ.get("GEMINI_API_KEY", "")
    config_path = os.path.join(GENESIS_BASE, "Config", "telegram_config.json")
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                config_key = cfg.get("gemini_api_key", "")
                if config_key and "YOUR_GEMINI_API_KEY" not in config_key:
                    key = config_key
        except Exception as e:
            log_msg(f"讀取金鑰配置失敗: {e}")
    if key:
        os.environ["GEMINI_API_KEY"] = key
    return key

class GenesisLightRAGEngine:
    def __init__(self):
        self.api_key = load_gemini_key()
        if not self.api_key:
            log_msg("[警告] GEMINI_API_KEY 未設定，圖譜引擎可能無法正常運作。")
            
        os.makedirs(RAG_STORAGE_DIR, exist_ok=True)
        self.initialized = False
        
        # 封裝 Gemini LLM，強制注入 API Key 並設定 model (使用 3.5 Flash Lite 輕量又極速)
        async def custom_llm_model_func(prompt, system_prompt=None, history_messages=[], **kwargs):
            return await gemini_model_complete(
                prompt,
                system_prompt=system_prompt,
                history_messages=history_messages,
                api_key=self.api_key,
                model_name="gemini-3.5-flash-lite",
                **kwargs
            )
            
        # 封裝 Gemini Embedding，強制注入 API Key (使用 .func 避開重複包裝衝突)
        async def custom_embedding_func(texts, **kwargs):
            return await gemini_embed.func(
                texts,
                api_key=self.api_key,
                **kwargs
            )
            
        # 複製原本 embedding 裝飾器屬性，並強制啟用 send_dimensions 以傳遞 1536 維度參數
        custom_embed_func = wrap_embedding_func_with_attrs(
            embedding_dim=1536,
            max_token_size=2048,
            model_name="gemini-embedding-001",
            supports_asymmetric=True,
            send_dimensions=True
        )(custom_embedding_func)
            
        self.rag = LightRAG(
            working_dir=RAG_STORAGE_DIR,
            llm_model_func=custom_llm_model_func,
            llm_model_name="gemini-3.5-flash-lite", # 確保 hashing_kv 不會覆寫成預設的 gpt-4o-mini
            embedding_func=custom_embed_func
        )
        
    async def ensure_initialized(self):
        if not self.initialized:
            await self.rag.initialize_storages()
            self.initialized = True

    async def index_all_sources_async(self):
        await self.ensure_initialized()
        log_msg("=== 開始執行知識圖譜建庫與增量索引 ===")
        # 需要索引的目標目錄與檔案
        targets = [
            (os.path.join(GENESIS_BASE, "RD_Center", "SDK"), [".py"]),
            (os.path.join(GENESIS_BASE, "RD_Center", "SDK_Bricks"), [".py"]),
            (os.path.join(GENESIS_BASE, "Library", "Rules"), [".py"]),
            (os.path.join(GENESIS_BASE, "SOP_Manual.txt"), None),
            (os.path.join(GENESIS_BASE, "TASKS.md"), None)
        ]
        
        total_indexed = 0
        for path, exts in targets:
            if not os.path.exists(path):
                continue
            if os.path.isfile(path):
                try:
                    await self._index_file_async(path)
                    total_indexed += 1
                except Exception as e:
                    log_msg(f"索引檔案出錯 {path}: {e}")
            else:
                for root, _, files in os.walk(path):
                    # 排除不必要的目錄
                    if any(x in root for x in ["__pycache__", ".venv", "Backup", "Logs", "cache", "rag_storage"]):
                        continue
                    for f in files:
                        _, ext = os.path.splitext(f)
                        if exts is None or ext.lower() in exts:
                            filepath = os.path.join(root, f)
                            try:
                                await self._index_file_async(filepath)
                                total_indexed += 1
                            except Exception as e:
                                log_msg(f"索引檔案出錯 {f}: {e}")
        log_msg(f"=== 增量建庫完成，共處理 {total_indexed} 個檔案項目 ===")

    async def _index_file_async(self, filepath):
        # 讀取檔案內容
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        if len(content.strip()) < 20:
            return
            
        # 加上結構化 Metadata 前綴
        formatted_content = (
            f"--- Document Source ---\n"
            f"File Path: {filepath}\n"
            f"File Name: {os.path.basename(filepath)}\n"
            f"Last Modified: {time.ctime(os.path.getmtime(filepath))}\n"
            f"Content:\n{content}\n"
        )
        
        # 執行插入 (LightRAG 的 ainsert 會自動做增量與實體解析)
        await self.rag.ainsert(formatted_content)
        log_msg(f"  [+] 已成功索引: {filepath}")

    async def query_async(self, query_text, mode="hybrid"):
        await self.ensure_initialized()
        log_msg(f"正在執行圖譜檢索 (模式: {mode}): {query_text}")
        start_time = time.time()
        result = await self.rag.aquery(query_text, param=QueryParam(mode=mode))
        duration = time.time() - start_time
        log_msg(f"檢索完成，耗時 {duration:.2f} 秒。")
        return result

    def index_all_sources(self):
        asyncio.run(self.index_all_sources_async())

    def query(self, query_text, mode="hybrid"):
        return asyncio.run(self.query_async(query_text, mode))

def main():
    engine = GenesisLightRAGEngine()
    
    # 支援指令列參數
    if len(sys.argv) > 1:
        cmd = sys.argv[1].strip().lower()
        if cmd == "build":
            engine.index_all_sources()
        elif cmd == "query" and len(sys.argv) > 2:
            q = sys.argv[2]
            res = engine.query(q)
            print(f"\n[LightRAG 檢索結果]:\n{res}")
        else:
            print("未知指令。用法: python LightRAG_Engine.py [build | query \"你的問題\"]")
    else:
        # 預設執行快速檢核
        log_msg("=== LightRAG Engine 檢核模式 ===")
        # 先做一個小測試
        test_q = "列出 SDK 系統的主要通訊模組"
        res = engine.query(test_q)
        print(f"測試檢索結果:\n{res}")

if __name__ == "__main__":
    main()