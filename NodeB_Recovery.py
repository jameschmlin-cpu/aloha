import hashlib

def force_reset_sop():
    # 這是原始的 SOP 文字，確保字元完全一致，不包含任何編輯器自動加入的隱藏符號
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
    
    # 計算新的正確 Hash
    new_hash = hashlib.sha256(sop_content.encode('utf-8')).hexdigest()
    
    print("Node B 重置中...")
    print(f"新的基準 Hash: {new_hash}")
    
    # 將 SOP 實體寫入檔案，確保編碼統一為 utf-8
    with open(r"C:\Genesis\SOP_Manual.txt", "w", encoding="utf-8") as f:
        f.write(sop_content)
    
    print("-> 檔案已重建，Hash 已更新。請確認系統是否解除熔斷。")

if __name__ == "__main__":
    force_reset_sop()