@echo off
chcp 65001 >nul
title Genesis System One-Click Bootstrapper
echo ========================================================
echo 🛸 [Stored Procedure] Booting Genesis Four-in-One System...
echo ========================================================
powershell.exe -ExecutionPolicy Bypass -File C:\Genesis\Genesis_Stored_Procedure.ps1
if %ERRORLEVEL% neq 0 (
    echo.
    echo 🔴 [FAIL] Genesis System startup failed with exit code %ERRORLEVEL%.
    pause
)
