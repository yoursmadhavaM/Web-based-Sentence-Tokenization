@echo off
REM Fixed installation script for Python 3.14 compatibility

echo ======================================================================
echo Installing Dependencies (Python 3.14 Compatible)
echo ======================================================================
echo.

cd /d "%~dp0"

REM Install packages one by one to avoid build issues
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo Using 'python' command...
    echo.
    echo Step 1: Installing FastAPI and Uvicorn...
    python -m pip install fastapi uvicorn[standard] python-multipart pydantic
    echo.
    echo Step 2: Installing spaCy (this may take a few minutes)...
    python -m pip install spacy --only-binary :all:
    if %errorlevel% neq 0 (
        echo.
        echo WARNING: Pre-built spaCy wheel not available for Python 3.14
        echo Trying to install latest spaCy version...
        python -m pip install --upgrade spacy
    )
    echo.
    echo Step 3: Downloading spaCy English model...
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

py --version >nul 2>&1
if %errorlevel% == 0 (
    echo Using 'py' command...
    echo.
    echo Step 1: Installing FastAPI and Uvicorn...
    py -m pip install fastapi uvicorn[standard] python-multipart pydantic
    echo.
    echo Step 2: Installing spaCy (this may take a few minutes)...
    py -m pip install spacy --only-binary :all:
    if %errorlevel% neq 0 (
        echo.
        echo WARNING: Pre-built spaCy wheel not available
        echo Trying to install latest spaCy version...
        py -m pip install --upgrade spacy
    )
    echo.
    echo Step 3: Downloading spaCy English model...
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

echo Python not found!
pause

:end
