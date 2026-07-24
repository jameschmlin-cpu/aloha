# Node_A_Monitor: 僅檢查路徑是否存在，絕不進行任何寫入
$path = "C:\ITE"
if (Test-Path $path) {
    Write-Host "Node_A_Success: 路徑 $path 存取正常" -ForegroundColor Green
} else {
    Write-Host "Node_A_Fail: 路徑不存在" -ForegroundColor Red
}

# Node_B_Validator: 檢查核心資料庫是否存在
$dbPath = "C:\ITE\Genesis_Core\Data\Memory_Core.db"
if (Test-Path $dbPath) {
    Write-Host "Node_B_Success: 資料庫已找到" -ForegroundColor Green
} else {
    Write-Host "Node_B_Fail: 資料庫遺失" -ForegroundColor Red
}