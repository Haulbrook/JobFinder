@echo off
REM Multi-Platform Job Search Runner (Windows)
cd /d "%~dp0"
chcp 65001 > nul
python search_jobs.py search "automation developer" "Remote" 10
pause
