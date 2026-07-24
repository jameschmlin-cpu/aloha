@echo off
chcp 65001 >nul
:: 強制在當前視窗執行，徹底解決 NotStarted 與權限問題
powershell -ExecutionPolicy Bypass -NoProfile -File "C:\Genesis\Validator\watcher.ps1"
pause