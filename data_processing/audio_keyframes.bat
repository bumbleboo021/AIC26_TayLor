@echo off
title Data Processing Pipeline

echo ==========================================
echo Bước 1: Cai dat requirements...
echo ==========================================
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [LỖI] Cai dat requirements that bai!
    pause
    exit /b %errorlevel%
)

echo.
echo ==========================================
echo Bước 2: Extracting audio...
echo ==========================================
python extract_audio.py
if %errorlevel% neq 0 (
    echo [LỖI] Chay extract_audio.py that bai!
    pause
    exit /b %errorlevel%
)

echo.
echo ==========================================
echo Bước 3: Extracting keyframes...
echo ==========================================
python extract_keyframes.py
if %errorlevel% neq 0 (
    echo [LỖI] Chay extract_keyframes.py that bai!
    pause
    exit /b %errorlevel%
)

echo.
echo ==========================================
echo Bước 4: Compressing keyframes...
echo ==========================================
python compress_keyframes.py
if %errorlevel% neq 0 (
    echo [LỖI] Chay compress_keyframes.py that bai!
    pause
    exit /b %errorlevel%
)

echo.
echo ==========================================
echo Hoan thanh toan bo qua trinh!
echo ==========================================
pause