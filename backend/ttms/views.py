from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q
from .models import (
    KPIMetrics, Vehicle, VehicleStage, ParkingCell,
    VehicleEntry, SystemAlert, TurnaroundTimeSparkline
)
from .serializers import (
    KPIMetricsSerializer, KPIMetricsDetailSerializer,
    VehicleSerializer, VehicleCreateUpdateSerializer,
    VehicleStageSerializer, ParkingCellSerializer,
    VehicleEntrySerializer, SystemAlertSerializer,
    TurnaroundTimeSparklineSerializer
)


class KPIMetricsViewSet(viewsets.ModelViewSet):
    """
    API endpoint for KPI metrics
    """
    queryset = KPIMetrics.objects.all()
    serializer_class = KPIMetricsSerializer
    
    @action(detail=False, methods=['get'])
    def latest(self, request):
        """Get the latest KPI metrics"""
        latest_kpi = KPIMetrics.objects.order_by('-updated_at').first()
        if latest_kpi:
            serializer = KPIMetricsDetailSerializer(latest_kpi)
            return Response(serializer.data)
        return Response({'error': 'No KPI data available'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'])
    def create_or_update(self, request):
        """Create or update KPI metrics"""
        latest_kpi = KPIMetrics.objects.order_by('-updated_at').first()
        
        if latest_kpi:
            serializer = KPIMetricsSerializer(latest_kpi, data=request.data, partial=True)
        else:
            serializer = KPIMetricsSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VehicleViewSet(viewsets.ModelViewSet):
    """
    API endpoint for vehicles
    Supports filtering by reg_no and rfid_no
    """
    queryset = Vehicle.objects.prefetch_related('stages').order_by('-timestamp')
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['reg_no', 'rfid_no']
    ordering_fields = ['reg_no', 'turnaround_time', 'progress', 'timestamp']
    ordering = ['-timestamp']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return VehicleCreateUpdateSerializer
        return VehicleSerializer
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get vehicles currently in progress"""
        vehicles = Vehicle.objects.filter(
            stages__state__in=['active', 'pending']
        ).distinct().prefetch_related('stages')
        serializer = VehicleSerializer(vehicles, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def completed(self, request):
        """Get vehicles with completed turnaround"""
        vehicles = Vehicle.objects.filter(
            stages__state='completed'
        ).distinct().prefetch_related('stages')
        serializer = VehicleSerializer(vehicles, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def update_stage(self, request, pk=None):
        """Update a specific stage for a vehicle"""
        vehicle = self.get_object()
        stage_name = request.data.get('stage')
        stage_data = request.data.get('data', {})
        
        try:
            stage = VehicleStage.objects.get(vehicle=vehicle, stage=stage_name)
            serializer = VehicleStageSerializer(stage, data=stage_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except VehicleStage.DoesNotExist:
            return Response(
                {'error': f'Stage {stage_name} not found for this vehicle'},
                status=status.HTTP_404_NOT_FOUND
            )


class VehicleStageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for vehicle stages
    """
    queryset = VehicleStage.objects.all()
    serializer_class = VehicleStageSerializer
    filter_backends = [SearchFilter]
    search_fields = ['vehicle__reg_no', 'stage']
    
    @action(detail=False, methods=['get'])
    def by_vehicle(self, request):
        """Get all stages for a specific vehicle"""
        vehicle_id = request.query_params.get('vehicle_id')
        if not vehicle_id:
            return Response(
                {'error': 'vehicle_id parameter required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        stages = VehicleStage.objects.filter(vehicle_id=vehicle_id).order_by('stage')
        serializer = VehicleStageSerializer(stages, many=True)
        return Response(serializer.data)


class ParkingCellViewSet(viewsets.ModelViewSet):
    """
    API endpoint for parking cells
    """
    queryset = ParkingCell.objects.all()
    serializer_class = ParkingCellSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['area', 'label', 'status']
    ordering_fields = ['area', 'label', 'status']
    ordering = ['area', 'label']
    
    @action(detail=False, methods=['get'])
    def by_area(self, request):
        """Get parking cells grouped by area"""
        area = request.query_params.get('area')
        if area:
            cells = ParkingCell.objects.filter(area=area).order_by('label')
        else:
            cells = ParkingCell.objects.all().order_by('area', 'label')
        
        serializer = ParkingCellSerializer(cells, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """Get available parking cells"""
        cells = ParkingCell.objects.filter(status='available').order_by('area', 'label')
        serializer = ParkingCellSerializer(cells, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def allocate(self, request, pk=None):
        """Allocate a parking cell to a vehicle"""
        cell = self.get_object()
        vehicle_id = request.data.get('vehicle_id')
        
        if not vehicle_id:
            return Response(
                {'error': 'vehicle_id required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from .models import Vehicle
            vehicle = Vehicle.objects.get(id=vehicle_id)
            cell.vehicle = vehicle
            cell.status = 'reserved'
            cell.save()
            serializer = ParkingCellSerializer(cell)
            return Response(serializer.data)
        except Vehicle.DoesNotExist:
            return Response(
                {'error': 'Vehicle not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class VehicleEntryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for vehicle entries
    """
    queryset = VehicleEntry.objects.all().select_related('vehicle')
    serializer_class = VehicleEntrySerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['vehicle__reg_no', 'area', 'loading_gate']
    ordering_fields = ['gate_entry_time', 'created_at']
    ordering = ['-gate_entry_time']
    
    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get today's vehicle entries"""
        from django.utils import timezone
        from datetime import timedelta
        
        today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow = today + timedelta(days=1)
        
        entries = VehicleEntry.objects.filter(
            gate_entry_time__gte=today,
            gate_entry_time__lt=tomorrow
        ).select_related('vehicle')
        serializer = VehicleEntrySerializer(entries, many=True)
        return Response(serializer.data)


class SystemAlertViewSet(viewsets.ModelViewSet):
    """
    API endpoint for system alerts
    """
    queryset = SystemAlert.objects.all().select_related('vehicle')
    serializer_class = SystemAlertSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['level', 'message', 'vehicle__reg_no']
    ordering_fields = ['level', 'created_at']
    ordering = ['-created_at']
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get unresolved alerts"""
        alerts = SystemAlert.objects.filter(is_resolved=False).select_related('vehicle')
        serializer = SystemAlertSerializer(alerts, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        """Resolve an alert"""
        from django.utils import timezone
        alert = self.get_object()
        alert.is_resolved = True
        alert.resolved_at = timezone.now()
        alert.save()
        serializer = SystemAlertSerializer(alert)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def resolve_all(self, request):
        """Resolve all active alerts"""
        from django.utils import timezone
        updated = SystemAlert.objects.filter(is_resolved=False).update(
            is_resolved=True,
            resolved_at=timezone.now()
        )
        return Response({'resolved_count': updated})


class TurnaroundTimeSparklineViewSet(viewsets.ModelViewSet):
    """
    API endpoint for turnaround time sparkline data
    """
    queryset = TurnaroundTimeSparkline.objects.all().order_by('-timestamp')
    serializer_class = TurnaroundTimeSparklineSerializer
    ordering = ['-timestamp']
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent turnaround time data (last 20 entries)"""
        data = TurnaroundTimeSparkline.objects.all().order_by('-timestamp')[:20]
        serializer = TurnaroundTimeSparklineSerializer(data, many=True)
        return Response(serializer.data)
