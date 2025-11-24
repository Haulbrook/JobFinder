@echo off
REM View Multi-Platform Job Queue (Windows)
cd /d "%~dp0"
chcp 65001 > nul
python search_jobs.py view
pause
