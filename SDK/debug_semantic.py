# C:\Genesis\SDK\debug_semantic.py
import json
path = r"C:\Genesis\SDK\block_manifest.json"
try:
    data = {"test": "success"}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)
    print(f"[Success] 檔案已強制寫入至: {path}")
except Exception as e:
    with open(r"C:\Genesis\SDK\debug_log.txt", "w") as f:
        f.write(str(e))
    print("[Fatal] 寫入失敗，錯誤已寫入 debug_log.txt")