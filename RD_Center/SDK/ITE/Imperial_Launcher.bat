@echo off
chcp 65001 >nul
title Hermes_Empire_Commander_Final
cd /d C:\ITE\Genesis_Core

echo [帝國戰情室啟動] 正在連線核心架構...
echo ------------------------------------------

:: 1. 環境自我診斷 (Fail-Fast)
echo [診斷] 檢查 System_Memory.json...
if not exist "Data\System_Memory.json" (
    echo [修復] 偵測到遺失，正在自動重構...
    if not exist "Data" mkdir Data
    echo {"status": "AUTO_RECOVERED", "ts": "%date% %time%"} > Data\System_Memory.json
)

:: 2. 影子程式免疫 (預先掃除)
echo [安全] 清除潛在影子埋伏...
taskkill /f /im shadow_exec.exe >nul 2>&1

:: 3. 核心點火 (保留監控視窗以供除錯)
echo [點火] 啟動 Kernel_Orchestrator...
echo [注意] 此視窗為監控戰情室，請勿關閉，否則將失去即時監控能力。
start "Kernel_War_Room" cmd /K "python Kernel_Orchestrator.py"

echo ------------------------------------------
echo [SUCCESS] 指揮官已就位，系統閉環監控中。
:: 不使用 exit，確保視窗留在桌面供您隨時核對