# Genesis 自動化同步與共同記憶層執行協議 (Protocol v2026.07.09-Final)

## 1. 任務目標
實現「雲端網頁版 Gemini」與「地端 AG 環境」之間的資訊零落差全自動同步。以 `C:\Genesis\Genesis_DFMEA.db` 為唯一共同記憶體載體，透過日誌流與資料庫交互達成自動化，禁止建立任何虛構目錄。

## 2. AG 端執行職責 (執行代碼與邏輯)
### A. 全自動監控進程 (Init: Genesis_Sync_Daemon.py)
AG 端必須在開機時啟動 `Genesis_Sync_Daemon.py`，履行以下職責：
1. **資料庫監聽**: 監控 `Genesis_DFMEA.db` 的 `System_Events` 表。一旦檢測到新指令（由雲端 Gemini 透過 API 寫入），立即執行對應之 `SDK_Bricks`。
2. **日誌對接**: 自動將 `DFMEA_Monitor.log` 的最新狀態數據寫入 `Genesis_DFMEA.db`，確保網頁端隨時可由 SQLite 讀取最新狀態。
3. **熔斷檢查**: 若兩端 Hash 檢核連續 3 次不一致，立即強制執行 `Genesis_Engineering_Standard` 之 Node D 熔斷程序。

### B. 資料交換架構 (Truth Source)
- **寫入位置**: `C:\Genesis\Genesis_DFMEA.db`
- **關鍵表單**: `Sync_Control_Table` (欄位：`instruction`, `status`, `last_hash`, `timestamp`)
- **嚴禁行為**: 禁止在 `C:\Genesis` 以外路徑建立檔案，嚴禁命名非系統現有之目錄。

## 3. 全自動執行 SOP
1. **雲端下令**: 網頁版 Gemini 產出 JSON 格式指令並送入 `Genesis_DFMEA.db` 的 `Sync_Control_Table`。
2. **本地執行**: AG 端監控進程偵測到新指令，自動解碼並調用 `Core_Gateway.py` 執行 `SDK_Bricks`。
3. **回報完成**: 任務結束後，AG 端將結果 Hash 碼與成功狀態回寫至 `Genesis_DFMEA.db` 的 `Sync_Control_Table`。
4. **狀態檢查**: 網頁端讀取 `Genesis_DFMEA.db` 狀態，確認兩端 Hash 對齊。

## 4. 階段校驗 (Node A-D)
- **Node A**: 讀取資料庫指令。
- **Node B**: 執行本地 `SDK_Bricks` 物理寫入。
- **Node C**: 回傳物理狀態代碼 (PRC) 至資料庫。
- **Node D**: 觸發狀態同步完成訊號，維持熔斷監控。

---