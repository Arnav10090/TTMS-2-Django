# Django Project Structure - TTMS & PTMS Separation

## Overview

This Django project has been restructured to support two independent applications:
- **TTMS** (Truck Turnaround Time Monitoring System)
- **PTMS** (Project & Task Management System)

Both apps exist within a single Django project with a shared authentication system and utilities, but with completely separate business logic, models, and database tables.

## Project Architecture

```
backend/
├── core/                          # Project configuration and shared utilities
│   ├── auth/                      # Shared authentication modules
│   │   ├��─ backends.py            # Custom auth backends
│   │   └── permissions.py         # Custom permission classes
│   ├── utils/                     # Shared utilities
│   │   ├── helpers.py             # App toggle helpers
│   │   ├── pagination.py          # Standard pagination
│   │   └── responses.py           # Response formatting
│   ├── management/commands/       # Management commands
│   │   ├── app_status.py          # Check app status
│   │   └── init_apps.py           # Initialize apps and sample data
│   ├── middleware.py              # Custom middleware
│   ├── settings.py                # Django settings with app toggles
│   ├── urls.py                    # Dynamic URL configuration
│   └── wsgi.py                    # WSGI application
│
├── ttms/                          # Truck Turnaround Time Monitoring System
│   ├── migrations/                # Database migrations (auto-created)
│   ├── admin.py                   # Django admin configuration
│   ├── apps.py                    # App configuration
│   ├── models.py                  # TTMS models (tables prefixed with ttms_)
│   ├── serializers.py             # DRF serializers
│   ├── views.py                   # API views and viewsets
│   ├── urls.py                    # URL routing
│   └── __init__.py
│
├── ptms/                          # Project & Task Management System
│   ├── migrations/                # Database migrations (auto-created)
│   ├── admin.py                   # Django admin configuration
│   ├── apps.py                    # App configuration
│   ├── models.py                  # PTMS models (tables prefixed with ptms_)
│   ├── serializers.py             # DRF serializers
│   ├── views.py                   # API views and viewsets
│   ├── urls.py                    # URL routing
│   └── __init__.py
│
├── api/                           # Legacy API app (preserved for backward compatibility)
│   ├── ...                        # Existing files
│   └── urls.py
│
└── manage.py                      # Django management script
```

## Database Schema

Django automatically prefixes tables by app name:

### TTMS Tables (ttms_*)
- `ttms_vehicle` - Vehicle information
- `ttms_vehiclestage` - Vehicle processing stages
- `ttms_parkingcell` - Parking cell management
- `ttms_vehicleentry` - Vehicle entry records
- `ttms_systemalert` - System alerts
- `ttms_turnaroundtimesparkline` - Historical turnaround data
- `ttms_kpimetrics` - KPI metrics data

### PTMS Tables (ptms_*)
- `ptms_project` - Project information
- `ptms_task` - Task management

### Shared Tables
- `auth_user` - User authentication (shared across both apps)
- `auth_group` - User groups and permissions

## API Endpoints

### TTMS Endpoints (when enabled)
```
GET/POST   /api/ttms/kpi/                    - KPI metrics
GET/POST   /api/ttms/vehicles/               - Vehicles
GET/POST   /api/ttms/vehicle-stages/         - Vehicle stages
GET/POST   /api/ttms/parking-cells/          - Parking cells
GET/POST   /api/ttms/vehicle-entries/        - Vehicle entries
GET/POST   /api/ttms/alerts/                 - System alerts
GET/POST   /api/ttms/sparkline/              - Turnaround time sparkline
```

### PTMS Endpoints (when enabled)
```
GET/POST   /api/ptms/projects/               - Projects
GET/POST   /api/ptms/tasks/                  - Tasks
```

### Status Endpoint (always available)
```
GET        /api/status/                      - Check enabled apps and their config
```

## Configuration

### Environment Variables

Control which apps are enabled/disabled via environment variables:

```bash
# Enable/disable TTMS (default: True)
ENABLE_TTMS=True

# Enable/disable PTMS (default: True)
ENABLE_PTMS=True

# Database configuration
DB_ENGINE=django.db.backends.postgresql
DB_NAME=ttr_dashboard
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# Django settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS configuration
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

### Settings Configuration

In `settings.py`:

```python
# Enable/disable apps (controlled by environment variables)
ENABLE_TTMS = os.getenv('ENABLE_TTMS', 'True') == 'True'
ENABLE_PTMS = os.getenv('ENABLE_PTMS', 'True') == 'True'

# App configuration objects
TTMS_CONFIG = {
    'enabled': ENABLE_TTMS,
    'name': 'Truck Turnaround Time Monitoring System',
    'description': '...',
    'prefix': 'ttms',
}

PTMS_CONFIG = {
    'enabled': ENABLE_PTMS,
    'name': 'Project & Task Management System',
    'description': '...',
    'prefix': 'ptms',
}
```

## Usage

### 1. Check App Status

```bash
python manage.py app_status
```

Output:
```
============================================================
APP STATUS REPORT
============================================================

