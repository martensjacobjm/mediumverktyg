@echo off
REM Automatic installation script for Windows
REM Checks Python version and installs dependencies

echo ======================================================================
echo ORC WORKING FLUID ANALYSIS TOOL - AUTOMATIC INSTALLATION
echo ======================================================================

python install.py

if errorlevel 1 (
    echo.
    echo Installation failed. Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo Installation successful!
pause
