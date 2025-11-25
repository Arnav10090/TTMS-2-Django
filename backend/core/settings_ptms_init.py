"""
Temporary PTMS settings for initial migration without ptms_auth.
Used only to bootstrap the database.
"""

import os
from datetime import timedelta
from core.base_settings import *

# Add PTMS app WITHOUT ptms.auth to avoid circular dependencies
INSTALLED_APPS = COMMON_INSTALLED_APPS + [
    'ptms',
]

# PTMS-specific database configuration
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

ROOT_URLCONF = 'core.urls_ptms'
ADMIN_SITE_HEADER = 'PTMS Administration'
ADMIN_SITE_TITLE = 'PTMS Admin Portal'

# Will be overridden by actual settings
AUTH_USER_MODEL = 'auth.User'
