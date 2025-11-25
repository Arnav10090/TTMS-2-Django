"""
Common constants and enums for TTMS and PTMS applications.
"""

from enum import Enum


class AppName(str, Enum):
    """Application names"""
    TTMS = 'ttms'
    PTMS = 'ptms'


class TimeRange(str, Enum):
    """Time range options for data queries"""
    TODAY = 'today'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
    YEARLY = 'yearly'
    CUSTOM = 'custom'


class StatusCode(int, Enum):
    """Common status codes"""
    SUCCESS = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409
    SERVER_ERROR = 500


class SortOrder(str, Enum):
    """Sort order options"""
    ASC = 'asc'
    DESC = 'desc'


# TTMS specific constants
TTMS_CONSTANTS = {
    'VEHICLE_REG_FORMAT': r'^[A-Z]{2}\d{2}[A-Z]{2}\d{4}$',
    'MIN_TURNAROUND_TIME': 15,  # minutes
    'MAX_TURNAROUND_TIME': 480,  # 8 hours
    'PARKING_AREAS': {
        'AREA_1': 'Area 1',
        'AREA_2': 'Area 2',
    },
    'VEHICLE_STAGES': [
        'gateEntry',
        'tareWeighing',
        'loading',
        'postLoadingWeighing',
        'gateExit',
    ],
    'STAGE_STATES': [
        'pending',
        'active',
        'completed',
    ],
    'ALERT_LEVELS': [
        'info',
        'warning',
        'critical',
    ],
}

# PTMS specific constants
PTMS_CONSTANTS = {
    'PROJECT_STATUS': [
        'active',
        'completed',
        'on_hold',
        'cancelled',
    ],
    'TASK_STATUS': [
        'pending',
        'in_progress',
        'completed',
        'blocked',
    ],
    'TASK_PRIORITY': [
        'low',
        'medium',
        'high',
        'critical',
    ],
}

# Common response messages
MESSAGES = {
    'SUCCESS': 'Operation completed successfully',
    'CREATED': 'Resource created successfully',
    'UPDATED': 'Resource updated successfully',
    'DELETED': 'Resource deleted successfully',
    'ERROR': 'An error occurred',
    'INVALID_DATA': 'Invalid data provided',
    'NOT_FOUND': 'Resource not found',
    'UNAUTHORIZED': 'Authentication required',
    'FORBIDDEN': 'Permission denied',
    'CONFLICT': 'Resource already exists',
}

# API response headers
RESPONSE_HEADERS = {
    'X-API-Version': '1.0',
    'X-Request-ID': 'unique-request-id',
}

# Pagination defaults
PAGINATION_DEFAULTS = {
    'page_size': 100,
    'max_page_size': 1000,
    'min_page_size': 10,
}

# Cache timeout (in seconds)
CACHE_TIMEOUTS = {
    'SHORT': 300,  # 5 minutes
    'MEDIUM': 3600,  # 1 hour
    'LONG': 86400,  # 24 hours
}
