import sys


import os


import subprocess





# 強制路徑錨定，確保系統一致性


BASE_PATH = r"C:\Genesis\Genesis_Core"


sys.path.append(BASE_PATH)





# 引用模組


from Secretary_Module import Secretary


from DFMEA_Engine import DFMEAEngine  # 整合 DFMEA 閉迴路引擎





class GenesisCore:


    # 修正引號轉義問題，路徑外層用單引號，內層路徑字串正確閉合


        self.nodes = {


            "Ollama_LLM": "ollama serve",


            "Telegram_Bot": r'python C:\Genesis\SDK\Core\Telegram_Gateway.js',


            "System_Core_Monitor": r"python C:\Genesis\SDK\Modules\System_Core_Monitor_OOP.py",


            "WebMCP": r"mcp-server --config C:\Genesis\Genesis_Core\Gate\WebMCP_Genesis.py",


            "Dashboard": r"python C:\Genesis\index.html"


        } # 補上了缺少的右大括號





    def boot(self):


        print("【GenesisCore】系統啟動程序開始...")


        self.sec.write("System Boot Sequence.")





        # 1. 閉迴路健康檢查 (DFMEA)


        print("[DFMEA] 執行系統自我診斷...")


        self.dfmea.run_closed_loop()


        


        # 2. 節點啟動


        for name, cmd in self.nodes.items():


            print(f"[Loading] {name}...")


            try:


                subprocess.Popen(cmd, shell=True)


                self.sec.write(f"Node Started: {name}")


            except Exception as e:


                self.sec.write(f"Node Error: {name} - {str(e)}")





    for name, path in self.monitors.items():


            if self.secretary.verify_path(path):


                print(f"[OK] {name} 已就緒")


                self.secretary.log(f"模組 {name} 運作正常")


            else:


                print(f"[ALERT] {name} 載入失敗")   


     


        print("【GenesisCore】全節點已啟動，帝國架構就緒。")


        self.sec.write("All nodes initialized.")








class Dispatcher:


    """中央調度器：負責檔案索引與節點執行調度"""


    def __init__(self):


        self.sec = SecretaryModule()


        self.dfmea = DFMEAEngine()


        self.root_path = r"C:\Genesis" # 帝國核心範圍


        


    def dispatch_files(self, file_path_list):


        """讀取鎖定檔案清單並進行調度"""


        self.sec.log(f"調度器啟動：開始執行 {len(file_path_list)} 個鎖定節點的索引作業。")


        for file in file_path_list:


            if os.path.exists(file):


                # 此處對接執行指令 (暫不執行複雜邏輯，確保穩定性)


                print(f"[Dispatcher] 已索引鎖定檔案: {os.path.basename(file)}")


            else:


                self.sec.error_report("Dispatcher", f"節點索引遺失: {file}")





if __name__ == "__main__":


    core = GenesisCore()


    dispatcher = Dispatcher()


    print("【中央調度器】已就緒，等待主管下達檔案批次清單。")


    core.boot()