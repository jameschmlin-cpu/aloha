# 強制指定 GPU 環境變數，確保 IDE 啟動時能捕捉到 RTX 3060
$env:CUDA_VISIBLE_DEVICES="0"
$env:TF_FORCE_GPU_ALLOW_GROWTH="true"

# 指定 Python 解析器為我們剛才驗證過的那條路徑
$env:PYTHONPATH="C:\Genesis\.venv_compute\Lib\site-packages"

# 啟動 Antigravity IDE
Write-Host "正在掛載算力通道至 Antigravity IDE..." -ForegroundColor Cyan
Start-Process "C:\ITE\Antigravity\Antigravity IDE\Antigravity IDE.exe"