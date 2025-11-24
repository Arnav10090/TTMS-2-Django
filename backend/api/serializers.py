from rest_framework import serializers
from .models import (
    KPIMetrics, Vehicle, VehicleStage, ParkingCell,
    VehicleEntry, SystemAlert, TurnaroundTimeSparkline
)


class VehicleStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleStage
        fields = ['id', 'stage', 'state', 'wait_time', 'standard_time']
        read_only_fields = ['id']


class VehicleSerializer(serializers.ModelSerializer):
    stages = VehicleStageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Vehicle
        fields = [
            'id', 'reg_no', 'rfid_no', 'tare_weight', 'weight_after_loading',
            'progress', 'turnaround_time', 'timestamp', 'stages',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'timestamp']


class VehicleCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = [
            'reg_no', 'rfid_no', 'tare_weight', 'weight_after_loading',
            'progress', 'turnaround_time'
        ]


class ParkingCellSerializer(serializers.ModelSerializer):
    vehicle_reg_no = serializers.CharField(source='vehicle.reg_no', read_only=True)
    
    class Meta:
        model = ParkingCell
        fields = [
            'id', 'area', 'label', 'status', 'vehicle', 'vehicle_reg_no',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class VehicleEntrySerializer(serializers.ModelSerializer):
    vehicle_reg_no = serializers.CharField(source='vehicle.reg_no', read_only=True)
    
    class Meta:
        model = VehicleEntry
        fields = [
            'id', 'vehicle', 'vehicle_reg_no', 'gate_entry_time',
            'area', 'position', 'loading_gate', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class SystemAlertSerializer(serializers.ModelSerializer):
    vehicle_reg_no = serializers.CharField(source='vehicle.reg_no', read_only=True)
    
    class Meta:
        model = SystemAlert
        fields = [
            'id', 'level', 'message', 'vehicle', 'vehicle_reg_no',
            'is_resolved', 'created_at', 'resolved_at'
        ]
        read_only_fields = ['id', 'created_at']


class TurnaroundTimeSparklineSerializer(serializers.ModelSerializer):
    class Meta:
        model = TurnaroundTimeSparkline
        fields = ['id', 'timestamp', 'value']
        read_only_fields = ['id', 'timestamp']


class KPIMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = KPIMetrics
        fields = [
            'id',
            'capacity_utilization', 'plant_capacity', 'trucks_inside',
            'capacity_trend_direction', 'capacity_trend_percentage',
            'turnaround_avg_day', 'turnaround_avg_cum', 'turnaround_last_year',
            'turnaround_trend_direction', 'turnaround_trend_percentage',
            'turnaround_performance_color',
            'vehicles_in_day', 'vehicles_out_day', 'vehicles_in_cum', 'vehicles_out_cum',
            'vehicles_trend_direction', 'vehicles_trend_percentage', 'vehicles_target',
            'dispatch_today', 'dispatch_cum_month', 'dispatch_target_day',
            'dispatch_trend_direction', 'dispatch_trend_percentage',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class KPIMetricsDetailSerializer(serializers.Serializer):
    """Serializer to format KPI data according to frontend expectations"""
    capacity = serializers.SerializerMethodField()
    turnaround = serializers.SerializerMethodField()
    vehicles = serializers.SerializerMethodField()
    dispatch = serializers.SerializerMethodField()
    
    def get_capacity(self, obj):
        return {
            'utilization': obj.capacity_utilization,
            'plantCapacity': obj.plant_capacity,
            'trucksInside': obj.trucks_inside,
            'trend': {
                'direction': obj.capacity_trend_direction,
                'percentage': obj.capacity_trend_percentage
            }
        }
    
    def get_turnaround(self, obj):
        sparkline = TurnaroundTimeSparkline.objects.all().order_by('timestamp')[:20]
        return {
            'avgDay': obj.turnaround_avg_day,
            'avgCum': obj.turnaround_avg_cum,
            'lastYear': obj.turnaround_last_year,
            'trend': {
                'direction': obj.turnaround_trend_direction,
                'percentage': obj.turnaround_trend_percentage
            },
            'performanceColor': obj.turnaround_performance_color,
            'sparkline': [{'v': s.value} for s in sparkline]
        }
    
    def get_vehicles(self, obj):
        return {
            'inDay': obj.vehicles_in_day,
            'outDay': obj.vehicles_out_day,
            'inCum': obj.vehicles_in_cum,
            'outCum': obj.vehicles_out_cum,
            'trend': {
                'direction': obj.vehicles_trend_direction,
                'percentage': obj.vehicles_trend_percentage
            },
            'target': obj.vehicles_target
        }
    
    def get_dispatch(self, obj):
        return {
            'today': obj.dispatch_today,
            'cumMonth': obj.dispatch_cum_month,
            'targetDay': obj.dispatch_target_day,
            'trend': {
                'direction': obj.dispatch_trend_direction,
                'percentage': obj.dispatch_trend_percentage
            }
        }
