# C:\Genesis\SDK\fix_gatekeeper.py
# -*- coding: utf-8 -*-

code = """# -*- coding: utf-8 -*-
from nodes.node_a import NodeA_Brain
from nodes.node_b import NodeB_Executor
import time

brain = NodeA_Brain()
executor = NodeB_Executor()
print("[System] Genesis Control Loop Active.")
while True:
    executor.run_cycle()
    time.sleep(1)
"""

with open(r"C:\Genesis\SDK\gatekeeper.py", "w", encoding="utf-8") as f:
    f.write(code)

print("[SUCCESS] Gatekeeper 編碼已強制重置為 UTF-8，請重新執行。")