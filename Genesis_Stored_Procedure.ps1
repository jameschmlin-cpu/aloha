# C:\Genesis\Genesis_Stored_Procedure.ps1
# ==============================================================================
# Genesis One-Click Stored Procedure Bootstrapper
# ==============================================================================

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "🛸 [Stored Procedure] Booting Genesis Four-in-One System..." -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan

# Step 1: Run AST Scanner & RAG Grounding Align
Write-Host "`n[Step 1/5] 🔍 Rebuilding SDK API Specifications Reference..." -ForegroundColor Yellow
python C:\Genesis\RD_Center\SDK\System\Generate_API_Specs.py
if ($LASTEXITCODE -ne 0) {
    Write-Error "[-] API Specifications generation failed."
    exit 1
}
Write-Host "[SUCCESS] sdk_api_reference.md regenerated and synced." -ForegroundColor Green

# Step 2: Validate Development Execution Mode
Write-Host "`n[Step 2/5] ⚙️ Aligning Local Developer Mode settings..." -ForegroundColor Yellow
$cfgPath = "C:\Genesis\Config\telegram_config.json"
if (Test-Path $cfgPath) {
    $cfg = Get-Content $cfgPath | ConvertFrom-Json
    $devMode = $cfg.development_mode
    Write-Host "[INFO] Current Development Mode is set to: $devMode" -ForegroundColor White
    if ($devMode -eq "LOCAL") {
        Write-Host "[SUCCESS] Developer Mode locked to LOCAL. Ground RTX 3060 compute engaged." -ForegroundColor Green
    } else {
        Write-Warning "[WARN] Development Mode is HYBRID. High frequency API consumption warning."
    }
} else {
    Write-Warning "[WARN] Config file missing. Defaulting to HYBRID mode."
}

# Step 3: Stop residual active processes
Write-Host "`n[Step 3/5] 🧹 Stopping residual background Genesis processes..." -ForegroundColor Yellow
$pids = Get-CimInstance Win32_Process | Where-Object {
    $_.CommandLine -like '*C:\Genesis*' -and $_.CommandLine -notlike '*Genesis_Stored_Procedure*' -and $_.ProcessId -ne $PID
} | Select-Object -ExpandProperty ProcessId

if ($pids) {
    Write-Host "[INFO] Terminating active PIDs: ($($pids -join ', '))" -ForegroundColor Gray
    Stop-Process -Id $pids -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
}
Write-Host "[SUCCESS] Process registers and memory buffers cleared." -ForegroundColor Green

# Step 4: Load Startup Manager V4 in the background
Write-Host "`n[Step 4/5] 🚀 Loading Startup Manager V4 Daemon..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList '-NoProfile -Command "python C:\Genesis\Startup_Manager_V4.py"' -WindowStyle Minimized
Write-Host "[INFO] Background daemon launched. Syncing heartbeats (10 seconds)..." -ForegroundColor Gray
Start-Sleep -Seconds 10

# Step 5: Perform health check via local status API
Write-Host "`n[Step 5/5] 🩺 Querying Local AI Cognitive Brain status..." -ForegroundColor Yellow
try {
    $body = @{ message = "/status" } | ConvertTo-Json
    $res = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/chat" -Method Post -Body $body -ContentType "application/json; charset=utf-8"
    Write-Host "`n------------------- [SYSTEM READY REPORT] -------------------" -ForegroundColor Green
    Write-Host $res.response -ForegroundColor Green
    Write-Host "-------------------------------------------------------------" -ForegroundColor Green
} catch {
    Write-Error "[-] Health check connection failed. Check Startup_Manager_V4.py logs."
}

# Final step: Launch the Interactive Main Engine Console
Write-Host "`n========================================================" -ForegroundColor Cyan
Write-Host "👑 System Ready! Launching Main Engine Console..." -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
python C:\Genesis\Headquarter\RD\Main_Engine.py
