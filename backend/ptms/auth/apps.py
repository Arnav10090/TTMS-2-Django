from django.apps import AppConfig


class PTMSAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ptms.auth'
    verbose_name = 'PTMS Authentication'
    label = 'ptms_auth'
