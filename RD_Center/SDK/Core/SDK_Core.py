# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\RD_Center\SDK\Core\SDK_Core.py
# 狀態：SDK_Core 核心模組 - 包含 Dashboard_Update_Hook 串聯

import urllib.request
import json
import time

def Dashboard_Update_Hook(brick_name, status, details=""):
    """
    每個積木執行後自動觸發 HTTP POST，將資料同步寫入儀表板。
    """
    url = "http://127.0.0.1:8080/api/dashboard-hook"
    payload = {
        "brick_name": brick_name,
        "status": status,
        "details": details,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        # Timeout configured to prevent blocking brick execution if server is offline
        with urllib.request.urlopen(req, timeout=2.0) as res:
            return True
    except Exception as e:
        print(f"[SDK_Core Hook Warning] Failed to push execution update: {e}")
        return False
