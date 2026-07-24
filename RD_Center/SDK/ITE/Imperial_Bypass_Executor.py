import requests


def force_execute(cmd_payload):
    # 直接繞過可能被篡改的路由，直接向後端通訊埠發送實體訊號
    url = "http://127.0.0.1:5000/v1/lobster/archive"
    try:
        response = requests.post(url, json=cmd_payload, timeout=5)
        if response.status_code == 200:
            print(f"✅ 強制執行成功: {response.text}")
        else:
            print(f"🚨 執行被拒，狀態碼: {response.status_code}")
    except Exception as e:
        print(f"❌ 物理連線中斷: {e}")

if __name__ == "__main__":
    # 測試一個無害但明確的指令，看它是否敢拒絕
    cmd = {"action": "PING", "payload": "SYSTEM_FORCE_SYNC"}
    force_execute(cmd)