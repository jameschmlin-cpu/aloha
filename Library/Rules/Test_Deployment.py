# -*- coding: utf-8 -*-
# 檔案位置: C:\Genesis\Library\Rules\Test_Deployment.py
# 已重構：此檔案為重定向包裝器，將實際執行導向 SDK_Bricks 積木
import sys
import subprocess
import os

GENESIS_BASE = r"C:\Genesis"
brick_path = os.path.join(GENESIS_BASE, "RD_Center", "SDK_Bricks", "Logic", "Test_Deployment.py")

if __name__ == "__main__":
    if os.path.exists(brick_path):
        print(f"[重定向] 正在引導執行至積木位置: {brick_path}\n")
        # 繼承目前的 Python 直譯器環境來執行積木
        proc = subprocess.run([sys.executable, brick_path], capture_output=False)
        sys.exit(proc.returncode)
    else:
        print(f"[錯誤] 找不到實體積木: {brick_path}")
        sys.exit(1)