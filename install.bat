@echo off
REM Smart installation that finds correct Python version automatically

python install.py

if errorlevel 1 (
    echo.
    echo Installation failed or no compatible Python found.
    echo.
    pause
    exit /b 1
)

echo.
pause

