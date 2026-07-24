# -*- coding: utf-8 -*-
import sys
import os

# ==========================================================
# 終極輸出導通：移除對原生屬性的依賴 (解決 SafeStreamWrapper 錯誤)
# ==========================================================
class SafeStdout:
    """模擬標準輸出流，防止底層編碼屬性檢查崩潰"""
    def write(self, s): 
        try: sys.__stdout__.write(s)
        except: pass
    def flush(self): 
        try: sys.__stdout__.flush()
        except: pass
    @property
    def encoding(self): return 'utf-8'
    def isatty(self): return False

# 強制接管 stdout
sys.stdout = SafeStdout()

# ==========================================================
# 物理路徑鎖定
# ==========================================================
ROOT_PATH = r"C:\Genesis"
if ROOT_PATH not in sys.path:
    sys.path.insert(0, ROOT_PATH)
sys.path.insert(0, os.path.join(ROOT_PATH, "Genesis_Core"))

# ==========================================================
# 核心模組匯入
# ==========================================================
try:
    from Genesis_Core.Security.Security_Bridge import PatchedAegisSentinel as AegisSentinel
    sys.stdout.write("[SUCCESS] Guardian_Bot: 核心安全橋接已導通。\n")
except ImportError as e:
    sys.stdout.write(f"[FATAL] 安全橋接匯入失敗: {e}\n")
    sys.exit(1)

class GuardianEngine:
    def __init__(self):
        try:
            self.aegis = AegisSentinel()
            sys.stdout.write("[SUCCESS] Guardian_Bot: AegisSentinel 初始化完成。\n")
        except Exception as e:
            sys.stdout.write(f"[CRITICAL] AegisSentinel 初始化異常: {e}\n")
            raise

if __name__ == "__main__":
    try:
        bot = GuardianEngine()
        sys.stdout.write("[SYSTEM] Guardian_Bot: 狀態維持正常，進入駐留模式。\n")
    except Exception as e:
        sys.stdout.write(f"[FATAL] Guardian_Bot 執行期間崩潰: {e}\n")
        sys.exit(1)