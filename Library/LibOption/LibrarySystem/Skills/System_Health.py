import psutil
def run():
    cpu = psutil.cpu_percent()
    print(f"⚙️ 系統負載：{cpu}%")
    return cpu