"""
PTMS (Project & Task Management System) specific settings.
Extends base_settings.py with PTMS-only configuration.
"""

import os
from core.base_settings import *

# Add PTMS app to installed apps
INSTALLED_APPS = COMMON_INSTALLED_APPS + [
    'ptms',
]

# PTMS-specific database configuration
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.getenv('DB_NAME', 'ptms_db'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
        'HOST': os.getenv('DB_HOST', 'ptms_postgres'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# PTMS URL configuration
ROOT_URLCONF = 'core.urls_ptms'

# PTMS app name for admin site
ADMIN_SITE_HEADER = 'PTMS Administration'
ADMIN_SITE_TITLE = 'PTMS Admin Portal'
