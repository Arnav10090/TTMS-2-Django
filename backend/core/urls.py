from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from core.utils import get_enabled_apps


class AppStatusView(APIView):
    """
    API endpoint to check the status of enabled apps
    """
    def get(self, request):
        enabled_apps = get_enabled_apps()
        return Response({
            'ttms_enabled': settings.ENABLE_TTMS,
            'ptms_enabled': settings.ENABLE_PTMS,
            'enabled_apps': enabled_apps,
            'ttms_config': settings.TTMS_CONFIG if settings.ENABLE_TTMS else None,
            'ptms_config': settings.PTMS_CONFIG if settings.ENABLE_PTMS else None,
        })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/status/', AppStatusView.as_view(), name='app-status'),
]

# Dynamically include app URLs based on settings
if settings.ENABLE_TTMS:
    urlpatterns.append(
        path('api/ttms/', include('ttms.urls', namespace='ttms'))
    )

if settings.ENABLE_PTMS:
    urlpatterns.append(
        path('api/ptms/', include('ptms.urls', namespace='ptms'))
    )
