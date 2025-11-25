from django.apps import AppConfig


class TTMSAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ttms.auth'
    verbose_name = 'TTMS Authentication'
    label = 'ttms_auth'
