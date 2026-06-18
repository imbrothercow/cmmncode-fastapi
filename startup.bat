@echo off
cd /d "%~dp0"

python -m pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo Failed to install dependencies.
    pause
    exit /b 1
)

echo Starting common-code-api server...
python -m uvicorn main:app --reload
pause
