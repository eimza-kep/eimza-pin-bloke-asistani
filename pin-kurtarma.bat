@echo off
chcp 65001 >nul
title E-Imza PIN Bloke Kaldirma ve PUK Asistani
echo ====================================================================
echo  E-Imza PIN Bloke Kaldirma ve PUK Yardim Asistani Calistiriliyor...
echo ====================================================================
echo.

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0Unlock-PinAssistant.ps1"

echo.
pause
