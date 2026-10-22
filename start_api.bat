@echo off
title Universal Hayvonlar Bozori - FastAPI Server
cd /d "%~dp0backend"
echo ===============================================================
echo  Universal Hayvonlar Bozori Backend API Server
echo  Asosiy manzil:    http://127.0.0.1:8000
echo  API Hujjatlari:   http://127.0.0.1:8000/docs
echo ===============================================================
echo Brauzerda ochilmoqda: http://127.0.0.1:8000/docs
start http://127.0.0.1:8000/docs
python run.py
pause
