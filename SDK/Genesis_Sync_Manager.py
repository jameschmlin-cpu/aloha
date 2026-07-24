import requests
import hashlib
import os

class Genesis_Sync_Manager:
    def __init__(self):
        self.root = r"C:\Genesis\SDK\Vendors"
        self.manifest_url = "https://cloud.genesis.logic/sync/manifest.json"

    def execute_sync(self):
        # 1. 抓取清單與 Hash
        resp = requests.get(self.manifest_url).json()
        for vendor in resp['vendors']:
            path = os.path.join(self.root, f"{vendor['name']}.py")
            # 2. 實體寫入與 Hash 比對
            data = requests.get(vendor['url']).content
            if hashlib.sha256(data).hexdigest() == vendor['sha256']:
                with open(path, 'wb') as f: f.write(data)
                print(f"【部署成功】{vendor['name']} 已實體更新")
            else:
                raise RuntimeError(f"【熔斷】{vendor['name']} Hash 驗證失敗")

if __name__ == "__main__":
    Genesis_Sync_Manager().execute_sync()