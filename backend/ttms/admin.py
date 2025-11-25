from django.contrib import admin
from .models import (
    KPIMetrics, Vehicle, VehicleStage, ParkingCell,
    VehicleEntry, SystemAlert, TurnaroundTimeSparkline
)


@admin.register(KPIMetrics)
class KPIMetricsAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'capacity_utilization', 'turnaround_avg_day', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-updated_at',)


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('reg_no', 'rfid_no', 'progress', 'turnaround_time', 'timestamp')
    list_filter = ('timestamp', 'created_at')
    search_fields = ('reg_no', 'rfid_no')
    readonly_fields = ('created_at', 'updated_at', 'timestamp')
    ordering = ('-timestamp',)


@admin.register(VehicleStage)
class VehicleStageAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'stage', 'state', 'wait_time', 'updated_at')
    list_filter = ('stage', 'state', 'updated_at')
    search_fields = ('vehicle__reg_no', 'stage')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('vehicle', 'stage')


@admin.register(ParkingCell)
class ParkingCellAdmin(admin.ModelAdmin):
    list_display = ('area', 'label', 'status', 'vehicle', 'updated_at')
    list_filter = ('area', 'status', 'updated_at')
    search_fields = ('area', 'label', 'vehicle__reg_no')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('area', 'label')


@admin.register(VehicleEntry)
class VehicleEntryAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'gate_entry_time', 'area', 'loading_gate', 'created_at')
    list_filter = ('area', 'gate_entry_time', 'created_at')
    search_fields = ('vehicle__reg_no', 'area', 'loading_gate')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-gate_entry_time',)


@admin.register(SystemAlert)
class SystemAlertAdmin(admin.ModelAdmin):
    list_display = ('level', 'message', 'vehicle', 'is_resolved', 'created_at')
    list_filter = ('level', 'is_resolved', 'created_at')
    search_fields = ('message', 'vehicle__reg_no')
    readonly_fields = ('created_at', 'resolved_at')
    ordering = ('-created_at',)


@admin.register(TurnaroundTimeSparkline)
class TurnaroundTimeSparklineAdmin(admin.ModelAdmin):
    list_display = ('value', 'timestamp')
    list_filter = ('timestamp',)
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)
