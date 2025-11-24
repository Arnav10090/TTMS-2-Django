@echo off
REM Django Backend Startup Script for Windows

echo.
echo Django Backend Startup Script
echo ==================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

echo Virtual environment activated

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt --quiet

if errorlevel 1 (
    echo Failed to install dependencies
    pause
    exit /b 1
)

echo Dependencies installed

REM Check if .env exists
if not exist ".env" (
    echo.
    echo Creating .env file from .env.example...
    copy .env.example .env
    echo .env file created (please update with your database credentials)
)

REM Run migrations
echo.
echo Running database migrations...
python manage.py migrate

if errorlevel 1 (
    echo Migration failed
    pause
    exit /b 1
)

echo Database migrations completed

REM Start development server
echo.
echo ==================================
echo Starting Django Development Server
echo ==================================
echo.
echo API URL: http://localhost:8000/api/
echo Admin URL: http://localhost:8000/admin/
echo.

python manage.py runserver

pause
