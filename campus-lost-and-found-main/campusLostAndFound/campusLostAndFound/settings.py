"""
Django settings for campusLostAndFound project.
Yeh file Django project ki sari settings rakhti hai.
"""

from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

# Base directory path - project ka root folder
BASE_DIR = Path(__file__).resolve().parent.parent

# .env file se values load karna (local ke liye)
load_dotenv(BASE_DIR / '.env')

# Security key - production mein isko secret rakhna zaroori hai
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-local-dev-key')

# Debug mode - development ke liye True, production mein False karna
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# Allowed hosts - production mein apna domain add karna
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.onrender.com']
CSRF_TRUSTED_ORIGINS = ['https://*.onrender.com']


# Application definition - sab installed apps ki list
INSTALLED_APPS = [
    'django.contrib.admin',  # Admin panel ke liye
    'django.contrib.auth',  # Authentication system ke liye
    'django.contrib.contenttypes',  # Content types framework
    'django.contrib.sessions',  # Session management
    'django.contrib.messages',  # Messaging framework
    'django.contrib.staticfiles',  # Static files handling
    
    # Third-party apps
    'crispy_forms',  # Forms ko bootstrap style dene ke liye
    'crispy_bootstrap5',  # Bootstrap 5 template pack
    
    # Local apps - humara main app
    'items',
]

# Middleware configuration - request/response processing ke liye
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Root URL configuration file
ROOT_URLCONF = 'campusLostAndFound.urls'

# Templates configuration - HTML templates ke liye settings
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Global templates folder
        'APP_DIRS': True,  # Har app mein templates folder dhundna
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI application path
WSGI_APPLICATION = 'campusLostAndFound.wsgi.application'


# Database configuration - SQLite use kar rahe hain
# DATABASE_URL set hai to PostgreSQL, warna SQLite
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        ssl_require=bool(os.environ.get('DATABASE_URL')),
    )
}


# Password validation rules - strong passwords ke liye
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization settings
LANGUAGE_CODE = 'en-us'  # English language
TIME_ZONE = 'Asia/Karachi'  # Pakistan timezone
USE_I18N = True  # Internationalization enable
USE_TZ = True  # Timezone support enable


# Static files configuration (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # Additional static folders
STATIC_ROOT = BASE_DIR / 'staticfiles'
STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage'},
}

# Media files configuration - user uploaded files ke liye
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Crispy Forms configuration - Bootstrap 5 use karne ke liye
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Login/Logout redirect URLs
LOGIN_REDIRECT_URL = 'item_list'  # Login ke baad yahan redirect hoga
LOGOUT_REDIRECT_URL = 'item_list'  # Logout ke baad yahan redirect hoga
LOGIN_URL = 'login'  # Login page ka URL