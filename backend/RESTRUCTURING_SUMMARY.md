# Django Project Restructuring Summary

## What Changed

Your Django project has been successfully restructured to separate TTMS and PTMS into independent applications while maintaining a single Django project. Here's what was done:

## New Directory Structure

### Created
```
backend/
├── ttms/                          # New TTMS app (moved from api)
│   ├── migrations/                # (auto-created)
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── __init__.py
│
├── ptms/                          # New PTMS app (ready for future models)
│   ├── migrations/                # (auto-created)
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── __init__.py
│
├── core/
│   ├── auth/                      # NEW - Shared auth module
│   │   ├── backends.py            # Custom auth backend
│   │   └── permissions.py         # Permission classes
│   ├── utils/                     # NEW - Shared utilities
│   │   ├── __init__.py
│   │   ├── helpers.py             # App toggle helpers
│   │   ├── pagination.py          # Standard pagination
│   │   └── responses.py           # Response formatting
│   ├── management/commands/       # NEW - Management commands
│   │   ├── __init__.py
│   │   ├── app_status.py          # Check app status
│   │   └── init_apps.py           # Initialize apps
│   ├── middleware.py              # NEW - Custom middleware
│   ├── settings.py                # UPDATED - Added toggles and config
│   ├── urls.py                    # UPDATED - Dynamic routing
│   └── wsgi.py
│
├── api/                           # Preserved for backward compatibility
��   └── ...
│
├── APP_STRUCTURE.md               # NEW - Detailed documentation
├── DEPLOYMENT_GUIDE.md            # NEW - Deployment instructions
└── RESTRUCTURING_SUMMARY.md       # NEW - This file
```

## Key Changes

### 1. TTMS App (New)
- **Location**: `backend/ttms/`
- **Models**: All vehicle-related models moved from `api/`
  - `Vehicle`
  - `VehicleStage`
  - `ParkingCell`
  - `VehicleEntry`
  - `SystemAlert`
  - `TurnaroundTimeSparkline`
  - `KPIMetrics`
- **Database prefix**: `ttms_*`
- **API endpoints**: `/api/ttms/*`

### 2. PTMS App (New)
- **Location**: `backend/ptms/`
- **Models**: New models for project management
  - `Project`
  - `Task`
- **Database prefix**: `ptms_*`
- **API endpoints**: `/api/ptms/*`
- Ready for future PTMS-specific models

### 3. Shared Components

#### Core Auth (`core/auth/`)
- `CustomAuthBackend` - Supports username or email login
- Permission classes for authorization
- Shared user authentication across both apps

#### Core Utils (`core/utils/`)
- `is_app_enabled(app_name)` - Check if app is enabled
- `get_enabled_apps()` - Get list of enabled apps
- `StandardPagination` - Consistent pagination
- Response formatting utilities

#### Middleware (`core/middleware.py`)
- `RequestLoggingMiddleware` - Log all requests
- `AppAvailabilityMiddleware` - Check app availability

#### Management Commands (`core/management/commands/`)
- `app_status` - Check status of all apps
- `init_apps` - Initialize apps with sample data

### 4. Settings Configuration

**New additions to `settings.py`:**
```python
# App toggles (controlled by env variables)
ENABLE_TTMS = os.getenv('ENABLE_TTMS', 'True') == 'True'
ENABLE_PTMS = os.getenv('ENABLE_PTMS', 'True') == 'True'

# App configurations
TTMS_CONFIG = {...}
PTMS_CONFIG = {...}

# Authentication backends
AUTHENTICATION_BACKENDS = [
    'core.auth.backends.CustomAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Custom middleware
MIDDLEWARE = [..., 'core.middleware.RequestLoggingMiddleware', ...]

# Logging configuration
LOGGING = {...}
```

### 5. URL Routing

**Updated `core/urls.py`:**
- Dynamic URL registration based on `ENABLE_TTMS` and `ENABLE_PTMS`
- New status endpoint: `/api/status/`
- App-specific namespaces: `ttms` and `ptms`

```python
# Dynamically added based on settings
/api/ttms/     # If ENABLE_TTMS=True
/api/ptms/     # If ENABLE_PTMS=True
/api/status/   # Always available
```

## Migration Path

### For Existing Data
The existing TTMS models have been moved from `api/` to `ttms/`. The database tables remain unchanged:
- Table names have `ttms_` prefix (as they did)
- All existing data is preserved
- No data loss occurs

### Steps After Restructuring

1. **Run migrations** (creates new PTMS tables):
   ```bash
   python manage.py migrate
   ```

2. **Check app status**:
   ```bash
   python manage.py app_status
   ```

3. **Initialize apps** (optional - creates sample data):
   ```bash
   python manage.py init_apps --create-superuser --sample-data
   ```

## Deployment Options

### Option 1: Deploy Both Apps (Default)
```bash
ENABLE_TTMS=True
ENABLE_PTMS=True
```
- All endpoints available: `/api/ttms/*` and `/api/ptms/*`
- Single server deployment
- Shared database, shared auth

