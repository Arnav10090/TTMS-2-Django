from django.contrib import admin
from .models import (
    KPIMetrics, Vehicle, VehicleStage, ParkingCell,
    VehicleEntry, SystemAlert, TurnaroundTimeSparkline
)


@admin.register(KPIMetrics)
class KPIMetricsAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at', 'updated_at']
    list_display = [
        'capacity_utilization', 'turnaround_avg_day',
        'vehicles_in_day', 'dispatch_today', 'updated_at'
    ]
    fieldsets = (
        ('Capacity', {
            'fields': (
                'capacity_utilization', 'plant_capacity', 'trucks_inside',
                'capacity_trend_direction', 'capacity_trend_percentage'
            )
        }),
        ('Turnaround', {
            'fields': (
                'turnaround_avg_day', 'turnaround_avg_cum', 'turnaround_last_year',
                'turnaround_trend_direction', 'turnaround_trend_percentage',
                'turnaround_performance_color'
            )
        }),
        ('Vehicles', {
            'fields': (
                'vehicles_in_day', 'vehicles_out_day', 'vehicles_in_cum', 'vehicles_out_cum',
                'vehicles_trend_direction', 'vehicles_trend_percentage', 'vehicles_target'
            )
        }),
        ('Dispatch', {
            'fields': (
                'dispatch_today', 'dispatch_cum_month', 'dispatch_target_day',
                'dispatch_trend_direction', 'dispatch_trend_percentage'
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at', 'updated_at', 'timestamp']
    list_display = ['reg_no', 'rfid_no', 'progress', 'turnaround_time', 'timestamp']
    list_filter = ['progress', 'timestamp']
    search_fields = ['reg_no', 'rfid_no']
    fieldsets = (
        ('Vehicle Information', {
            'fields': ('reg_no', 'rfid_no')
        }),
        ('Weight Data', {
            'fields': ('tare_weight', 'weight_after_loading')
        }),
        ('Progress', {
            'fields': ('progress', 'turnaround_time')
        }),
        ('Timestamps', {
            'fields': ('timestamp', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(VehicleStage)
class VehicleStageAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at', 'updated_at']
    list_display = ['vehicle', 'stage', 'state', 'wait_time', 'standard_time']
    list_filter = ['stage', 'state']
    search_fields = ['vehicle__reg_no']
    fieldsets = (
        ('Stage Information', {
            'fields': ('vehicle', 'stage', 'state')
        }),
        ('Timing', {
            'fields': ('wait_time', 'standard_time')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ParkingCell)
class ParkingCellAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at', 'updated_at']
    list_display = ['area', 'label', 'status', 'vehicle', 'updated_at']
    list_filter = ['area', 'status']
    search_fields = ['label', 'vehicle__reg_no']
    fieldsets = (
        ('Location', {
            'fields': ('area', 'label')
        }),
        ('Status', {
            'fields': ('status', 'vehicle')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(VehicleEntry)
class VehicleEntryAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at', 'updated_at']
    list_display = ['vehicle', 'gate_entry_time', 'area', 'loading_gate']
    list_filter = ['area', 'gate_entry_time']
    search_fields = ['vehicle__reg_no']
    fieldsets = (
        ('Vehicle', {
            'fields': ('vehicle',)
        }),
        ('Entry Details', {
            'fields': ('gate_entry_time', 'area', 'position', 'loading_gate')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SystemAlert)
class SystemAlertAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at', 'resolved_at']
    list_display = ['level', 'message', 'vehicle', 'is_resolved', 'created_at']
    list_filter = ['level', 'is_resolved', 'created_at']
    search_fields = ['message', 'vehicle__reg_no']
    fieldsets = (
        ('Alert', {
            'fields': ('level', 'message', 'vehicle')
        }),
        ('Resolution', {
            'fields': ('is_resolved', 'resolved_at')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(TurnaroundTimeSparkline)
class TurnaroundTimeSparklineAdmin(admin.ModelAdmin):
    readonly_fields = ['timestamp']
    list_display = ['value', 'timestamp']
    list_filter = ['timestamp']
    ordering = ['-timestamp']
