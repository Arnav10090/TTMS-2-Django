"""
Common utility functions shared between TTMS and PTMS.
These are lightweight helpers - NO business logic, NO models.
"""

from datetime import datetime, timedelta
from django.utils import timezone


def get_time_range(days: int = 30) -> tuple:
    """
    Get start and end datetime for a given number of days.
    
    Args:
        days: Number of days to go back (default 30)
    
    Returns:
        Tuple of (start_datetime, end_datetime)
    """
    end = timezone.now()
    start = end - timedelta(days=days)
    return start, end


def get_date_range_month() -> tuple:
    """
    Get start and end datetime for current month.
    
    Returns:
        Tuple of (start_datetime, end_datetime)
    """
    today = timezone.now()
    start = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    if today.month == 12:
        end = start.replace(year=start.year + 1, month=1) - timedelta(seconds=1)
    else:
        end = start.replace(month=start.month + 1) - timedelta(seconds=1)
    
    return start, end


def get_date_range_year() -> tuple:
    """
    Get start and end datetime for current year.
    
    Returns:
        Tuple of (start_datetime, end_datetime)
    """
    today = timezone.now()
    start = today.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    end = start.replace(year=start.year + 1) - timedelta(seconds=1)
    
    return start, end


def get_date_range_today() -> tuple:
    """
    Get start and end datetime for today.
    
    Returns:
        Tuple of (start_datetime, end_datetime)
    """
    today = timezone.now()
    start = today.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1) - timedelta(seconds=1)
    
    return start, end


def format_duration_minutes(minutes: int) -> str:
    """
    Format minutes into human-readable duration string.
    
    Args:
        minutes: Number of minutes
    
    Returns:
        Formatted string (e.g., "1h 30m", "45m")
    """
    if minutes < 0:
        return "0m"
    
    hours = minutes // 60
    mins = minutes % 60
    
    if hours == 0:
        return f"{mins}m"
    elif mins == 0:
        return f"{hours}h"
    else:
        return f"{hours}h {mins}m"


def format_percentage(value: float, decimal_places: int = 1) -> str:
    """
    Format value as percentage string.
    
    Args:
        value: Float value (0-100)
        decimal_places: Number of decimal places
    
    Returns:
        Formatted percentage string
    """
    if not isinstance(value, (int, float)):
        return "0%"
    
    return f"{value:.{decimal_places}f}%"


def truncate_text(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    Truncate text to max length and add suffix.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
    
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def chunk_list(lst: list, chunk_size: int) -> list:
    """
    Split list into chunks of given size.
    
    Args:
        lst: List to chunk
        chunk_size: Size of each chunk
    
    Returns:
        List of chunks
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def safe_get_dict(dictionary: dict, key: str, default=None):
    """
    Safely get value from dictionary with dot notation support.
    
    Example:
        safe_get_dict({'a': {'b': 'value'}}, 'a.b') -> 'value'
    
    Args:
        dictionary: Dictionary to get value from
        key: Key (supports dot notation)
        default: Default value if key not found
    
    Returns:
        Value or default
    """
    keys = key.split('.')
    value = dictionary
    
    for k in keys:
        if isinstance(value, dict):
            value = value.get(k)
            if value is None:
                return default
        else:
            return default
    
    return value
