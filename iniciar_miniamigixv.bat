@echo off
cd /d "%~dp0"

start "MiniAmigixV Server" /min cmd /k "cd /d "%~dp0" && if exist "env\Scripts\activate.bat" call "env\Scripts\activate.bat" && python manage.py runserver 127.0.0.1:8000"

timeout /t 3 /nobreak > nul
start "" "http://127.0.0.1:8000/home/"
