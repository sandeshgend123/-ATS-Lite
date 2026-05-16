#!/bin/bash
# Quick setup script for ATS Lite

echo "==================================="
echo "ATS Lite - Quick Setup"
echo "==================================="

# Create virtual environment
echo ""
echo "1. Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "2. Activating virtual environment..."
source venv/bin/activate || venv\Scripts\activate

# Install dependencies
echo "3. Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "4. Running migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser
echo "5. Creating superuser (admin account)..."
python manage.py createsuperuser

# Collect static files
echo "6. Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "==================================="
echo "Setup complete!"
echo "Run: python manage.py runserver"
echo "Visit: http://127.0.0.1:8000"
echo "Admin: http://127.0.0.1:8000/admin"
echo "==================================="
