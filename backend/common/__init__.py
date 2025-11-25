"""
Common utilities shared between TTMS and PTMS applications.
This module contains lightweight helper functions, NOT models or authentication logic.

Each app (TTMS and PTMS) manages its own:
- Authentication & User models
- Business logic & models
- Permissions & authorization

This module only provides:
- Common helper functions
- Pagination classes
- Response formatting
- Validators
- Constants & enums
"""

__version__ = '1.0.0'
