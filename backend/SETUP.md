# Quick Start Guide - Django Backend Setup

## Option 1: Using Docker (Recommended)

### Prerequisites
- Docker and Docker Compose installed

### Steps
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Start PostgreSQL and Django:
   ```bash
   docker-compose up
   ```

3. In another terminal, run migrations:
   ```bash
   docker-compose exec web python manage.py migrate
   ```

4. Create a superuser:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

5. Access the API:
   - API Base: `http://localhost:8000/api/ttms/`
   - Admin: `http://localhost:8000/admin/`

## Option 2: Local Setup (Manual)

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- pip

### Steps

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create `.env` file:
   ```bash
   cp .env.example .env
   ```

5. Update `.env` with your PostgreSQL credentials:
   ```
   DB_NAME=ttr_dashboard
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   ```

6. Create PostgreSQL database:
   ```bash
   # Using psql
   createdb ttr_dashboard
   ```

7. Run migrations:
   ```bash
   python manage.py migrate
   ```

8. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

9. Start development server:
   ```bash
   python manage.py runserver
   ```

10. Access the application:
    - API Base: `http://localhost:8000/api/ttms/`
    - Admin: `http://localhost:8000/admin/`

## Connecting Frontend to Backend

Update your frontend API base URL to `http://localhost:8000/api/ttms/`

If you're using the frontend at `http://localhost:5173`, the CORS settings in `.env` should already include it:
```
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

## Loading Sample Data

You can load sample data using the Django shell:

```bash
python manage.py shell
```

Then execute:

```python
from ttms.models import KPIMetrics, Vehicle, VehicleStage
from datetime import datetime

# Create KPI metrics
kpi = KPIMetrics.objects.create(
    capacity_utilization=72,
    plant_capacity=120,
    trucks_inside=86,
    capacity_trend_direction='up',
    capacity_trend_percentage=3.2,
    turnaround_avg_day=92,
    turnaround_avg_cum=95,
    turnaround_last_year=102,
    turnaround_trend_direction='down',
    turnaround_trend_percentage=1.4,
    turnaround_performance_color='yellow',
    vehicles_in_day=140,
    vehicles_out_day=132,
    vehicles_in_cum=1980,
    vehicles_out_cum=1968,
    vehicles_trend_direction='up',
    vehicles_trend_percentage=5.1,
    vehicles_target=150,
    dispatch_today=88,
    dispatch_cum_month=1220,
    dispatch_target_day=120,
    dispatch_trend_direction='up',
    dispatch_trend_percentage=2.3
)

# Create a sample vehicle
vehicle = Vehicle.objects.create(
    reg_no='MH12-1001',
    rfid_no='RFID-1001',
    tare_weight=2500,
    weight_after_loading=5200,
    progress=45,
    turnaround_time=75
)

# Create stages for the vehicle
stages = ['gateEntry', 'tareWeighing', 'loading', 'postLoadingWeighing', 'gateExit']
for stage in stages:
    VehicleStage.objects.create(
        vehicle=vehicle,
        stage=stage,
        state='pending' if stage != 'gateEntry' else 'completed',
        wait_time=15,
        standard_time=30
    )

print("Sample data created successfully!")
```

## API Endpoints Quick Reference

### Auth (JWT)
```
POST   /api/ttms/auth/login/
POST   /api/ttms/auth/refresh/
POST   /api/ttms/auth/verify/
```

### KPI
```
GET    /api/ttms/kpi/
GET    /api/ttms/kpi/latest/
POST   /api/ttms/kpi/
POST   /api/ttms/kpi/create_or_update/
```

### Vehicles
```
GET    /api/ttms/vehicles/
GET    /api/ttms/vehicles/active/
GET    /api/ttms/vehicles/completed/
POST   /api/ttms/vehicles/
```

### Parking
```
GET    /api/ttms/parking-cells/
GET    /api/ttms/parking-cells/by_area/?area=AREA-1
GET    /api/ttms/parking-cells/available/
POST   /api/ttms/parking-cells/{id}/allocate/
```

### Vehicle Entries
```
GET    /api/ttms/vehicle-entries/
GET    /api/ttms/vehicle-entries/today/
POST   /api/ttms/vehicle-entries/
```

### Alerts
```
GET    /api/ttms/alerts/
GET    /api/ttms/alerts/active/
POST   /api/ttms/alerts/{id}/resolve/
POST   /api/ttms/alerts/resolve_all/
```

## Troubleshooting

### Port 8000 already in use
```bash
python manage.py runserver 8001
```

### Database connection error
- Ensure PostgreSQL is running
- Check credentials in `.env`
- Verify database exists

### CORS errors
- Add your frontend URL to `CORS_ALLOWED_ORIGINS`
- Ensure frontend requests go to `http://localhost:8000/api/`

### Missing dependencies
```bash
pip install -r requirements.txt --upgrade
```

## Next Steps

1. Create migrations: `python manage.py makemigrations`
2. Apply migrations: `python manage.py migrate`
3. Access admin: `http://localhost:8000/admin/`
4. Start making API calls from the frontend

For more details, see [README.md](README.md)
