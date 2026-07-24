$watcher = New-Object System.IO.FileSystemWatcher
$watcher.Path = "C:\Genesis\SDK\memory"
$watcher.Filter = "*.txt"
$watcher.IncludeSubdirectories = $false
$watcher.EnableRaisingEvents = $true

$action = {
    $path = $Event.SourceEventArgs.FullPath
    $name = $Event.SourceEventArgs.Name
    Write-Host "偵測到新積木生成: $name，正在自動進行 Hash 核驗..." -ForegroundColor Cyan
    
    # 自動調用您剛剛寫好的驗證器
    & "C:\Genesis\Validator\validator.ps1" -filePath $path -expectedHash "您的目標Hash值"
}

Register-ObjectEvent $watcher "Created" -Action $action