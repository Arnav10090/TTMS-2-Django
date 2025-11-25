"""
Common validators for TTMS and PTMS applications.
"""

from django.core.exceptions import ValidationError
import re


def validate_phone_number(value):
    """
    Validate phone number format.
    
    Args:
        value: Phone number string
    
    Raises:
        ValidationError: If format is invalid
    """
    if not re.match(r'^[\d\s\-\+\(\)]{10,}$', value):
        raise ValidationError('Invalid phone number format')


def validate_registration_number(value):
    """
    Validate vehicle registration number.
    
    Args:
        value: Registration number
    
    Raises:
        ValidationError: If format is invalid
    """
    if not re.match(r'^[A-Z]{2}\d{2}[A-Z]{2}\d{4}$', value):
        raise ValidationError('Invalid registration number format (e.g., TN01AB1234)')


def validate_positive_number(value):
    """
    Validate that number is positive.
    
    Args:
        value: Numeric value
    
    Raises:
        ValidationError: If number is not positive
    """
    if value < 0:
        raise ValidationError('Value must be positive')


def validate_percentage(value):
    """
    Validate that value is a valid percentage (0-100).
    
    Args:
        value: Numeric value
    
    Raises:
        ValidationError: If value is not 0-100
    """
    if not (0 <= value <= 100):
        raise ValidationError('Value must be between 0 and 100')


def validate_email_domain(value, allowed_domains=None):
    """
    Validate email domain against allowed domains.
    
    Args:
        value: Email address
        allowed_domains: List of allowed domains
    
    Raises:
        ValidationError: If domain is not allowed
    """
    if not allowed_domains:
        return
    
    domain = value.split('@')[1].lower()
    if domain not in allowed_domains:
        raise ValidationError(f'Email domain must be one of: {", ".join(allowed_domains)}')


def validate_unique_together(model, **kwargs):
    """
    Validate unique_together constraint.
    
    Args:
        model: Django model class
        **kwargs: Field values to check
    
    Raises:
        ValidationError: If combination already exists
    """
    if model.objects.filter(**kwargs).exists():
        raise ValidationError(f'{model.__name__} with these values already exists')


def validate_choice_field(value, choices):
    """
    Validate that value is in allowed choices.
    
    Args:
        value: Value to validate
        choices: List/tuple of allowed choices
    
    Raises:
        ValidationError: If value is not in choices
    """
    if value not in [choice[0] for choice in choices]:
        raise ValidationError(f'Invalid choice. Must be one of: {", ".join([str(c[0]) for c in choices])}')
