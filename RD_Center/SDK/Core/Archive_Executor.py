# C:\Genesis\Genesis_Core\Archive_Executor.py

# 狀態：手術刀式歸檔，執行冗餘代碼移轉

import os

import shutil



def archive_redundant_files():

    archive_path = r"C:\Genesis\Genesis_Core\Archive_Deprecated"

    if not os.path.exists(archive_path):

        os.makedirs(archive_path)

    

    # 待歸檔檔案列表

    files_to_archive = [

        "DispatcherOld0608.py",

        "HermesKernel.py",

        "Artisan/SystemEngine.py"

    ]

    

    for file_name in files_to_archive:

        src = os.path.join(r"C:\Genesis\Genesis_Core", file_name)

        dst = os.path.join(archive_path, os.path.basename(file_name))

        if os.path.exists(src):

            shutil.move(src, dst)

            print(f"已歸檔: {file_name}")

    print("歸檔完成，執行路徑已清理。")



if __name__ == "__main__":

    archive_redundant_files()