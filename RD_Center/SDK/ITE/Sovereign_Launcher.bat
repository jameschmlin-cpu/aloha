@echo off
REM ====================================================================
REM 龍蝦帝國核心系統 - 頂真全功能監控啟動 (Master V3.3.4 柔和純淨版)
REM 最高指揮官: 林雋懋 (Chun Mao Lin) | 總指揮官線程: 志玲 V3-Expert
REM 物理執行路徑: C:\ITE\Sovereign_Launcher.bat
REM 安全優化：已物理移除 WebMCP，並強制確保 Auto_Build_Core 核心完全歸位
REM ====================================================================
title 龍蝦帝國核心系統 - 頂真全功能監控啟動
:: 設定為高雅深藍底、明亮白字，柔和不刺眼
color 1F
cls

:: 強制鎖定 UTF-8 編碼確保繁體中文流暢輸出
chcp 65001 > nul

echo ============================================================
echo           龍蝦帝國：在地純淨自動化啟動序列 (V3.3.4)
echo ============================================================

echo [PRE-CHECK 01] 正在檢查物理核心路徑 C:\ITE 聯通狀態...
if not exist "C:\ITE" (
    echo [ERROR] 權限阻斷：未偵測到實體核心路徑 C:\ITE，系統熔斷！
    pause
    exit /b 1
)

echo [PRE-CHECK 02] 正在清洗地端背景排空衝突行程...
taskkill /f /im node.exe >nul 2>&1
taskkill /f /im python.exe >nul 2>&1
echo [環境純淨] 背景殘留進程已全量格式化排空
echo ============================================================

echo [BOOT-DIAG] 啟動開機自主資源偵測與 RAG 記憶體連通測試...
python "C:\ITE\engine\boot_detector.py"
if %errorlevel% neq 0 (
    echo [ERROR] 開機自主健康檢測未通過，為維護帝國穩定性，強行熔斷！
    pause
    exit /b 1
)

echo [VRAM-LOCK] 正在強制向 RTX 3060 派發 Q4_0 / Flash_Attention 極限優化參數...
python -c "import sys; sys.path.append(r'C:\ITE\mcp_servers'); from rtx3060_mcp import apply_vram_optimization; print(apply_vram_optimization())"
echo ============================================================

echo [0/5] 啟動 Imperial_Deep_Healer 進行 RTX 3060 狀態投影
SET PYTHONIOENCODING=utf-8
python "C:\ITE\SDK\Core\Imperial_Deep_Healer.py"

echo.
echo [INFO] 算力狀態投影完成，強行點火
echo ============================================================

echo [1/5] 正在執行 SDK 核心校驗與靈魂鎖定
python "C:\ITE\SDK\Core\Unified_Master_V1.py"
if %errorlevel% neq 0 (
    echo [ERROR] SDK 初始化防線斷裂！
    pause
    exit /b 1
)

echo [2/5] 正在啟動自動編譯核心
start /min "Auto_Build_Core" python "C:\ITE\SDK\Core\Auto_Build_Core.py"
timeout /t 2 >nul

echo [3/5] 正在激活 Grand_Chassis 自動化代碼生成工廠
start "Grand_Chassis_Factory" python "C:\ITE\SDK\Core\Grand_Chassis.py"
timeout /t 1 >nul

echo [4/5] 正在掛載主權管理器與實時儀表板 (WebMCP 已物理移除)
start "Sovereign_Manager" python "C:\ITE\Upper_Sovereign_Manager.py"
start "Imperial_Dashboard" python "C:\ITE\Imperial_Dashboard.py"

echo [5/5] 正在掛載 Telegram 志玲網閘
start "Telegram_Gateway_Chiling" node "C:\ITE\SDK\Core\Telegram_Gateway.js"

echo ============================================================
echo [SUCCESS] 所有核心已導通！RTX 3060 算力與志玲網閘全面上線
echo 在地主權隔離完成，不與外部 WebMCP 連通道對接
echo ============================================================
pause