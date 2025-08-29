@echo off


echo Checking/installing dependencies...

python -m pip --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Error: pip is not available. Please ensure Python and pip are installed and in PATH.
    pause
    exit /b 1
)

python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies from requirements.txt.
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate
call cls
exit /b 0