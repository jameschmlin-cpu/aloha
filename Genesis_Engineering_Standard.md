# Genesis 工程規範與節點校驗協議 (Protocol v2026.07.09)

## 1. 核心路徑規範
* **Root Directory**: `C:\Genesis`
* 所有物理寫入操作必須強制導向此路徑，嚴禁任何逃逸行為。

## 2. SDK 4 Stages 自動化流程
所有程式碼異動必須通過以下四個階段：
1.  **Stage 1 (Definition)**: 分析需求，明確定義寫入邊界與目標模組。
2.  **Stage 2 (Validation)**: 進行路徑合法性檢查、Token 噴發量預估與沙盒環境模擬。
3.  **Stage 3 (Execution)**: 產出程式碼與對應的實體 Hash 碼。
4.  **Stage 4 (Inheritance)**: 完成代碼測試覆蓋並進行繼承檢查，確保與舊有系統相容。

## 3. Node A-D 全節點校驗機制
在執行物理寫入前，必須經過全節點校驗：
* **Node A (Input)**: 接收指令，並與 Hash 比對基準進行核對。
* **Node B (Processing)**: 監控代碼寫入軌跡，確保無未經授權的偏移。
* **Node C (Verification)**: 進入最終節點校驗，必須獲得「實體回傳代碼 (Physical Response Code)」方可通過。
* **Node D (Finalization)**: 物理寫入執行，啟動系統熔斷監控節點。若偵測到數據不符，立即執行熔斷並回報。

## 4. 品質與作業要求
* **專業用語**: 嚴禁使用外國翻譯腔。所有用語必須符合台灣本土開發者習慣，要求簡潔、精準、頂真。
* **實體 Hash**: 任何異動必須附帶實體 Hash。無 Hash 者視為無效異動。
* **權限與主管責任**: Gemini 僅為執行端，最終決策權歸屬於主管。未獲得 Node C 回傳代碼前，不得回報作業成功。