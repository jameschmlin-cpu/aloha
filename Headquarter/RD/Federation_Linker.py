# C:\Genesis\Headquarter\RD\Federation_Linker.py
import os

def link_legion():
    rd_dir = r"C:\Genesis\Headquarter\RD"
    skills = [f for f in os.listdir(rd_dir) if f.startswith("Skill_") and f.endswith(".py")]
    
    # 為每個 Skill 注入「通訊接口」
    for skill in skills:
        with open(os.path.join(rd_dir, skill), "a", encoding="utf-8") as f:
            f.write("\n\ndef emit_event(event_name, data):\n    print(f'[Bus] 發送事件: {event_name} | 數據: {data}')")
    
    print(f"[SUCCESS] 軍團互聯協議已部署至 {len(skills)} 個單位，原子交互模式已激活。")

if __name__ == "__main__":
    link_legion()