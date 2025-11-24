from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    KPIMetricsViewSet, VehicleViewSet, VehicleStageViewSet,
    ParkingCellViewSet, VehicleEntryViewSet, SystemAlertViewSet,
    TurnaroundTimeSparklineViewSet
)

router = DefaultRouter()
router.register(r'kpi', KPIMetricsViewSet, basename='kpi')
router.register(r'vehicles', VehicleViewSet, basename='vehicle')
router.register(r'stages', VehicleStageViewSet, basename='stage')
router.register(r'parking', ParkingCellViewSet, basename='parking')
router.register(r'entries', VehicleEntryViewSet, basename='entry')
router.register(r'alerts', SystemAlertViewSet, basename='alert')
router.register(r'sparkline', TurnaroundTimeSparklineViewSet, basename='sparkline')

urlpatterns = [
    path('', include(router.urls)),
]
