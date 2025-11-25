# Updated Project Structure - Independent Docker Containers

## New Architecture

```
backend/
├── manage.py                          # Main Django management script
│
├── core/                              # Django project configuration (shared base)
│   ├── __init__.py
│   ├── asgi.py
│   ��── wsgi.py
│   ├── base_settings.py               # NEW: Common settings base
│   ├── settings_ttms.py               # NEW: TTMS-specific settings
│   ├── settings_ptms.py               # NEW: PTMS-specific settings
│   ├── urls_ttms.py                   # NEW: TTMS URL config
│   ├── urls_ptms.py                   # NEW: PTMS URL config
│   └── middleware.py                  # Lightweight middleware only
│
├── common/                            # NEW: Lightweight shared utilities (NO models, NO auth)
│   ├── __init__.py
│   ├── utils.py                       # Common helper functions
│   ├── pagination.py                  # Standard pagination
│   ├── responses.py                   # Response formatting
│   ├── validators.py                  # Common validators
│   └── constants.py                   # Shared constants
│
├── ttms/                              # TTMS Application (COMPLETELY INDEPENDENT)
│   ├── migrations/                    # TTMS migrations
│   ├── management/
│   │   └── commands/                  # TTMS management commands
│   ├── apps.py                        # TTMS app config
│   ├── models.py                      # TTMS ONLY models
│   ├── serializers.py                 # TTMS ONLY serializers
│   ├── views.py                       # TTMS ONLY views
│   ├── admin.py                       # TTMS ONLY admin
│   ├── auth.py                        # TTMS authentication (own User model)
│   ├── permissions.py                 # TTMS permissions
│   ├── urls.py                        # TTMS URL routing
│   ├── __init__.py
│   └── tests.py                       # TTMS tests
│
├── ptms/                              # PTMS Application (COMPLETELY INDEPENDENT)
│   ├── migrations/                    # PTMS migrations
│   ├── management/
│   │   └── commands/                  # PTMS management commands
│   ├── apps.py                        # PTMS app config
│   ├── models.py                      # PTMS ONLY models
│   ├── serializers.py                 # PTMS ONLY serializers
│   ├── views.py                       # PTMS ONLY views
│   ├── admin.py                       # PTMS ONLY admin
│   ├── auth.py                        # PTMS authentication (own User model)
│   ├── permissions.py                 # PTMS permissions
│   ├── urls.py                        # PTMS URL routing
│   ├── __init__.py
│   └── tests.py                       # PTMS tests
│
├── api/                               # DEPRECATED: Keep only for reference/migration
│   ├── models.py                      # OLD: Preserved as backup
│   ├── views.py                       # OLD: Preserved as backup
│   ├── serializers.py                 # OLD: Preserved as backup
│   └── urls.py                        # OLD: Preserved as backup
│
├── Docker/                            # NEW: Docker configurations
│   ├── Dockerfile.ttms                # TTMS container
│   ├── Dockerfile.ptms                # PTMS container
│   ├── docker-compose.yml             # Local development
│   ├── docker-compose.prod.yml        # Production setup
│   ├── entrypoint.ttms.sh             # TTMS entrypoint
│   └── entrypoint.ptms.sh             # PTMS entrypoint
│
├── requirements.txt                   # Common dependencies
├── requirements-ttms.txt              # NEW: TTMS-specific (if needed)
├── requirements-ptms.txt              # NEW: PTMS-specific (if needed)
│
├── .dockerignore                      # Docker build ignore
├── .gitignore                         # Git ignore
│
└── README.md                          # Updated documentation
```

## Database Structure

```
TTMS Container (Docker)
├── Database: ttms_db (separate PostgreSQL instance)
├── User Table: ttms_auth_user (TTMS users only)
├── Tables:
│   ├── ttms_vehicle
│   ├── ttms_vehiclestage
│   ├── ttms_parkingcell
│   ├── ttms_vehicleentry
│   ├── ttms_systemalert
│   ├── ttms_turnaroundtimesparkline
│   ├── ttms_kpimetrics
│   └── ... (all Django internal tables)

PTMS Container (Docker)
├── Database: ptms_db (separate PostgreSQL instance)
├── User Table: ptms_auth_user (PTMS users only)
├── Tables:
│   ├── ptms_project
│   ├── ptms_task
│   └── ... (all Django internal tables)
```

## Settings Configuration

### `core/base_settings.py`
- Common Django settings
- Database config (to be overridden per app)
- Common middleware
- Installed apps (to be extended per app)

