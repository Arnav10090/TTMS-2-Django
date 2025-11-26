# Django Backend for TTR Dashboard

A Django REST API backend for the TTR (Turnaround Time) Dashboard built with Django REST Framework and PostgreSQL.

## Features

- **KPI Metrics Management**: Track capacity, turnaround time, vehicle, and dispatch metrics
- **Vehicle Tracking**: Complete vehicle lifecycle management with multiple processing stages
- **Parking Management**: Allocate and track parking spaces
- **Scheduling**: Vehicle entry scheduling and management
- **Alerts System**: System alerts and notifications
- **RESTful API**: Full REST API using Django REST Framework

## Requirements

- Python 3.8+
- PostgreSQL 12+
- pip

## Installation

### 1. Clone/Setup the Project

```bash
cd backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the `backend/` directory based on `.env.example`:

```bash
cp .env.example .env
```

Update `.env` with your PostgreSQL credentials:

```
DEBUG=True
SECRET_KEY=your-secret-key-here

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=ttr_dashboard
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# CORS - Update with your frontend URL
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

### 5. Setup PostgreSQL Database

Create a PostgreSQL database:

```bash
# Using psql
createdb ttr_dashboard
```

Or using PostgreSQL GUI tools like pgAdmin.

### 6. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser

```bash
python manage.py createsuperuser
```

### 8. Run Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/ttms/`

## API Endpoints

Base: `http://localhost:8000/api/ttms/`

### Auth (JWT)
- `POST /api/ttms/auth/login/` – Obtain access/refresh tokens
- `POST /api/ttms/auth/refresh/` – Refresh access token
- `POST /api/ttms/auth/verify/` – Verify token
- `GET /api/ttms/auth/users/` – User list (if permissions allow)

### KPI Metrics
- `GET /api/ttms/kpi/` – List all KPI records
- `GET /api/ttms/kpi/latest/` – Latest KPI metrics
- `POST /api/ttms/kpi/` – Create KPI record
- `POST /api/ttms/kpi/create_or_update/` – Create or update latest KPI

### Vehicles
- `GET /api/ttms/vehicles/` – List vehicles (search/order supported)
- `GET /api/ttms/vehicles/{id}/` – Vehicle detail with stages
- `GET /api/ttms/vehicles/active/` – Vehicles in progress
- `GET /api/ttms/vehicles/completed/` – Completed vehicles
- `POST /api/ttms/vehicles/` – Create vehicle
- `POST /api/ttms/vehicles/{id}/update_stage/` – Update a specific stage

### Vehicle Stages
- `GET /api/ttms/vehicle-stages/` – List stages
- `GET /api/ttms/vehicle-stages/by_vehicle/?vehicle_id=1` – Stages for vehicle

### Parking
- `GET /api/ttms/parking-cells/` – List parking cells
- `GET /api/ttms/parking-cells/by_area/?area=AREA-1` – Cells by area
- `GET /api/ttms/parking-cells/available/` – Available spots
- `POST /api/ttms/parking-cells/{id}/allocate/` – Allocate spot to vehicle

### Vehicle Entries
- `GET /api/ttms/vehicle-entries/` – List entries
- `GET /api/ttms/vehicle-entries/today/` – Today’s entries
- `POST /api/ttms/vehicle-entries/` – Create entry

### System Alerts
- `GET /api/ttms/alerts/` – List alerts
- `GET /api/ttms/alerts/active/` – Unresolved alerts
- `POST /api/ttms/alerts/{id}/resolve/` – Resolve alert
- `POST /api/ttms/alerts/resolve_all/` – Resolve all active alerts

### Sparkline Data
- `GET /api/ttms/sparkline/` – List sparkline data
- `GET /api/ttms/sparkline/recent/` – Last 20 entries

### Loading Gates (Scheduling)
- `GET /api/ttms/loading-gates/` – List gates
- `GET /api/ttms/loading-gates/status/` – Summarized status
- `POST /api/ttms/loading-gates/{id}/assign/` – Assign gate to entry
- `POST /api/ttms/loading-gates/{id}/release/` – Release gate

## Database Schema

### KPIMetrics
Stores all KPI data points including capacity, turnaround time, vehicles, and dispatch metrics.

### Vehicle
Represents a vehicle in the system with weight, progress, and turnaround time data.

### VehicleStage
Tracks the state of each processing stage (Gate Entry, Tare Weighing, Loading, Post-Loading Weighing, Gate Exit) for a vehicle.

### ParkingCell
Manages parking area slots with status tracking (available, occupied, reserved).

### VehicleEntry
Records when a vehicle enters the system during scheduling.

### SystemAlert
Stores system alerts with different severity levels (critical, warning, info, success).

### TurnaroundTimeSparkline
Historical turnaround time data for trend visualization.

## Admin Interface

Access Django admin at `http://localhost:8000/admin/` with your superuser credentials.

## Frontend Integration

The frontend expects the KPI endpoint to return data in this format:

```json
{
  "capacity": {
    "utilization": 72,
    "plantCapacity": 120,
    "trucksInside": 86,
    "trend": {"direction": "up", "percentage": 3.2}
  },
  "turnaround": {
    "avgDay": 92,
    "avgCum": 95,
    "lastYear": 102,
    "trend": {"direction": "down", "percentage": 1.4},
    "performanceColor": "yellow",
    "sparkline": [{"v": 85}, {"v": 95}, ...]
  },
  "vehicles": {
    "inDay": 140,
    "outDay": 132,
    "inCum": 1980,
    "outCum": 1968,
    "trend": {"direction": "up", "percentage": 5.1},
    "target": 150
  },
  "dispatch": {
    "today": 88,
    "cumMonth": 1220,
    "targetDay": 120,
    "trend": {"direction": "up", "percentage": 2.3}
  }
}
```

## Deployment

### Using Gunicorn

```bash
pip install gunicorn
gunicorn core.wsgi:application
```

### Production Checklist

1. Set `DEBUG=False` in `.env`
2. Generate a strong `SECRET_KEY`
3. Set appropriate `ALLOWED_HOSTS`
4. Configure PostgreSQL for production
5. Set up proper CORS origins
6. Use environment variables for sensitive data
7. Enable HTTPS
8. Set up proper logging

## Development

### Creating Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Loading Sample Data

Create a management command or use the Django shell:

```bash
python manage.py shell
```

## Testing

Run tests with:

```bash
python manage.py test
```

## Troubleshooting

### Database Connection Error
- Ensure PostgreSQL is running
- Check database credentials in `.env`
- Verify database exists

### CORS Errors
- Add your frontend URL to `CORS_ALLOWED_ORIGINS` in `.env`
- Ensure frontend is making requests to `http://localhost:8000/api/`

### Port Already in Use
- Run on different port: `python manage.py runserver 8001`
- Or kill the process using port 8000

## License

[Your License Here]
