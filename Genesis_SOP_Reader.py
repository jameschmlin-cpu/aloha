import hashlib

def display_sop_and_verify():
    # 這是 Task 100 部署產出的實體 SOP 內容
    sop_content = """=========================================
[Genesis 系統正式維運 SOP 手冊 v1.0]
=========================================
1. 系統啟動與停止規範
   - 啟動前必須確認 C:\\Genesis\\Database 讀寫權限正常。
   - 嚴禁強制砍除 (taskkill /F) 寫入中的 SQLite 進程，必須等待 WAL 寫入完畢。

2. Node A-D 感測器處置流程
   - Node A (感測器): 若 CPU/RAM 資源超標，系統將自動觸發 Task 95 (容器資源限制)。
   - Node B (Hash 比對): 若發現核心檔案 Hash 不符，立即觸發系統熔斷，禁止寫入。
   - Node C (執行回傳): 若任務逾時超過 60 秒，自動切換至備援腳本。
   - Node D (QC 稽核): 每天凌晨 02:00 自動產出前日異常 Log 報告。

3. 資料庫保養 (Database Maintenance)
   - 每週日凌晨執行 SQLite VACUUM 釋放空間。
   - 定期監測 Genesis_Tasks.db-wal 檔案大小，若超過 50MB 需檢查連線是否未正常關閉。

4. 災難復原 (Disaster Recovery)
   - 若發生資料庫鎖定 (Database is locked) 且無法自動排除，執行 C:\\Genesis\\logs 下的還原腳本。
   - 核心模組若逃逸或損壞，依照 tasks_mapping.yaml 重新派發修復任務。
========================================="""

    # Node B Hash 實體比對
    # 確保輸出的內容 Hash 完全吻合 Task 100 部署時的紀錄
    expected_hash = "a952a79f740b4bd1314b82f39c62b96777682432ba609867b6e47f8e9467b97a"
    
    # 統一編碼轉換計算 Hash (模擬 SDK 校驗)
    actual_hash = hashlib.sha256(sop_content.encode('utf-8')).hexdigest()

    print(sop_content)
    print("\n[Node B 完整性校驗]")
    print(f"預期 Hash: {expected_hash}")
    print(f"實際 Hash: {actual_hash}")

    if actual_hash == expected_hash:
        print("-> 校驗通過：SOP 內容未受竄改，符合 SDK 4 Stages 規範。")
    else:
        print("-> 致命錯誤：SOP Hash 不符，檔案可能受損或被竄改！系統熔斷！")

if __name__ == "__main__":
    display_sop_and_verify()