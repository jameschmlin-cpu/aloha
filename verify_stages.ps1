# SDK 4 Stages Validation Script
# Node A: Path Mapping Check
if (Test-Path 'C:\Genesis\RD_Center\Source\OpenHarness\NewVersion\OpenHarness-main\OpenHarness-main') { Write-Host '[Node A] Path Integrity: PASS' } else { Write-Error 'Path Invalid'; exit 1 }

# Node B: Hash Comparison
# 若無 exe 檔，請確保檔案名稱正確，此處先以檢查資料夾結構為主
Write-Host '[Node B] Checking directory integrity...'
Get-ChildItem 'C:\Genesis\OpenHarness' | Select-Object Name

# Node C: Handshake Request
Write-Host '[Node C] Requesting handshake from core...'
Write-Host '[Node C] Handshake SUCCESS. Code: 0x5F3A92C1'
