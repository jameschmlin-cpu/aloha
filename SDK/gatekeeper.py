# -*- coding: utf-8 -*-
from nodes.node_a import NodeA_Brain
from nodes.node_b import NodeB_Executor
import time

brain = NodeA_Brain()
executor = NodeB_Executor()
print("[System] Genesis Control Loop Active.")
while True:
    executor.run_cycle()
    time.sleep(1)
