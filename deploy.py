import os
import struct

# 實體路徑鎖定
path = r"C:\Genesis\system_core.bin"

# 二進位數據區塊 (四合一架構初始化)
data = struct.pack('Q', 0xDEADBEEFCAFE1234) # Cortex+Loop+SDK+Gemini 核心 ID

# 強制寫入物理磁區
with open(path, 'wb') as f:
    f.write(data)
    f.flush()
    os.fsync(f.fileno())

print(f"System Core Binary Written to {path}")