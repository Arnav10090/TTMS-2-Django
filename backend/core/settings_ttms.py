"""
TTMS (Truck Turnaround Time Monitoring System) specific settings.
Extends base_settings.py with TTMS-only configuration.
"""

import os
from datetime import timedelta
from core.base_settings import *

# Add TTMS app to installed apps
INSTALLED_APPS = COMMON_INSTALLED_APPS + [
    'ttms',
]

# TTMS-specific database configuration
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.getenv('DB_NAME', 'ttms_db'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
        'HOST': os.getenv('DB_HOST', 'ttms_postgres'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# TTMS URL configuration
ROOT_URLCONF = 'core.urls_ttms'

# TTMS app name for admin site
ADMIN_SITE_HEADER = 'TTMS Administration'
ADMIN_SITE_TITLE = 'TTMS Admin Portal'

# TTMS Custom User Model
AUTH_USER_MODEL = 'ttms_auth.TTMSUser'

# TTMS Authentication Backend
AUTHENTICATION_BACKENDS = [
    'ttms.auth.backends.TTMSAuthBackend',
]

# JWT Configuration for TTMS
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}

# REST Framework Configuration for TTMS
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
