@echo off
echo === Setting up API environment ===

REM Check if Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in PATH.
    exit /b 1
)

REM Create virtual environment
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Upgrade pip
python -m pip install --upgrade pip

REM Install dependencies
python -m pip install -r requirements.txt

REM Ensure database directory exists
if not exist api\data\create_database\instance (
    mkdir api\data\create_database\instance
)

REM Build database
python api\data\create_database\create_database.py

REM Navigate to api directory
cd api

REM Save data into database
python -m data.save_location.save_location_zone
python -m data.save_location.save_payment
python -m data.save_location.save_ratecode
python -m data.save_location.save_vendor
python -m data.save_location.save_trips

echo Backend Environment setup complete. Running at http://localhost:8000

REM Launch backend server
python -m web.app
