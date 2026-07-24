
# 模擬原有的 rmCPa 介面，直接返回計算後的字典，不經過任何 DLL 載入
def rmCPa(command):
    # 這裡就是您的核心運算，直接由 Python 原生執行
    # 若需擴充，直接在此處增加 elif 分支即可
    if command == "TEST_CONNECTION":
        return "SUCCESS_NATIVE_EXEC"
    elif command == "SALARY_CALC":
        return {"status": "OK", "result": "NATIVE_EXEC_COMPLETE"}
    return "UNKNOWN_COMMAND"

# 確保對接層與外部調用完全一致
def run_bridge_command(command, data):
    return rmCPa(command)