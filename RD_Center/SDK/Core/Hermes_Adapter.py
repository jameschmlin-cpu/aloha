# 檔案：C:\Genesis\Genesis_Core\Hermes_Adapter.py

import subprocess




class HermesAdapter:

    """單純的橋接器，呼叫舊有 WebMCP 進行測試，不更動原始碼"""

    def __init__(self):

        self.target_script = r"C:\Genesis\Genesis_Core\Gate\WebMCP_Genesis.py"



    def execute_self_test(self):

        print(f"[Adapter] 正在呼叫舊程式進行自動測試: {self.target_script}")

        try:

            # 呼叫舊程式執行診斷，保留其完整性

            result = subprocess.run(["python", self.target_script, "--test"], capture_output=True, text=True)

            if result.returncode == 0:

                print("[Adapter] 🟢 測試通過")

                return True

            else:

                print(f"[Adapter] 🔴 測試失敗: {result.stderr}")

                return False

        except Exception as e:

            print(f"[Adapter] 執行錯誤: {e}")

            return False