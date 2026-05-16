@echo off
REM Quick setup script for ATS Lite (Windows)

echo ===================================
echo ATS Lite - Quick Setup (Windows)
echo ===================================

REM Create virtual environment
echo.
echo 1. Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo 2. Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies
echo 3. Installing dependencies...
pip install -r requirements.txt

REM Run migrations
echo 4. Running migrations...
python manage.py makemigrations
python manage.py migrate

REM Create superuser
echo 5. Creating superuser (admin account)...
python manage.py createsuperuser

REM Collect static files
echo 6. Collecting static files...
python manage.py collectstatic --noinput

echo.
echo ===================================
echo Setup complete!
echo Run: python manage.py runserver
echo Visit: http://127.0.0.1:8000
echo Admin: http://127.0.0.1:8000/admin
echo ===================================
pause
