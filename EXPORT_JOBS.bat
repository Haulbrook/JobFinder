@echo off
REM Export Jobs to CSV (Windows)
cd /d "%~dp0"
chcp 65001 > nul
set timestamp=%date:~-4%%date:~4,2%%date:~7,2%
python search_jobs.py export jobs_%timestamp%.csv
echo Jobs exported to jobs_%timestamp%.csv
pause
