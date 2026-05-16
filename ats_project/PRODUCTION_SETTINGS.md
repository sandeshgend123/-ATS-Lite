# Production settings for PythonAnywhere

# Update the following in ats/settings.py for production:

DEBUG = False

# Add your domain here
ALLOWED_HOSTS = [
    'yourusername.pythonanywhere.com',
    'www.yourusername.pythonanywhere.com',
    'localhost',
    '127.0.0.1',
]

# Use a strong secret key - generate with:
# python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
SECRET_KEY = 'your-secret-key-here'

# Database - use PostgreSQL in production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'your_db_host',
        'PORT': '5432',
    }
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = '/home/yourusername/ats_project/static'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/yourusername/ats_project/media'

# Email configuration for notifications
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'

# CORS settings for your domain
CORS_ALLOWED_ORIGINS = [
    "https://yourusername.pythonanywhere.com",
    "https://www.yourusername.pythonanywhere.com",
]

# Security
CSRF_TRUSTED_ORIGINS = [
    "https://yourusername.pythonanywhere.com",
    "https://www.yourusername.pythonanywhere.com",
]

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/home/yourusername/ats_project/logs/error.log',
        },
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['file', 'console'],
        'level': 'INFO',
    },
}
