@echo off
REM RF SnP to CSV Converter - GUI Launcher
REM Convenient launcher for the PyQt6 application

echo Starting RF SnP to CSV Converter...
echo.

cd /d "%~dp0"
"C:\Project\html_exporter\.venv\Scripts\python.exe" ui_pyqt6\main.py

if errorlevel 1 (
    echo.
    echo Application encountered an error.
    pause
)
