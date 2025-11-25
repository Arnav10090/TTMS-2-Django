from django.core.management.base import BaseCommand
from django.conf import settings
from core.utils import get_enabled_apps


class Command(BaseCommand):
    help = 'Check the status of installed apps'
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('APP STATUS REPORT'))
        self.stdout.write(self.style.SUCCESS('='*60 + '\n'))
        
        enabled_apps = get_enabled_apps()
        
        apps = {
            'ttms': {
                'enabled': settings.ENABLE_TTMS,
                'config': settings.TTMS_CONFIG,
            },
            'ptms': {
                'enabled': settings.ENABLE_PTMS,
                'config': settings.PTMS_CONFIG,
            },
        }
        
        for app_name, app_info in apps.items():
            if app_info['enabled']:
                self.stdout.write(self.style.SUCCESS(f'✓ {app_name.upper()} is ENABLED'))
                config = app_info['config']
                self.stdout.write(f'  Name: {config.get("name")}')
                self.stdout.write(f'  Description: {config.get("description")}')
                self.stdout.write(f'  Prefix: /api/{config.get("prefix")}/')
            else:
                self.stdout.write(self.style.ERROR(f'✗ {app_name.upper()} is DISABLED'))
            self.stdout.write('')
        
        self.stdout.write(self.style.SUCCESS(f'Enabled apps: {", ".join(enabled_apps) if enabled_apps else "None"}'))
        self.stdout.write(self.style.SUCCESS('='*60 + '\n'))
