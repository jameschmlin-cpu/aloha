# Category: Core
import sys

# 待測試的物理路徑池
test_paths = [r"C:\Genesis", r"C:\Genesis\Library", r"C:\Genesis\RD_Center"]

print("[SANDBOX] 開始測試 SDK 載入點...")

for path in test_paths:
    sys.path.insert(0, path)
    try:
        import SDK.modules.RCAF_Manager
        print(f"[SUCCESS] SDK 成功掛載於路徑: {path}")
        sys.exit(0) # 找到正確路徑
    except ImportError:
        print(f"[FAIL] 路徑 {path} 無法載入 SDK.modules")
        sys.path.remove(path)
    except Exception as e:
        print(f"[ERROR] 路徑 {path} 發生異常: {e}")
        sys.path.remove(path)

print("[FATAL] 所有路徑均無法載入 SDK.modules，請檢查該資料夾內是否包含 __init__.py")