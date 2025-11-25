#!/usr/bin/env python
"""
Script to load sample data into TTMS database.
Run from backend directory: python load_sample_data_script.py
"""

import os
import sys
import django
import json

# Setup Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings_ttms')

# Setup Django
django.setup()

from ttms.models import KPIMetrics, Vehicle, VehicleStage, ParkingCell, TurnaroundTimeSparkline
from django.contrib.auth.models import User
from django.utils import timezone

def load_fixtures_from_file(fixture_path):
    """Load fixtures from JSON file"""
    with open(fixture_path, 'r') as f:
        fixtures = json.load(f)
    return fixtures

def create_kpi_data():
    """Create or update KPI metrics"""
    # Clear existing KPI data
    KPIMetrics.objects.all().delete()
    
    kpi = KPIMetrics.objects.create(
        capacity_utilization=82,
        plant_capacity=120,
        trucks_inside=98,
        capacity_trend_direction='up',
        capacity_trend_percentage=8.5,
        turnaround_avg_day=45,
        turnaround_avg_cum=42,
        turnaround_last_year=52,
        turnaround_trend_direction='down',
        turnaround_trend_percentage=-13.5,
        turnaround_performance_color='green',
        vehicles_in_day=38,
        vehicles_out_day=35,
        vehicles_in_cum=285,
        vehicles_out_cum=280,
        vehicles_trend_direction='up',
        vehicles_trend_percentage=5.2,
        vehicles_target=150,
        dispatch_today=35,
        dispatch_cum_month=685,
        dispatch_target_day=120,
        dispatch_trend_direction='up',
        dispatch_trend_percentage=12.3,
    )
    print(f"✓ Created KPI Metrics record")
    return kpi

def create_vehicles_data():
    """Create sample vehicle data"""
    vehicles_data = [
        {
            'reg_no': 'TN01AB1234',
            'rfid_no': 'RFID001',
            'tare_weight': 5000,
            'weight_after_loading': 12500,
            'progress': 80,
            'turnaround_time': 42,
        },
        {
            'reg_no': 'TN02CD5678',
            'rfid_no': 'RFID002',
            'tare_weight': 4800,
            'weight_after_loading': 11200,
            'progress': 100,
            'turnaround_time': 38,
        },
        {
            'reg_no': 'TN03EF9012',
            'rfid_no': 'RFID003',
            'tare_weight': 5100,
            'weight_after_loading': 13000,
            'progress': 45,
            'turnaround_time': 28,
        },
        {
            'reg_no': 'TN04GH3456',
            'rfid_no': 'RFID004',
            'tare_weight': 4900,
            'weight_after_loading': 10800,
            'progress': 60,
            'turnaround_time': 35,
        },
        {
            'reg_no': 'TN05IJ7890',
            'rfid_no': 'RFID005',
            'tare_weight': 5200,
            'weight_after_loading': 12800,
            'progress': 25,
            'turnaround_time': 32,
        },
    ]
    
    vehicles = []
    for data in vehicles_data:
        vehicle, created = Vehicle.objects.get_or_create(
            reg_no=data['reg_no'],
            defaults={
                'rfid_no': data['rfid_no'],
                'tare_weight': data['tare_weight'],
                'weight_after_loading': data['weight_after_loading'],
                'progress': data['progress'],
                'turnaround_time': data['turnaround_time'],
            }
        )
        if created:
            print(f"✓ Created Vehicle: {vehicle.reg_no}")
        else:
            print(f"→ Vehicle already exists: {vehicle.reg_no}")
        vehicles.append(vehicle)
    
    return vehicles

def create_vehicle_stages(vehicles):
    """Create vehicle stages for each vehicle"""
    stages_config = [
        ('gateEntry', 'completed'),
        ('tareWeighing', 'completed'),
        ('loading', 'active'),
        ('postLoadingWeighing', 'pending'),
        ('gateExit', 'pending'),
    ]
    
    for vehicle in vehicles:
        for stage_name, state in stages_config:
            stage, created = VehicleStage.objects.get_or_create(
                vehicle=vehicle,
                stage=stage_name,
                defaults={
                    'state': state,
                    'wait_time': 10,
                    'standard_time': 30,
                }
            )
            if created:
                print(f"✓ Created Stage: {vehicle.reg_no} - {stage_name}")

def create_parking_cells():
    """Create parking cell grid"""
    areas = ['AREA-1', 'AREA-2']
    cells_per_area = 10
    
    created_count = 0
    for area in areas:
        for i in range(1, cells_per_area + 1):
            cell, created = ParkingCell.objects.get_or_create(
                area=area,
                label=f'P{i:02d}',
                defaults={
                    'status': 'available' if i % 3 != 0 else 'occupied',
                }
            )
            if created:
                created_count += 1
    
    print(f"✓ Created/Updated {created_count} Parking Cells")

def create_sparkline_data():
    """Create turnaround time sparkline data"""
    TurnaroundTimeSparkline.objects.all().delete()
    
    values = [42, 45, 40, 43, 41, 44, 39, 42, 45, 46, 43, 41, 40, 38, 42]
    
    for value in values:
        TurnaroundTimeSparkline.objects.create(value=value)
    
    print(f"✓ Created {len(values)} Sparkline data points")

def main():
    """Main function to load all sample data"""
    print("\n" + "="*50)
    print("Loading TTMS Sample Data")
    print("="*50 + "\n")
    
    try:
        # Load KPI data
        create_kpi_data()
        
        # Load vehicle data
        vehicles = create_vehicles_data()
        
        # Load vehicle stages
        create_vehicle_stages(vehicles)
        
        # Load parking cells
        create_parking_cells()
        
        # Load sparkline data
        create_sparkline_data()
        
        print("\n" + "="*50)
        print("✓ Sample data loaded successfully!")
        print("="*50 + "\n")
        
    except Exception as e:
        print(f"\n✗ Error loading sample data: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
