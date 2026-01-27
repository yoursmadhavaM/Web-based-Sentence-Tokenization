@echo off
REM Batch script to start the Sentence Segmentation server on Windows

echo ======================================================================
echo Starting Sentence Segmentation API Server
echo ======================================================================
echo.

REM Try different Python commands
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo Using 'python' command...
    python run_server.py
    goto :end
)

python3 --version >nul 2>&1
if %errorlevel% == 0 (
    echo Using 'python3' command...
    python3 run_server.py
    goto :end
)

py --version >nul 2>&1
if %errorlevel% == 0 (
    echo Using 'py' command...
    py run_server.py
    goto :end
)

echo.
echo ERROR: Python not found!
echo.
echo Please try one of these solutions:
echo.
echo 1. Install Python from https://www.python.org/downloads/
echo    Make sure to check "Add Python to PATH" during installation
echo.
echo 2. Try running manually with:
echo    py run_server.py
echo    or
echo    python3 run_server.py
echo.
echo 3. If Python is installed but not in PATH, use full path:
echo    C:\Python311\python.exe run_server.py
echo.
pause

:end
