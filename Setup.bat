@echo off
REM VoiceForge 2762 — Windows setup wizard
REM Creates a virtual environment, installs dependencies, preloads the model.
title VoiceForge 2762 Setup
cd /d "%~dp0"

echo ============================================
echo   VoiceForge 2762 — Setup
echo ============================================
echo.

where python >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Python not found. Install Python 3.10+ from python.org
  echo and tick "Add python.exe to PATH" during install.
  pause
  exit /b 1
)

for /f "tokens=*" %%v in ('python --version 2^>^&1') do echo Found %%v

if not exist .venv (
  echo Creating virtual environment...
  python -m venv .venv
  if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment.
    pause
    exit /b 1
  )
)

echo Upgrading pip...
.venv\Scripts\python.exe -m pip install --upgrade pip

echo Installing dependencies (this may take a few minutes)...
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 (
  echo [ERROR] Dependency install failed. Check your internet connection.
  pause
  exit /b 1
)

where ffmpeg >nul 2>nul
if errorlevel 1 (
  echo [NOTE] FFmpeg was not found on PATH. Pitch, reverb, BGM and MP3
  echo output need FFmpeg — install it from ffmpeg.org and retry if needed.
)

echo.
echo Preloading the Pocket TTS model (first run downloads weights)...
.venv\Scripts\python.exe preload_model.py
if errorlevel 1 (
  echo [NOTE] Model preload did not finish. The server will retry on first use.
)

echo.
echo ============================================
echo   Setup complete!
echo   Run VoiceForge2762.vbs to launch the studio,
echo   then open http://127.0.0.1:7860
echo ============================================
pause
