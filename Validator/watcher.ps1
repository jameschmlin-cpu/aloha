# watcher.ps1 - 修正版：加入持續運行機制
$path = "C:\Genesis\SDK\memory"
$filter = "*.txt"

Write-Host "系統監控中：正在監視 $path ..." -ForegroundColor Yellow

$watcher = New-Object System.IO.FileSystemWatcher
$watcher.Path = $path
$watcher.Filter = $filter
$watcher.IncludeSubdirectories = $false
$watcher.EnableRaisingEvents = $true

$action = {
    $filePath = $Event.SourceEventArgs.FullPath
    $fileName = $Event.SourceEventArgs.Name
    Start-Sleep -Milliseconds 500
    Write-Host "`n[自動監控] 偵測到新積木: $fileName，自動啟動核驗..." -ForegroundColor Cyan
    & "C:\Genesis\Validator\validator.ps1" -filePath $filePath -expectedHash "195CBB656C2C2D023FF78A70575E684AB32606E7CF03F1DD53600905F4F8051B"
}

Register-ObjectEvent $watcher "Created" -Action $action

# [核心修正] 強制進入迴圈，避免進程在監控器掛載後立即退出
while ($true) {
    Start-Sleep -Seconds 1
}