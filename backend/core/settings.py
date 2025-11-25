"""
Default Django settings - defaults to TTMS for backward compatibility.

For app-specific settings, use:
- DJANGO_SETTINGS_MODULE=core.settings_ttms (for TTMS containers)
- DJANGO_SETTINGS_MODULE=core.settings_ptms (for PTMS containers)

This file exists for backward compatibility and defaults to TTMS settings.
"""

from core.settings_ttms import *
