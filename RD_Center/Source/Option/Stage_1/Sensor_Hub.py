# -*- coding: utf-8 -*-
from SDK.Base.connective_base import Connective_Base
import psutil

class Sensor_Hub(Connective_Base):
    def __init__(self):
        super().__init__() # 建立物理層連線根基

    def capture_metrics(self):
        if not self.is_node_connected():
            raise ConnectionError("Stage 1: 物理層連線阻斷")
        return {
            "cpu": psutil.cpu_percent(interval=None),
            "mem": psutil.virtual_memory().percent
        }