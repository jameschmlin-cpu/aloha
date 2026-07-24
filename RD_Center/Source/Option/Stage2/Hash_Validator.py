# -*- coding: utf-8 -*-
from Stage1.Sensor_Hub import Sensor_Hub
from SDK.Base.secure_connectivity import SecureConnectivityOP
import hashlib

class Hash_Validator(SecureConnectivityOP):
    def __init__(self):
        super().__init__() # 建立安全封裝層
        self.sensor = Sensor_Hub() # 依賴注入 S1 物理狀態

    def validate(self, file_path):
        # 實體邏輯：確保 S1 狀態正常後執行 Hash 比對
        if not self.sensor.is_node_connected():
            return False
        sha = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha.update(chunk)
        return sha.hexdigest()