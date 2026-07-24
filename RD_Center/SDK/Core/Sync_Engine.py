import shutil
import os

def sync():

    src = r'C:\Genesis\Genesis_Core\Vault\DFMEA_Rules.db'

    dst = r'C:\Genesis\Library\LibrarySystem\Shared_Knowledge.db'

    if os.path.exists(src): shutil.copy2(src, dst)