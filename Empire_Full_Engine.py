import os
import time
import datetime
import importlib.util

# 核心路徑鎖定：C:\Genesis
ROOT = r"C:\Genesis"
BRICK_LIB = os.path.join(ROOT, "Library", "SDK_Bricks")
LOG_PATH = os.path.join(ROOT, "Logs", "empire_execution.log")

def execute_brick(brick_name):
    """載入並執行積木，動態識別類別名稱，執行回饋閉環"""
    brick_path = os.path.join(BRICK_LIB, f"{brick_name}.py")
    if not os.path.exists(brick_path):
        return

    try:
        # 動態載入模組
        spec = importlib.util.spec_from_file_location(brick_name, brick_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # 動態獲取模組內定義的類別名稱，不再進行強制轉換
        classes = [c for c in dir(module) if isinstance(getattr(module, c), type)]
        if not classes:
            raise AttributeError(f"積木 {brick_name} 未定義任何 Class")
        
        # 直接調用發現的第一個類別
        brick_class = getattr(module, classes[0])
        instance = brick_class()
        instance.run()
        
        # 成功日誌
        with open(LOG_PATH, 'a', encoding='utf-8') as l:
            l.write(f"[{datetime.datetime.now()}] [執行成功] {brick_name}\n")
            
    except Exception as e:
        # 失敗回報與錯誤記錄
        with open(LOG_PATH, 'a', encoding='utf-8') as l:
            l.write(f"[{datetime.datetime.now()}] [執行失敗] {brick_name} | Error: {str(e)}\n")

def monitor_loop():
    print(f"[SYSTEM] 帝國執行回饋迴路啟動，路徑鎖定: {ROOT}")
    
    # 初始化 Logs 目錄
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    
    while True:
        # 遍歷所有已生產的積木
        for brick_file in os.listdir(BRICK_LIB):
            if not brick_file.endswith(".py"): 
                continue
            
            brick_name = brick_file.replace('.py', '')
            print(f"[{datetime.datetime.now()}] [監控中] 執行積木: {brick_name}")
            
            # 執行回饋迴路
            execute_brick(brick_name)
            
        # 每小時執行一次全量閉環
        time.sleep(3600)

if __name__ == "__main__":
    monitor_loop()