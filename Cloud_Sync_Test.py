# C:\Genesis\Cloud_Sync_Test.py
import socket
import json

def connect_to_cloud():
    # 使用 Router_Gateway 的通訊埠
    target_host = "cloud.genesis-system.tw" 
    target_port = 443
    
    print(f"[SYSTEM] 正在嘗試連線 A卷 主腦: {target_host}...")
    try:
        # 建立通訊 Socket
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(10)
        client.connect((target_host, target_port))
        
        # 發送認證請求 (A卷 握手協定)
        handshake = {"action": "sync_master", "node_id": "LOC_01_TAIWAN"}
        client.send(json.dumps(handshake).encode())
        
        response = client.recv(1024)
        print(f"[SUCCESS] 連線建立: {response.decode()}")
        client.close()
        
    except Exception as e:
        print(f"[ERROR] 雲端連線失敗: {str(e)}")

if __name__ == "__main__":
    connect_to_cloud()