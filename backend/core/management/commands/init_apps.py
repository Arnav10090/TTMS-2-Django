from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.contrib.auth.models import User
from core.utils import get_enabled_apps


class Command(BaseCommand):
    help = 'Initialize apps and create sample data'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--create-superuser',
            action='store_true',
            help='Create a superuser for admin access',
        )
        parser.add_argument(
            '--app',
            type=str,
            help='Initialize a specific app (ttms or ptms)',
        )
        parser.add_argument(
            '--sample-data',
            action='store_true',
            help='Create sample data for enabled apps',
        )
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('APP INITIALIZATION'))
        self.stdout.write(self.style.SUCCESS('='*60 + '\n'))
        
        enabled_apps = get_enabled_apps()
        
        if not enabled_apps:
            self.stdout.write(self.style.WARNING('No apps are enabled!'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'Enabled apps: {", ".join(enabled_apps)}'))
        self.stdout.write('')
        
        if options['create_superuser']:
            self.create_superuser()
        
        if options['sample_data']:
            self.create_sample_data(enabled_apps)
        
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(self.style.SUCCESS('Initialization completed!'))
        self.stdout.write(self.style.SUCCESS('='*60 + '\n'))
    
    def create_superuser(self):
        """Create a superuser if it doesn't exist"""
        if User.objects.filter(username='admin').exists():
            self.stdout.write(self.style.WARNING('Superuser "admin" already exists'))
            return
        
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        self.stdout.write(self.style.SUCCESS('✓ Superuser "admin" created (password: admin123)'))
        self.stdout.write('')
    
    def create_sample_data(self, enabled_apps):
        """Create sample data for enabled apps"""
        self.stdout.write(self.style.SUCCESS('Creating sample data...\n'))
        
        if 'ttms' in enabled_apps:
            self.create_ttms_sample_data()
        
        if 'ptms' in enabled_apps:
            self.create_ptms_sample_data()
    
    def create_ttms_sample_data(self):
        """Create sample TTMS data"""
        from ttms.models import Vehicle, VehicleStage, KPIMetrics, ParkingCell
        
        self.stdout.write('Creating TTMS sample data...')
        
        if Vehicle.objects.exists():
            self.stdout.write(self.style.WARNING('  Sample vehicles already exist, skipping...'))
            return
        
        # Create KPI Metrics
        kpi = KPIMetrics.objects.create(
            capacity_utilization=75,
            plant_capacity=120,
            trucks_inside=90,
            capacity_trend_direction='up',
            capacity_trend_percentage=2.5,
            turnaround_avg_day=45,
            turnaround_avg_cum=48,
            turnaround_last_year=52,
            turnaround_trend_direction='down',
            turnaround_trend_percentage=-3.2,
            turnaround_performance_color='green',
            vehicles_in_day=45,
            vehicles_out_day=42,
            vehicles_in_cum=285,
            vehicles_out_cum=280,
            vehicles_trend_direction='up',
            vehicles_trend_percentage=1.8,
            vehicles_target=150,
            dispatch_today=85,
            dispatch_cum_month=2000,
            dispatch_target_day=120,
            dispatch_trend_direction='up',
            dispatch_trend_percentage=4.2,
        )
        self.stdout.write(self.style.SUCCESS('  ✓ KPI Metrics created'))
        
        # Create sample vehicles
        vehicle1 = Vehicle.objects.create(
            reg_no='TN01AB1234',
            rfid_no='RFID001',
            tare_weight=5000,
            weight_after_loading=15000,
            progress=75,
            turnaround_time=45,
        )
        
        vehicle2 = Vehicle.objects.create(
            reg_no='TN02CD5678',
            rfid_no='RFID002',
            tare_weight=4800,
            weight_after_loading=14500,
            progress=50,
            turnaround_time=38,
        )
        self.stdout.write(self.style.SUCCESS(f'  ✓ {Vehicle.objects.count()} Sample vehicles created'))
        
        # Create parking cells
        for area in ['AREA-1', 'AREA-2']:
            for i in range(1, 6):
                ParkingCell.objects.create(
                    area=area,
                    label=f'Cell-{i}',
                    status='available' if i > 3 else 'occupied',
                )
        self.stdout.write(self.style.SUCCESS(f'  ✓ {ParkingCell.objects.count()} Parking cells created'))
    
    def create_ptms_sample_data(self):
        """Create sample PTMS data"""
        from ptms.models import Project, Task
        from django.contrib.auth.models import User
        
        self.stdout.write('Creating PTMS sample data...')
        
        if Project.objects.exists():
            self.stdout.write(self.style.WARNING('  Sample projects already exist, skipping...'))
            return
        
        admin_user = User.objects.first()
        
        # Create sample projects
        project1 = Project.objects.create(
            name='Q4 Logistics Optimization',
            description='Optimize logistics processes for Q4 peak season',
            status='active',
            created_by=admin_user,
        )
        
        project2 = Project.objects.create(
            name='Fleet Maintenance Program',
            description='Regular maintenance schedule for fleet vehicles',
            status='active',
            created_by=admin_user,
        )
        self.stdout.write(self.style.SUCCESS(f'  ✓ {Project.objects.count()} Sample projects created'))
        
        # Create sample tasks
        for project in [project1, project2]:
            Task.objects.create(
                project=project,
                title='Planning Phase',
                description='Complete project planning and requirements gathering',
                status='completed',
                priority='high',
                assigned_to=admin_user,
            )
            Task.objects.create(
                project=project,
                title='Implementation',
                description='Implement project requirements',
                status='in_progress',
                priority='high',
                assigned_to=admin_user,
            )
            Task.objects.create(
                project=project,
                title='Testing & Deployment',
                description='Test and deploy the solution',
                status='pending',
                priority='medium',
            )
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ {Task.objects.count()} Sample tasks created'))
