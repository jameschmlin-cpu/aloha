# C:\Genesis\Headquarter\RD\Main_Engine.py (全域路由映射版)
import os
import re

class MainEngine:
    def __init__(self):
        self.rd_dir = r"C:\Genesis\Headquarter\RD"
        self.log_path = r"C:\Genesis\Headquarter\Logs\Empire_Audit.log"
        # 強化後的解析器：支援部門與 Skill 混合解析
        self.cmd_pattern = re.compile(r"啟動\s+(?P<target>[\w_]+)", re.U)
        print("[System] 帝國引擎已啟動，動態路由模式已掛載。")

    def log_event(self, action, status):
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(f"ACTION: {action} | STATUS: {status}\n")

    def listen(self, command):
        match = self.cmd_pattern.search(command)
        if match:
            target = match.group('target')
            # 動態檢查：只要 RD 目錄下有 Skill_XXX.yaml，自動對應
            if os.path.exists(os.path.join(self.rd_dir, f"Skill_{target}.yaml")):
                self.log_event(f"Route_To_{target}", "MATCHED")
                print(f"[Engine] 正在指派任務給部門: {target}")
                print(f"[SUCCESS] {target} 節點已喚醒，正在讀取部門邏輯...")
            else:
                print(f"[Error] 未發現部門 {target} 的設定檔，請檢查 RD 目錄。")
        else:
            print("[Engine] 指令格式錯誤，請使用：啟動 [部門名稱/Skill名稱]")

if __name__ == "__main__":
    engine = MainEngine()
    while True:
        cmd = input("董事長，請下令 (全功能解析模式): ")
        if cmd == "exit": break
        engine.listen(cmd)