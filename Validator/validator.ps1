param (
    [Parameter(Mandatory=$true)][string]$filePath,
    [Parameter(Mandatory=$true)][string]$expectedHash
)

if (-not (Test-Path $filePath)) {
    Write-Host "ERROR: File not found -> $filePath" -ForegroundColor Red
    exit 1
}

$actualHash = (Get-FileHash -Path $filePath -Algorithm SHA256).Hash.ToUpper()
$expectedHash = $expectedHash.ToUpper()

if ($actualHash -eq $expectedHash) {
    Write-Host "SUCCESS: Hash matched." -ForegroundColor Green
    exit 0
} else {
    Write-Host "ERROR: Hash mismatch!" -ForegroundColor Red
    Write-Host "Expected: $expectedHash"
    Write-Host "Actual:   $actualHash"
    exit 1
}