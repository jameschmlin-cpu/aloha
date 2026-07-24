# 設定編碼以消除亂碼
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[System.Console]::InputEncoding = [System.Text.Encoding]::UTF8

# 強制指向我們剛建好的乾淨環境
$env:PATH = "C:\Genesis\.venv_compute\Scripts;" + $env:PATH

# 重新啟動監控節點
Write-Host "正在啟動修復後的監控節點..." -ForegroundColor Green
powershell.exe -ExecutionPolicy Bypass -File "C:\ITE\Antigravity\agent_node.ps1"