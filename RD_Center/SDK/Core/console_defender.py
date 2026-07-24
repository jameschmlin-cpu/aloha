# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\RD_Center\SDK\Core\console_defender.py
# 狀態：物理層主控台與異常防禦核心，防止 Unicode 崩潰，並記錄全局 unhandled tracebacks。

import sys
import os
import traceback
from datetime import datetime

class ConsoleDefender:
    def __init__(self):
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        self.encoding = sys.stdout.encoding or 'ascii'
        
    def write_safe(self, text, stream_name):
        # 如果不是 UTF-8 輸出環境，自動過濾/替換 Emojis，防杜 CP950/Big5 UnicodeEncodeError 崩潰
        is_utf8 = 'utf-8' in self.encoding.lower() or 'utf8' in self.encoding.lower()
        if not is_utf8:
            text = text.replace("🚨", "[CRITICAL]")
            text = text.replace("⚠️", "[警告]")
            text = text.replace("✅", "[OK]")
            text = text.replace("❌", "[FAIL]")
            text = text.replace("🌟", "[INFO]")
            text = text.replace("⚡", "[FAST]")
            text = text.replace("🔌", "[LINK]")
            try:
                text.encode(self.encoding)
            except UnicodeEncodeError:
                # 若編碼仍不支援其他特殊符號，將其替換為 "?" 符號以保證系統絕不熔斷
                text = text.encode(self.encoding, errors='replace').decode(self.encoding)
        
        orig = self.original_stdout if stream_name == 'stdout' else self.original_stderr
        orig.write(text)
        orig.flush()

class SafeStreamWrapper:
    def __init__(self, defender, stream, name):
        self.defender = defender
        self.stream = stream
        self.name = name
        
    def write(self, text):
        self.defender.write_safe(text, self.name)
        
    def flush(self):
        self.stream.flush()

def setup_global_defense():
    defender = ConsoleDefender()
    sys.stdout = SafeStreamWrapper(defender, sys.stdout, 'stdout')
    sys.stderr = SafeStreamWrapper(defender, sys.stderr, 'stderr')
    
    def exception_hook(exctype, value, tb):
        err_msg = "".join(traceback.format_exception(exctype, value, tb))
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 尋找 Genesis 根目錄
        def find_genesis_base():
            if "GENESIS_HOME" in os.environ:
                return os.environ["GENESIS_HOME"]
            current = os.path.abspath(__file__)
            while True:
                parent, name = os.path.split(current)
                if name.lower() == "genesis" or os.path.exists(os.path.join(current, "Genesis_Map.json")):
                    return current
                if not name:
                    break
                current = parent
            return r"C:\Genesis"
            
        genesis_base = find_genesis_base()
        log_dir = os.path.join(genesis_base, "logs")
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, "genesis_error.log")
        
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] UNHANDLED EXCEPTION:\n{err_msg}\n{'-'*60}\n")
        except Exception:
            pass
            
        # 乾淨簡短地輸出簡短錯誤到 sys.stderr，防止破壞 CI/CD 等監控腳本解析
        sys.stderr.write(f"[FATAL_EXCEPTION] {exctype.__name__}: {value}\n")
        sys.exit(1)
        
    sys.excepthook = exception_hook
