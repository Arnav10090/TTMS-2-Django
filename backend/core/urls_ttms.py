"""
TTMS (Truck Turnaround Time Monitoring System) URL Configuration

This is the main URL router for the TTMS application.
All TTMS API endpoints are defined here.

Routes:
- /admin/ - Django admin interface
- /api/ttms/ - TTMS data endpoints (KPI, vehicles, parking, etc.)
- /api/ttms/auth/ - TTMS authentication endpoints
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenVerifyView

# Import TTMS auth views and viewsets
from ttms.auth.views import (
    TTMSTokenObtainPairView,
    TTMSTokenRefreshView,
    TTMSUserViewSet
)

# Import TTMS data viewsets
from ttms.views import (
    KPIMetricsViewSet,
    VehicleViewSet,
    VehicleStageViewSet,
    ParkingCellViewSet,
    VehicleEntryViewSet,
    SystemAlertViewSet,
    TurnaroundTimeSparklineViewSet,
    LoadingGateViewSet,
)

# Create router for TTMS endpoints
router = DefaultRouter()

# Auth routes
router.register(r'auth/users', TTMSUserViewSet, basename='ttms-users')

# Data routes
router.register(r'kpi', KPIMetricsViewSet, basename='ttms-kpi')
router.register(r'vehicles', VehicleViewSet, basename='ttms-vehicle')
router.register(r'vehicle-stages', VehicleStageViewSet, basename='ttms-vehicle-stage')
router.register(r'parking-cells', ParkingCellViewSet, basename='ttms-parking-cell')
router.register(r'vehicle-entries', VehicleEntryViewSet, basename='ttms-vehicle-entry')
router.register(r'alerts', SystemAlertViewSet, basename='ttms-alert')
router.register(r'sparkline', TurnaroundTimeSparklineViewSet, basename='ttms-sparkline')
router.register(r'loading-gates', LoadingGateViewSet, basename='ttms-loading-gate')

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),
    
    # API endpoints with TTMS router
    path('api/ttms/', include(router.urls)),
    
    # JWT Token endpoints
    path('api/ttms/auth/login/', TTMSTokenObtainPairView.as_view(), name='ttms-token-obtain-pair'),
    path('api/ttms/auth/refresh/', TTMSTokenRefreshView.as_view(), name='ttms-token-refresh'),
    path('api/ttms/auth/verify/', TokenVerifyView.as_view(), name='ttms-token-verify'),
]