### Option 2: Deploy Only TTMS
```bash
ENABLE_TTMS=True
ENABLE_PTMS=False
```
- Only TTMS endpoints available: `/api/ttms/*`
- PTMS endpoints return 404

### Option 3: Deploy Only PTMS
```bash
ENABLE_TTMS=False
ENABLE_PTMS=True
```
- Only PTMS endpoints available: `/api/ptms/*`
- TTMS endpoints return 404

### Option 4: Deploy to Separate Servers
```
Server A: ENABLE_TTMS=True, ENABLE_PTMS=False
Server B: ENABLE_TTMS=False, ENABLE_PTMS=True
```
- Load balancer routes requests to appropriate server
- Shared PostgreSQL database
- Separate Django instances

## Backward Compatibility

- ✅ Existing TTMS data is preserved
- ✅ Database tables keep same structure and naming
- ✅ API endpoints remain at `/api/ttms/*`
- ✅ Legacy `api/` app is preserved (not deleted)
- ✅ Admin interface still works
- ✅ Django's built-in auth system intact

## Breaking Changes

❌ **None!** All changes are backward compatible.

- Existing API endpoints work as before
- Database tables are unchanged
- Authentication works the same way
- Admin interface is enhanced (new apps visible)

## New Features

✅ **Added:**

1. **App Toggle System**: Enable/disable apps via environment variables
2. **Selective Deployment**: Deploy specific apps independently
3. **Shared Auth**: Single authentication system for both apps
4. **Management Commands**: 
   - `python manage.py app_status` - Check enabled apps
   - `python manage.py init_apps` - Initialize with sample data
5. **Request Logging**: All requests are logged
6. **App Availability Middleware**: Checks if requested app is enabled
7. **Standardized Pagination**: Consistent across both apps
8. **Documentation**: Comprehensive guides for structure and deployment

## Configuration Options

### Environment Variables

```bash
# Enable/disable apps
ENABLE_TTMS=True|False
ENABLE_PTMS=True|False

# Django settings
DEBUG=True|False
SECRET_KEY=<your-secret-key>
ALLOWED_HOSTS=<comma-separated-hosts>

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=ttr_dashboard
DB_USER=postgres
DB_PASSWORD=<password>
DB_HOST=localhost
DB_PORT=5432

# CORS
CORS_ALLOWED_ORIGINS=<comma-separated-origins>
```

## Testing the Restructuring

### Check Status
```bash
python manage.py app_status
```

### Test API Endpoints
```bash
# Check which apps are enabled
curl http://localhost:8000/api/status/

# Test TTMS endpoints (if enabled)
curl http://localhost:8000/api/ttms/kpi/
curl http://localhost:8000/api/ttms/vehicles/

# Test PTMS endpoints (if enabled)
curl http://localhost:8000/api/ptms/projects/
curl http://localhost:8000/api/ptms/tasks/
```

### Run Tests
```bash
# All tests
python manage.py test

# Specific app
python manage.py test ttms
python manage.py test ptms
```

## Next Steps

1. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

2. **Verify Everything Works**:
   ```bash
   python manage.py app_status
   python manage.py check
   ```

3. **Test API**:
   ```bash
   python manage.py runserver
   # Visit http://localhost:8000/api/status/
   ```

4. **Read Documentation**:
   - `APP_STRUCTURE.md` - Detailed architecture
   - `DEPLOYMENT_GUIDE.md` - Deployment instructions

5. **Plan Deployment**:
   - Decide which apps to deploy
   - Set environment variables accordingly
   - Update frontend to use appropriate API endpoints

## Files Created/Modified

### Created
- `backend/ttms/` (entire directory)
- `backend/ptms/` (entire directory)
- `backend/core/auth/` (directory with files)
- `backend/core/utils/` (directory with files)
- `backend/core/management/` (directory with commands)
- `backend/core/middleware.py`
- `backend/APP_STRUCTURE.md`
- `backend/DEPLOYMENT_GUIDE.md`
- `backend/RESTRUCTURING_SUMMARY.md`

### Modified
- `backend/core/settings.py` - Added app toggles, auth, logging
- `backend/core/urls.py` - Dynamic URL registration
- `backend/requirements.txt` - Added `daphne==4.0.0`

### Preserved (Unchanged)
- `backend/api/` - All existing files preserved
- `backend/manage.py`
- All other Django files

## Support & Documentation

For detailed information, see:
1. **APP_STRUCTURE.md** - Complete architecture and design
2. **DEPLOYMENT_GUIDE.md** - Step-by-step deployment instructions
3. **Backend README.md** - Original project documentation

## Questions?

Common questions answered in the documentation:
- How do I deploy only TTMS?
- How do I use Docker for deployment?
- How do I enable/disable apps?
- How do I add a new model to TTMS/PTMS?
- How do I manage migrations?

Check `APP_STRUCTURE.md` and `DEPLOYMENT_GUIDE.md` for answers.
