from pathlib import Path
import os
import sys
from dotenv import load_dotenv

# -----------------------------
# Базовая директория проекта
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------
# Загружаем .env
# -----------------------------
load_dotenv(BASE_DIR / '.env')

# -----------------------------
# Безопасность
# -----------------------------
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-key')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

# -----------------------------
# Приложения
# -----------------------------
INSTALLED_APPS = [
    # стандартные Django приложения
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # сторонние
    'rest_framework',

    # локальные
    'users',
    'materials',
    'payments',
    'blog'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'lms_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
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

WSGI_APPLICATION = 'lms_project.wsgi.application'

# -----------------------------
# База данных
# -----------------------------
if "test" in sys.argv:
    # Для запуска тестов — SQLite в памяти
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    }
else:
    # PostgreSQL из переменных окружения (.env или CI/CD)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('POSTGRES_DB', 'lms_db'),
            'USER': os.getenv('POSTGRES_USER', 'test_user'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'test_pass'),
            'HOST': os.getenv('POSTGRES_HOST', '127.0.0.1'),
            'PORT': os.getenv('POSTGRES_PORT', '5432'),
        }
    }

# -----------------------------
# Валидаторы паролей
# -----------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -----------------------------
# Локализация
# -----------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# -----------------------------
# Статика и медиа
# -----------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# -----------------------------
# Кастомная модель пользователя
# -----------------------------
AUTH_USER_MODEL = 'users.User'

# -----------------------------
# DRF
# -----------------------------
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}

# -----------------------------
# Primary key field type
# -----------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -----------------------------
# Stripe ключи
# -----------------------------
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "sk_test_sk_test_51S1ON1BAdFbKgv8xcAU13QAGDRjCajfWw9IMKg2M3PBDnT1QbjCSts3xPBlPpUWZxNosuHXjlKTfFrwpsGAGh3Lk00o4HhmnPH")
STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY", "pk_test_pk_test_51S1ON1BAdFbKgv8xZkIqthPE7qZuIXeq3efVbI4MdiEXVShGNVA3BNaAl9GdaDXbRUMBU9erhspQBIXPRFR5eao000olQPc0Oh")

# -----------------------------
# Redis URL (для кэша или Celery)
# -----------------------------
REDIS_URL = os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/0')
