# C:\Genesis\Headquarter\RD\Update_Supervisor_Status.py
import sys
import json
import os

def update_status(status="熱烈辦公中", room_id="document"):
    path = r"C:\Users\user\.openclaw\subagents\focus-supervisor.json"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = {
        "resourceId": room_id,
        "detail": status,
        "label": "林雋懋主管"
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[STATUS] 主管狀態更新：於房間 {room_id} -> {status}")

if __name__ == "__main__":
    status = sys.argv[1] if len(sys.argv) > 1 else "熱烈辦公中"
    room_id = sys.argv[2] if len(sys.argv) > 2 else "document"
    update_status(status, room_id)