✓ TTMS is ENABLED
  Name: Truck Turnaround Time Monitoring System
  Description: System for monitoring and managing truck turnaround times
  Prefix: /api/ttms/

✓ PTMS is ENABLED
  Name: Project & Task Management System
  Description: System for managing projects and tasks
  Prefix: /api/ptms/

Enabled apps: ttms, ptms
============================================================
```

### 2. Initialize Apps and Create Sample Data

```bash
# Check enabled apps
python manage.py init_apps

# Create superuser for admin access
python manage.py init_apps --create-superuser

# Create sample data for enabled apps
python manage.py init_apps --sample-data

# Both superuser and sample data
python manage.py init_apps --create-superuser --sample-data
```

### 3. Run Migrations

```bash
# Create migrations for new models
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate

# Apply migrations for specific app
python manage.py migrate ttms
python manage.py migrate ptms
```

### 4. Disable/Enable Apps for Deployment

**Deploy only TTMS:**
```bash
export ENABLE_TTMS=True
export ENABLE_PTMS=False
python manage.py runserver
```

**Deploy only PTMS:**
```bash
export ENABLE_TTMS=False
export ENABLE_PTMS=True
python manage.py runserver
```

**Deploy both (default):**
```bash
export ENABLE_TTMS=True
export ENABLE_PTMS=True
python manage.py runserver
```

## Shared Components

### Authentication
- Uses Django's built-in `User` model (shared across both apps)
- Both apps share the same authentication system
- Custom authentication backend supports username or email login

### Authorization
- Uses Django's built-in permission system
- Both apps share the same user groups and permissions
- Custom permission classes for role-based access

### Utilities
Available in `core.utils`:
- `is_app_enabled(app_name)` - Check if an app is enabled
- `get_enabled_apps()` - Get list of enabled apps
- `get_app_config(app_name)` - Get app configuration
- `StandardPagination` - Standard pagination for API
- `success_response()` - Format success responses
- `error_response()` - Format error responses

### Middleware
- `RequestLoggingMiddleware` - Logs all incoming requests
- `AppAvailabilityMiddleware` - Checks if requested app is enabled

## Development Workflow

### Adding a New Endpoint to TTMS

1. Add model in `ttms/models.py`
2. Register in `ttms/admin.py`
3. Create serializer in `ttms/serializers.py`
4. Create viewset in `ttms/views.py`
5. Register in `ttms/urls.py`

Example:
```python
# ttms/models.py
class NewModel(models.Model):
    # ... fields

# ttms/serializers.py
class NewModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewModel
        fields = '__all__'

# ttms/views.py
class NewModelViewSet(viewsets.ModelViewSet):
    queryset = NewModel.objects.all()
    serializer_class = NewModelSerializer

# ttms/urls.py
router.register(r'newmodels', NewModelViewSet, basename='newmodel')
```

### Adding a New Model to PTMS

Same process as TTMS, but using `ptms/` directories.

## Database Considerations

### Table Prefixing
Django automatically prefixes table names with the app name:
- TTMS: `ttms_*`
- PTMS: `ptms_*`
- Shared: `auth_*`, `django_*`

### Migrations
Each app maintains its own migrations folder. This allows:
- Independent migration history
- Selective deployment of app changes
- Better version control and auditing

### Shared Data
The `auth_user` table is shared between both apps. Use Django's User model for any user-related fields.

## Testing

Both apps can be tested independently or together:

```bash
# Test all apps
python manage.py test

# Test specific app
python manage.py test ttms
python manage.py test ptms

# Test with verbosity
python manage.py test --verbosity=2
```

## Deployment Strategies

### Strategy 1: Single Deployment (Both Apps)
- Deploy entire project with `ENABLE_TTMS=True` and `ENABLE_PTMS=True`
- Both apps share same database and server

### Strategy 2: Selective Deployment
- Deploy to Server A: `ENABLE_TTMS=True, ENABLE_PTMS=False`
- Deploy to Server B: `ENABLE_TTMS=False, ENABLE_PTMS=True`
- Different servers, shared database
- Route requests based on domain/path

### Strategy 3: Future Separation
- When completely independent is needed:
  1. Export PTMS models and data
  2. Create separate Django project for PTMS
  3. Migrate to separate database
  4. Update frontend routing

## Troubleshooting

### App not appearing in admin
- Check if app is in `INSTALLED_APPS` in settings.py
- Ensure app `AppConfig` is registered correctly
- Run migrations: `python manage.py migrate`

### 404 on app endpoint
- Check if app is enabled: `python manage.py app_status`
- Verify URL is correct: `/api/{app_name}/...`
- Check middleware is not blocking request

### Database errors after enabling new app
- Run migrations: `python manage.py migrate`
- Check if app models reference non-existent fields
- Verify database permissions

## Future Enhancements

1. **API Versioning**: Add version numbers to endpoints (`/api/v1/ttms/`)
2. **Rate Limiting**: Implement per-app rate limiting
3. **Monitoring**: Add app-specific monitoring and metrics
4. **Separate Databases**: Migrate to separate databases per app
5. **Service Separation**: Convert to microservices if needed
