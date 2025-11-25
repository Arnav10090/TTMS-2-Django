"""
TTMS (Truck Turnaround Time Monitoring System) specific settings.
Extends base_settings.py with TTMS-only configuration.
"""

import os
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