### `core/settings_ttms.py`
```python
from core.base_settings import *

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'rest_framework',
    'corsheaders',
    'ttms',  # ONLY TTMS app
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'ttms_db'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
        'HOST': os.getenv('DB_HOST', 'ttms_postgres'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

ROOT_URLCONF = 'core.urls_ttms'
```

### `core/settings_ptms.py`
```python
from core.base_settings import *

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'rest_framework',
    'corsheaders',
    'ptms',  # ONLY PTMS app
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'ptms_db'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
        'HOST': os.getenv('DB_HOST', 'ptms_postgres'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

ROOT_URLCONF = 'core.urls_ptms'
```

## URL Configuration

### `core/urls_ttms.py`
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/ttms/', include('ttms.urls')),
]
```

### `core/urls_ptms.py`
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/ptms/', include('ptms.urls')),
]
```

## Docker Setup

### `Docker/Dockerfile.ttms`
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DJANGO_SETTINGS_MODULE=core.settings_ttms
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

ENTRYPOINT ["./Docker/entrypoint.ttms.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### `Docker/Dockerfile.ptms`
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DJANGO_SETTINGS_MODULE=core.settings_ptms
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

ENTRYPOINT ["./Docker/entrypoint.ptms.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### `Docker/docker-compose.yml` (Development)
```yaml
version: '3.8'

services:
  # TTMS Stack
  ttms_postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: ttms_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5433:5432"
    volumes:
      - ttms_postgres_data:/var/lib/postgresql/data

  ttms_app:
    build:
      context: .
      dockerfile: Docker/Dockerfile.ttms
    command: python manage.py runserver 0.0.0.0:8000
    ports:
      - "8001:8000"
    environment:
      DJANGO_SETTINGS_MODULE: core.settings_ttms
      DB_HOST: ttms_postgres
      DB_NAME: ttms_db
      DEBUG: "True"
    depends_on:
      - ttms_postgres
    volumes:
      - .:/app

  # PTMS Stack
  ptms_postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: ptms_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5434:5432"
    volumes:
      - ptms_postgres_data:/var/lib/postgresql/data

  ptms_app:
    build:
      context: .
      dockerfile: Docker/Dockerfile.ptms
    command: python manage.py runserver 0.0.0.0:8000
    ports:
      - "8002:8000"
    environment:
      DJANGO_SETTINGS_MODULE: core.settings_ptms
      DB_HOST: ptms_postgres
      DB_NAME: ptms_db
      DEBUG: "True"
    depends_on:
      - ptms_postgres
    volumes:
      - .:/app

volumes:
  ttms_postgres_data:
  ptms_postgres_data:
```

## Key Differences from Previous Structure

| Aspect | Previous | New |
|--------|----------|-----|
| Settings | Single settings.py with toggles | Separate: base_settings.py, settings_ttms.py, settings_ptms.py |
| Database | Shared database | Separate databases per app |
| Authentication | Shared auth_user table | Independent auth_user tables |
| INSTALLED_APPS | Both apps always included | Only relevant app per container |
| URL Routing | Dynamic based on toggles | Static per app |
| Docker | Not designed | Purpose-built Dockerfiles |
| Migrations | Combined | Independent per app |
| Shared Code | Limited | Lightweight utils only |

## Deployment Scenarios

### Development: Run Both Locally
```bash
cd backend
docker-compose -f Docker/docker-compose.yml up
# TTMS: http://localhost:8001/api/ttms/
# PTMS: http://localhost:8002/api/ptms/
```

### Production: Deploy Only TTMS
```bash
docker build -f Docker/Dockerfile.ttms -t ttms-app:latest .
docker run -e DB_HOST=ttms-postgres ttms-app:latest
# Endpoint: /api/ttms/*
```

### Production: Deploy Only PTMS
```bash
docker build -f Docker/Dockerfile.ptms -t ptms-app:latest .
docker run -e DB_HOST=ptms-postgres ptms-app:latest
# Endpoint: /api/ptms/*
```

## What Gets Removed

❌ All toggle logic (ENABLE_TTMS, ENABLE_PTMS)
❌ Dynamic URL registration
❌ App availability middleware
❌ Toggle-based management commands
❌ Shared authentication between apps
❌ Middleware checking app status
❌ All the enable/disable complexity

## What Stays Lightweight in `common/`

✅ Utility functions (not models)
✅ Pagination classes
✅ Response formatters
✅ Validators
✅ Constants
✅ Date/time helpers
✅ **NO** authentication
✅ **NO** models
✅ **NO** business logic

---

**Ready to proceed with implementation?** ✅

Would you like me to go ahead and implement:
1. Refactor settings files
2. Update TTMS app for independence
3. Update PTMS app for independence
4. Create common utilities
5. Create Dockerfiles
6. Update URL configurations
