from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class KPIMetrics(models.Model):
    """Stores KPI metrics data"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Capacity KPI
    capacity_utilization = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0,
        help_text="Capacity utilization percentage"
    )
    plant_capacity = models.IntegerField(
        default=120,
        help_text="Total plant capacity"
    )
    trucks_inside = models.IntegerField(
        default=0,
        help_text="Number of trucks currently inside"
    )
    capacity_trend_direction = models.CharField(
        max_length=4,
        choices=[('up', 'Up'), ('down', 'Down')],
        default='up'
    )
    capacity_trend_percentage = models.FloatField(default=0.0)
    
    # Turnaround KPI
    turnaround_avg_day = models.IntegerField(
        default=0,
        help_text="Average turnaround time for the day in minutes"
    )
    turnaround_avg_cum = models.IntegerField(
        default=0,
        help_text="Cumulative average turnaround time in minutes"
    )
    turnaround_last_year = models.IntegerField(
        default=0,
        help_text="Last year's turnaround time in minutes"
    )
    turnaround_trend_direction = models.CharField(
        max_length=4,
        choices=[('up', 'Up'), ('down', 'Down')],
        default='down'
    )
    turnaround_trend_percentage = models.FloatField(default=0.0)
    turnaround_performance_color = models.CharField(
        max_length=10,
        choices=[('green', 'Green'), ('yellow', 'Yellow'), ('red', 'Red'), ('blue', 'Blue')],
        default='blue'
    )
    
    # Vehicles KPI
    vehicles_in_day = models.IntegerField(default=0)
    vehicles_out_day = models.IntegerField(default=0)
    vehicles_in_cum = models.IntegerField(default=0)
    vehicles_out_cum = models.IntegerField(default=0)
    vehicles_trend_direction = models.CharField(
        max_length=4,
        choices=[('up', 'Up'), ('down', 'Down')],
        default='up'
    )
    vehicles_trend_percentage = models.FloatField(default=0.0)
    vehicles_target = models.IntegerField(default=150)
    
    # Dispatch KPI
    dispatch_today = models.IntegerField(default=0)
    dispatch_cum_month = models.IntegerField(default=0)
    dispatch_target_day = models.IntegerField(default=120)
    dispatch_trend_direction = models.CharField(
        max_length=4,
        choices=[('up', 'Up'), ('down', 'Down')],
        default='up'
    )
    dispatch_trend_percentage = models.FloatField(default=0.0)
    
    class Meta:
        verbose_name_plural = "KPI Metrics"
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"KPI Metrics - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class Vehicle(models.Model):
    """Represents a vehicle in the system"""
    reg_no = models.CharField(max_length=50, unique=True)
    rfid_no = models.CharField(max_length=100, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Weight information
    tare_weight = models.IntegerField(
        default=0,
        help_text="Tare weight in kg"
    )
    weight_after_loading = models.IntegerField(
        default=0,
        help_text="Weight after loading in kg"
    )
    
    # Process information
    progress = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0,
        help_text="Process progress percentage"
    )
    turnaround_time = models.IntegerField(
        default=0,
        help_text="Turnaround time in minutes"
    )
    timestamp = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"Vehicle {self.reg_no}"


class VehicleStage(models.Model):
    """Represents a stage in the vehicle's journey"""
    STAGE_CHOICES = [
        ('gateEntry', 'Gate Entry'),
        ('tareWeighing', 'Tare Weighing'),
        ('loading', 'Loading'),
        ('postLoadingWeighing', 'Post Loading Weighing'),
        ('gateExit', 'Gate Exit'),
    ]
    
    STATE_CHOICES = [
        ('completed', 'Completed'),
        ('active', 'Active'),
        ('pending', 'Pending'),
    ]
    
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='stages')
    stage = models.CharField(max_length=50, choices=STAGE_CHOICES)
    state = models.CharField(max_length=20, choices=STATE_CHOICES)
    wait_time = models.IntegerField(
        default=0,
        help_text="Wait time in minutes"
    )
    standard_time = models.IntegerField(
        default=30,
        help_text="Standard time for this stage in minutes"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('vehicle', 'stage')
        ordering = ['vehicle', 'stage']
    
    def __str__(self):
        return f"{self.vehicle.reg_no} - {self.get_stage_display()}"


class ParkingCell(models.Model):
    """Represents a parking cell/slot"""
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('reserved', 'Reserved'),
    ]
    
    AREA_CHOICES = [
        ('AREA-1', 'Area 1'),
        ('AREA-2', 'Area 2'),
    ]
    
    area = models.CharField(max_length=10, choices=AREA_CHOICES)
    label = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='parking_assignments'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('area', 'label')
        ordering = ['area', 'label']
    
    def __str__(self):
        return f"{self.area} - {self.label} ({self.status})"


class VehicleEntry(models.Model):
    """Represents a vehicle entry in the scheduling system"""
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='entries'
    )
    gate_entry_time = models.DateTimeField()
    area = models.CharField(max_length=20, default='AREA-1')
    position = models.CharField(max_length=200, blank=True)
    loading_gate = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-gate_entry_time']
    
    def __str__(self):
        return f"Entry - {self.vehicle.reg_no} at {self.gate_entry_time}"


class SystemAlert(models.Model):
    """Represents system alerts"""
    LEVEL_CHOICES = [
        ('critical', 'Critical'),
        ('warning', 'Warning'),
        ('info', 'Info'),
        ('success', 'Success'),
    ]
    
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    message = models.TextField()
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='alerts'
    )
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"[{self.level.upper()}] {self.message}"


class TurnaroundTimeSparkline(models.Model):
    """Stores historical turnaround time data for sparkline charts"""
    timestamp = models.DateTimeField(auto_now_add=True)
    value = models.IntegerField(help_text="Turnaround time in minutes")
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"Sparkline - {self.value} min at {self.timestamp}"
