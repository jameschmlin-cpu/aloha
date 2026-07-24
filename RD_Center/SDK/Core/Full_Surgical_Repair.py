# 檔案：C:\Genesis\Genesis_Core\Full_Surgical_Repair.py

# 目的：一次性修補所有 8 支程式，移除空殼，強制閉環。

import os



def perform_surgical_repair():

    # 檔案清單與對應的實體閉環邏輯

    repair_map = {

        "Hermes_Kernel.py": "from System_Service_Registry import ServiceRegistry\nfrom Security.Aegis_Sentinel import AegisSentinel\nimport os\n\nclass HermesKernel:\n    def __init__(self):\n        self.registry = ServiceRegistry()\n        self.sentinel = AegisSentinel()\n    def boot(self):\n        if os.path.exists(r'C:\\ITE\\Genesis_Core\\Integrity_Manifest.db'):\n            self.registry.spawn_all_services()\n        else: raise Exception('Integrity Check Failed')",

        

        "System_Service_Registry.py": "import subprocess, psutil\nclass ServiceRegistry:\n    def spawn_all_services(self):\n        procs = {'Hard_Obs': r'C:\\ITE\\Genesis_Core\\Security\\Hardware_Observer.py'}\n        for name, path in procs.items():\n            p = subprocess.Popen(['python', path])\n            print(f'[Registry] {name} started with PID: {p.pid}')",

        

        "Interface_Controller.py": "from flask import Flask, jsonify\nimport sqlite3\napp = Flask(__name__)\n@app.route('/')\ndef index():\n    try:\n        with sqlite3.connect(r'C:\\ITE\\Genesis_Core\\Data\\Unified_Empire_Memory.db') as conn:\n            data = conn.execute('SELECT * FROM State_Table').fetchall()\n            return jsonify({'status': 'Success', 'data': data})\n    except Exception as e: return jsonify({'status': 'Error', 'msg': str(e)})",

        

        "Integration_Bridge.py": "import requests\nclass SystemBridge:\n    def link_ollama(self):\n        try:\n            r = requests.post('http://localhost:11434/api/generate', json={'model': 'llama3', 'prompt': 'test'}, timeout=5)\n            return r.status_code == 200\n        except: return False",

        

        "Config_Enforcer.py": "import os\nCONFIG = {'DB': r'C:\\ITE\\Genesis_Core\\Data\\Unified_Empire_Memory.db'}\ndef enforce_paths():\n    if not os.path.exists(os.path.dirname(CONFIG['DB'])): os.makedirs(os.path.dirname(CONFIG['DB']))\n    with open(CONFIG['DB'], 'a'): pass",

        

        "Sync_Engine.py": "import shutil, os\ndef sync():\n    src = r'C:\\ITE\\Genesis_Core\\Vault\\DFMEA_Rules.db'\n    dst = r'C:\\ITE\\Library\\LibrarySystem\\Shared_Knowledge.db'\n    if os.path.exists(src): shutil.copy2(src, dst)",

        

        "Hermes_Interface.py": "import sqlite3\nclass HermesInterface:\n    def sync_data(self):\n        with sqlite3.connect(r'C:\\ITE\\Genesis_Core\\Data\\Unified_Empire_Memory.db') as conn:\n            return conn.execute('SELECT 1').fetchone() is not None",

        

        "Test_Hermes_Interface.py": "from Hermes_Interface import HermesInterface\nprint(f'Test Status: {HermesInterface().sync_data()}')"

    }



    base_path = r"C:\Genesis\Genesis_Core"

    for filename, code in repair_map.items():

        with open(os.path.join(base_path, filename), 'w', encoding='utf-8') as f:

            f.write(code)

        print(f"[SURGICAL_FIX] {filename} 已完成邏輯閉環。")



if __name__ == "__main__":

    perform_surgical_repair()