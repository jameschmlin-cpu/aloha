import os
import sqlite3
from genesis_gateway import GenesisGateway

class LibraryCore:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self._initialize_table()
        self.gateway = GenesisGateway()
        
        # 定義 LibSystem 的分區映射 (Registry 映射)
        self.partitions = {
            "Logic": os.path.join(r"C:\Genesis\Library\LibOption\LibrarySystem", "Logic"),
            "Security": os.path.join(r"C:\Genesis\Library\LibOption\LibrarySystem", "Security"),
            "Registry": os.path.join(r"C:\Genesis\Library\LibOption\LibrarySystem", "Registry")
        }
        print("[System] 帝國藍圖區掛載完成，已註冊分區: Logic, Security, Registry")

    def _initialize_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Knowledge_Base 
                            (id INTEGER PRIMARY KEY, category TEXT, content TEXT, hash TEXT)''')
        self.connection.commit()

    def dispatch_module(self, partition_key, module_name):
        """
        分派員接口：負責路由至特定分區並回傳目標路徑
        """
        if partition_key not in self.partitions:
            print(f"[Dispatch Error] 未知分區: {partition_key}")
            return None
        
        target_path = os.path.join(self.partitions[partition_key], module_name)
        print(f"[Dispatch] 分派指令: 路由 [{partition_key}] -> {module_name}")
        
        # 這裡可以加入對 Gateway 的進一步呼叫，例如記錄分派行為
        self.gateway.log("history_db", f"Dispatching to {partition_key}: {module_name}")
        return target_path

    def run(self):
        print("[System] Genesis 核心引擎已就緒，等待指令...")
        # 分派範例：
        # guard_path = self.dispatch_module("Security", "Compiler_Guard.py")

if __name__ == "__main__":
    # 初始化
    from Genesis_Full_Init import run_init
    run_init()
    
    lib = LibraryCore(r"C:\Genesis\Database\Shared_Knowledge.db")
    print("Library_Main: System Ready.")
    lib.run()