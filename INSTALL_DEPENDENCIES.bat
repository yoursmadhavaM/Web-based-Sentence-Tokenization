@echo off
REM Script to install all dependencies for the Sentence Segmentation Tool

echo ======================================================================
echo Installing Dependencies for Sentence Segmentation Tool
echo ======================================================================
echo.

REM Change to project directory
cd /d "%~dp0"

echo Current directory: %CD%
echo.

REM Try different Python commands to install dependencies
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo Using 'python' command...
    echo.
    echo Step 1: Installing Python packages...
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    echo.
    echo Step 2: Downloading spaCy English model...
    python -m spacy download en_core_web_sm
    echo.
    echo ======================================================================
    echo Installation Complete!
    echo ======================================================================
    echo.
    echo You can now start the server with:
    echo   python run_server.py
    echo.
    pause
    goto :end
)

python3 --version >nul 2>&1
if %errorlevel% == 0 (
    echo Using 'python3' command...
    echo.
    echo Step 1: Installing Python packages...
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements.txt
    echo.
    echo Step 2: Downloading spaCy English model...
    python3 -m spacy download en_core_web_sm
    echo.
    echo ======================================================================
    echo Installation Complete!
    echo ======================================================================
    echo.
    echo You can now start the server with:
    echo   python3 run_server.py
    echo.
    pause
    goto :end
)

py --version >nul 2>&1
if %errorlevel% == 0 (
    echo Using 'py' command...
    echo.
    echo Step 1: Installing Python packages...
    py -m pip install --upgrade pip
    py -m pip install -r requirements.txt
    echo.
    echo Step 2: Downloading spaCy English model...
    py -m spacy download en_core_web_sm
    echo.
    echo ======================================================================
    echo Installation Complete!
    echo ======================================================================
    echo.
    echo You can now start the server with:
    echo   py run_server.py
    echo.
    pause
    goto :end
)

echo.
echo ERROR: Python not found!
echo.
echo Please install Python from https://www.python.org/downloads/
echo Make sure to check "Add Python to PATH" during installation
echo.
pause

:end
