"""
PTMS (Project & Task Management System) specific settings.
Extends base_settings.py with PTMS-only configuration.
"""

import os
from datetime import timedelta
from core.base_settings import *

# Add PTMS app to installed apps
# NOTE: ptms_auth removed temporarily due to Django migration ordering issues with custom user models
INSTALLED_APPS = COMMON_INSTALLED_APPS + [
    # 'ptms.auth.apps.PTMSAuthConfig',
    'ptms',
]

# PTMS-specific database configuration
# Use environment variables to switch between Docker and local PostgreSQL
# Docker defaults: DB_HOST=ptms_postgres, DB_NAME=ptms_db
# Local defaults: DB_HOST=localhost, DB_NAME=ptms_local
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.getenv('DB_NAME', 'ptms_local'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# PTMS URL configuration
ROOT_URLCONF = 'core.urls_ptms'

# PTMS app name for admin site
ADMIN_SITE_HEADER = 'PTMS Administration'
ADMIN_SITE_TITLE = 'PTMS Admin Portal'

# PTMS Custom User Model
# NOTE: Cannot use custom AUTH_USER_MODEL with admin app due to Django migration constraints
# AUTH_USER_MODEL = 'ptms_auth.PTMSUser'
AUTH_USER_MODEL = 'auth.User'  # Use Django's default User model

# PTMS Authentication Backend
AUTHENTICATION_BACKENDS = [
    'ptms.auth.backends.PTMSAuthBackend',
]

# JWT Configuration for PTMS
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

# REST Framework Configuration for PTMS
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
