from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    KPIMetricsViewSet, VehicleViewSet, VehicleStageViewSet,
    ParkingCellViewSet, VehicleEntryViewSet, SystemAlertViewSet,
    TurnaroundTimeSparklineViewSet, LoadingGateViewSet
)

router = DefaultRouter()
router.register(r'kpi', KPIMetricsViewSet, basename='kpi')
router.register(r'vehicles', VehicleViewSet, basename='vehicle')
router.register(r'vehicle-stages', VehicleStageViewSet, basename='vehicle-stage')
router.register(r'parking-cells', ParkingCellViewSet, basename='parking-cell')
router.register(r'vehicle-entries', VehicleEntryViewSet, basename='vehicle-entry')
router.register(r'alerts', SystemAlertViewSet, basename='alert')
router.register(r'sparkline', TurnaroundTimeSparklineViewSet, basename='sparkline')
router.register(r'loading-gates', LoadingGateViewSet, basename='loading-gate')

app_name = 'ttms'

urlpatterns = [
    path('', include(router.urls)),
]
