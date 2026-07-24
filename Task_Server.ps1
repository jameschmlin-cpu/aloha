$TaskFile = 'C:\Genesis\task_queue.txt'
Write-Host '任務監控中... (等待指令)' -ForegroundColor Cyan
while($true) {
    if (Test-Path $TaskFile) {
        $cmd = Get-Content $TaskFile -Raw
        if (![string]::IsNullOrWhiteSpace($cmd)) {
            Write-Host '執行任務中...' -ForegroundColor Yellow
            Invoke-Expression $cmd
            Set-Content -Path $TaskFile -Value ''
            Write-Host '任務完成。' -ForegroundColor Green
        }
    }
    Start-Sleep -Seconds 1
}
