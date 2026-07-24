# QC Agents 實務檢核標準與熔斷機制清單

## 1. 任務啟動前檢核 (Pre-Execution Check)
在執行任何程式碼生成前，Gem 必須完成以下自我審查：
- [ ] 路徑確認：強制確認路徑變數已指派為 `C:\Genesis`。憲法("C:\Genesis\Management_Hub\project_constitution.md")
- [ ] 節點狀態：檢測 Node A (輸入)、Node B (解析)、Node C (校驗)、Node D (輸出) 是否連線正常。
- [ ] 歷史比對：核對該任務是否與過往失敗紀錄（Root Cause）衝突。

## 2. SDK 4 Stages 強制流程
- 階段一 (Design)：產出架構設計圖與路徑路徑檢查碼。
- 階段二 (Execution)：進行 Token 噴發預估，確保不會產生冗餘程式碼。
- 階段三 (Sandbox)：模擬執行，產出實體 Hash。
- 階段四 (Commit)：等待 Node C 返回執行代碼，若無代碼嚴禁輸出完成訊息。

## 3. 熔斷觸發條件 (Breaker Trip Conditions)
符合以下任一條件，Gem 必須立即中止：
- 檢測到非 `C:\Genesis` 之外的寫入請求。
- 實體 Hash 與校驗值不符。
- 任何形式的「pass」或「TODO」空殼代碼被嘗試產出。
- 使用者指令要求繞過 QC 檢查。
- 違反憲法("C:\Genesis\Management_Hub\project_constitution.md")

## 4. 異常處理與回報
一旦熔斷：
- 禁止任何進一步的代碼寫入。
- 必須產出包含 `[FAILED]` 標籤的 Root Cause 分析報告。
- 報告內容需包含：錯誤節點位置、違規路徑、以及建議的修正方案。