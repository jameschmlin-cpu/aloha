# C:\Genesis\SDK\nodes\node_c.py
import subprocess

class NodeC_GooseRunner:
    """本地端執行器：負責與 Goose 交互並監控程序存活"""
    def __init__(self):
        self.goose_exe = r"C:\Genesis\Bin\goose.exe"
        self.working_dir = r"C:\Genesis"

    def execute_task(self, command):
        """將指令送入 Goose 並進行實體執行"""
        # 使用 shell=True 確保指令路徑解析正確
        process = subprocess.Popen(
            [self.goose_exe, "run", command],
            cwd=self.working_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate()
        return {"returncode": process.returncode, "stdout": stdout, "stderr": stderr}