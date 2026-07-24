import os

import shutil

import time



def physical_verify():

    # 路徑定義

    base = r"C:\Genesis\Genesis_Core"

    src = os.path.join(base, "Test_File.txt")

    dest_dir = os.path.join(base, "Loop_Test_Zone")

    

    # 建立環境

    if not os.path.exists(dest_dir): os.makedirs(dest_dir)

    with open(src, "w") as f: f.write("START")

    

    # 開始物理循環測試 (3次)

    for i in range(1, 4):

        target = os.path.join(dest_dir, f"Loop_{i}.txt")

        # 執行實體移動 (模擬搬運)

        shutil.copy(src, target)

        

        # 實體寫入時間戳記 (模擬邏輯更新)

        with open(target, "a") as f:

            f.write(f"\nTIMESTAMP:{time.time()}")

            

        # 驗證物理存在

        if not os.path.exists(target):

            raise Exception(f"循環 {i} 物理寫入失敗")

        

        # 強制延遲確保硬碟 IO 寫入完成

        time.sleep(1)

        

    return True



if __name__ == "__main__":

    try:

        if physical_verify():

            print("SUCCESS: 3_LOOPS_COMPLETED")

    except Exception as e:

        print(f"FAIL: {str(e)}")