from django.conf import settings


def is_app_enabled(app_name):
    """
    Check if an app is enabled based on settings.
    
    Args:
        app_name (str): Name of the app ('ttms' or 'ptms')
    
    Returns:
        bool: True if app is enabled, False otherwise
    """
    setting_name = f'ENABLE_{app_name.upper()}'
    return getattr(settings, setting_name, False)


def get_enabled_apps():
    """
    Get list of all enabled apps.
    
    Returns:
        list: List of enabled app names
    """
    enabled = []
    for app in ['ttms', 'ptms']:
        if is_app_enabled(app):
            enabled.append(app)
    return enabled


def get_app_config(app_name):
    """
    Get configuration for a specific app from settings.
    
    Args:
        app_name (str): Name of the app
    
    Returns:
        dict: Configuration dictionary
    """
    config_name = f'{app_name.upper()}_CONFIG'
    return getattr(settings, config_name, {})
