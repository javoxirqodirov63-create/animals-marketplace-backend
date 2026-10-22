@echo off
chcp 65001 > nul
title Universal Hayvonlar Bozori (Animals-uz)
echo ========================================================
echo   Universal Hayvonlar Bozori - Barcha Tizimlar
echo ========================================================
echo.
echo 1. FastAPI Backend server ishga tushmoqda (http://127.0.0.1:8000)...
start "Animals Backend API" cmd /k "cd /d "%~dp0backend" && python run.py"

timeout /t 3 /nobreak > nul

echo 2. Flutter Mobil Ilovasi ishga tushmoqda (http://localhost:7777)...
start "Animals Flutter App" cmd /k "cd /d "%~dp0..\Animals" && C:\src\flutter\bin\flutter.bat run -d chrome --web-port 7777"

echo.
echo Barchasi tayyor! 
echo - Admin Boshqaruv Paneli: http://127.0.0.1:8000/admin
echo - Mobil Ilova:            http://localhost:7777
echo - Swagger API Hujjatlari: http://127.0.0.1:8000/docs
echo.
pause
