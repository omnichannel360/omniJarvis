@echo off
cd /d "%~dp0"
echo Launching Jarvis Desktop App...
.venv\Scripts\python.exe hands/desktop_app.py
pause
