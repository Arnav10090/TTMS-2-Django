#!/usr/bin/env python
"""
Direct database migration using Django ORM without the migration loader check.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings_ptms')
django.setup()

from django.core.management import call_command

# Try to migrate using call_command with arguments
try:
    call_command('migrate', verbosity=2)
    print("Migration successful!")
except Exception as e:
    print(f"Migration failed: {e}")
