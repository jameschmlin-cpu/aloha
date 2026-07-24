# setup_tunnel.ps1
# C:\Genesis\setup_tunnel.ps1
# Automated Cloudflare Tunnel downloader and setup instructions for ezai.idv.tw

$ProgressPreference = 'SilentlyContinue'
$GenesisBase = "C:\Genesis"
$BinDir = "$GenesisBase\Bin"
$CloudflaredPath = "$BinDir\cloudflared.exe"

# 1. Ensure Bin directory exists
if (-not (Test-Path $BinDir)) {
    New-Item -ItemType Directory -Path $BinDir | Out-Null
}

# 2. Download portable cloudflared.exe
if (-not (Test-Path $CloudflaredPath)) {
    Write-Host "[1/3] Downloading Cloudflare Tunnel client..." -ForegroundColor Yellow
    $Uri = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
    try {
        Invoke-WebRequest -Uri $Uri -OutFile $CloudflaredPath -TimeoutSec 90
        Write-Host "[SUCCESS] cloudflared.exe downloaded to $CloudflaredPath" -ForegroundColor Green
    } catch {
        Write-Error "Download failed: $_"
        exit 1
    }
} else {
    Write-Host "[1/3] cloudflared.exe already exists, skipping download." -ForegroundColor Green
}

# 3. Print setup instructions
Write-Host ""
Write-Host "==========================================================" -ForegroundColor Yellow
Write-Host "       Cloudflare Tunnel (Genesis + Node-RED) Setup" -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Yellow
Write-Host "Follow these steps to securely expose both services:" -ForegroundColor White
Write-Host ""
Write-Host "Step 1: Perform interactive login authentication" -ForegroundColor Cyan
Write-Host "   C:\Genesis\Bin\cloudflared.exe tunnel login" -ForegroundColor Yellow
Write-Host ""
Write-Host "Step 2: Create tunnel" -ForegroundColor Cyan
Write-Host "   C:\Genesis\Bin\cloudflared.exe tunnel create genesis-tunnel" -ForegroundColor Yellow
Write-Host "   (This generates a JSON credentials file in C:\Users\user\.cloudflared\)" -ForegroundColor Gray
Write-Host ""
Write-Host "Step 3: Configure DNS Routes for both Genesis & Node-RED" -ForegroundColor Cyan
Write-Host "   C:\Genesis\Bin\cloudflared.exe tunnel route dns genesis-tunnel genesis.ezai.idv.tw" -ForegroundColor Yellow
Write-Host "   C:\Genesis\Bin\cloudflared.exe tunnel route dns genesis-tunnel nodered.ezai.idv.tw" -ForegroundColor Yellow
Write-Host ""
Write-Host "Step 4: Create a configuration file at C:\Genesis\Bin\config.yml:" -ForegroundColor Cyan
Write-Host "   tunnel: <your-tunnel-uuid>" -ForegroundColor Gray
Write-Host "   credentials-file: C:\Users\user\.cloudflared\<your-tunnel-uuid>.json" -ForegroundColor Gray
Write-Host "   ingress:" -ForegroundColor Gray
Write-Host "     - hostname: genesis.ezai.idv.tw" -ForegroundColor Gray
Write-Host "       service: http://localhost:8000" -ForegroundColor Gray
Write-Host "     - hostname: nodered.ezai.idv.tw" -ForegroundColor Gray
Write-Host "       service: http://localhost:1880" -ForegroundColor Gray
Write-Host "     - service: http_status:404" -ForegroundColor Gray
Write-Host ""
Write-Host "Step 5: Run the tunnel using the configuration file" -ForegroundColor Cyan
Write-Host "   C:\Genesis\Bin\cloudflared.exe -config C:\Genesis\Bin\config.yml run genesis-tunnel" -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Yellow
Write-Host "Once active, access your panels at:" -ForegroundColor White
Write-Host " - Genesis Dashboard: https://genesis.ezai.idv.tw" -ForegroundColor Green
Write-Host " - Node-RED Control:  https://nodered.ezai.idv.tw" -ForegroundColor Green
Write-Host ""
