param (
    [Parameter(Mandatory=$true)][string]$filePath,
    [Parameter(Mandatory=$true)][string]$content,
    [Parameter(Mandatory=$true)][string]$expectedHash
)

# 使用精確寫入模式，不增加任何換行與特殊字元
[System.IO.File]::WriteAllText($filePath, $content)

Write-Host "執行自動化核驗..." -ForegroundColor Cyan

# 調用驗證器
& "C:\Genesis\Validator\validator.ps1" -filePath $filePath -expectedHash $expectedHash

if ($LASTEXITCODE -eq 0) {
    Write-Host "自動化放行成功：積木已安全整合。" -ForegroundColor Green
} else {
    Write-Host "自動化封鎖：積木 Hash 錯誤，檔案已移除。" -ForegroundColor Red
    Remove-Item -Path $filePath -Force
}