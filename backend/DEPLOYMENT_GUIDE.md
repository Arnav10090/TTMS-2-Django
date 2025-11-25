# TTMS & PTMS Deployment Guide

## Quick Start

### 1. Setup & Initial Configuration

```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Create .env file with configuration
cat > .env << EOF
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
DB_ENGINE=django.db.backends.postgresql
DB_NAME=ttr_dashboard
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

# App toggles
ENABLE_TTMS=True
ENABLE_PTMS=True
EOF

# Apply migrations
python manage.py migrate

# Create superuser and sample data
python manage.py init_apps --create-superuser --sample-data

# Start development server
python manage.py runserver
```

### 2. Check What's Available

```bash
# Check app status
python manage.py app_status

# Test API endpoints
curl http://localhost:8000/api/status/
```

## Deployment Scenarios

### Scenario 1: Deploy Both TTMS and PTMS

```bash
# .env configuration
ENABLE_TTMS=True
ENABLE_PTMS=True

# Start server
python manage.py runserver

# Available endpoints:
# - /api/ttms/* - TTMS API
# - /api/ptms/* - PTMS API
# - /api/status/ - Status check
```

### Scenario 2: Deploy Only TTMS

```bash
# .env configuration
ENABLE_TTMS=True
ENABLE_PTMS=False

# Start server
python manage.py runserver

# Available endpoints:
# - /api/ttms/* - TTMS API only
# - /api/status/ - Status check
# - /api/ptms/* - Returns 404
```

### Scenario 3: Deploy Only PTMS

```bash
# .env configuration
ENABLE_TTMS=False
ENABLE_PTMS=True

# Start server
python manage.py runserver

# Available endpoints:
# - /api/ptms/* - PTMS API only
# - /api/status/ - Status check
# - /api/ttms/* - Returns 404
```

### Scenario 4: Multiple Servers (Load Balancing)

**Server A (TTMS):**
```bash
# .env
ENABLE_TTMS=True
ENABLE_PTMS=False
BIND_PORT=8001

python manage.py runserver 0.0.0.0:8001
```

**Server B (PTMS):**
```bash
# .env
ENABLE_TTMS=False
ENABLE_PTMS=True
BIND_PORT=8002

python manage.py runserver 0.0.0.0:8002
```

**Load Balancer (nginx example):**
```nginx
upstream ttms {
    server server_a:8001;
}

upstream ptms {
    server server_b:8002;
}

server {
    listen 80;
    server_name api.example.com;

    location /api/ttms/ {
        proxy_pass http://ttms;
    }

    location /api/ptms/ {
        proxy_pass http://ptms;
    }
}
```

## Docker Deployment

### Dockerfile for Both Apps

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Run migrations and start server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
```

### Docker Compose for Both Apps

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: ttr_dashboard
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data

  django_both:
    build: ./backend
    command: >
      sh -c "python manage.py migrate &&
             python manage.py init_apps --create-superuser --sample-data &&
             python manage.py runserver 0.0.0.0:8000"
    ports:
      - "8000:8000"
    environment:
      ENABLE_TTMS: "True"
      ENABLE_PTMS: "True"
      DB_HOST: db
      DEBUG: "True"
    depends_on:
      - db

volumes:
  postgres_data:
```

### Docker Compose for Separate Apps

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: ttr_dashboard
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data

  ttms_server:
    build: ./backend
    command: >
      sh -c "python manage.py migrate &&
             python manage.py runserver 0.0.0.0:8001"
    ports:
      - "8001:8001"
    environment:
      ENABLE_TTMS: "True"
      ENABLE_PTMS: "False"
      DB_HOST: db
      DEBUG: "True"
    depends_on:
      - db

  ptms_server:
    build: ./backend
    command: >
      sh -c "python manage.py migrate &&
             python manage.py runserver 0.0.0.0:8002"
    ports:
      - "8002:8002"
    environment:
      ENABLE_TTMS: "False"
      ENABLE_PTMS: "True"
      DB_HOST: db
      DEBUG: "True"
    depends_on:
      - db

  nginx:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - ttms_server
      - ptms_server

volumes:
  postgres_data:
```

## Production Deployment Checklist

### Before Deployment

- [ ] Update `SECRET_KEY` in settings
- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Update `CORS_ALLOWED_ORIGINS` with your frontend URLs
- [ ] Configure proper database (PostgreSQL recommended)
- [ ] Run `python manage.py collectstatic`
- [ ] Run `python manage.py check --deploy`

### Environment Variables (Production)

```bash
# Django
DEBUG=False
SECRET_KEY=your-very-secure-secret-key-here
ALLOWED_HOSTS=api.example.com,www.example.com

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=ttr_dashboard_prod
DB_USER=db_user
DB_PASSWORD=very_secure_password
DB_HOST=db.example.com
DB_PORT=5432

# CORS
CORS_ALLOWED_ORIGINS=https://app.example.com,https://www.example.com

# Apps
ENABLE_TTMS=True
ENABLE_PTMS=True

# Logging
DJANGO_LOG_LEVEL=WARNING
```

### Using Gunicorn

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn core.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --timeout 120
```

### Using uWSGI

```bash
# Install uwsgi
pip install uwsgi

# Run with uwsgi
uwsgi --http :8000 \
      --wsgi-file core/wsgi.py \
      --master \
      --processes 4 \
      --threads 2
```

## Database Backup & Restore

### Backup PostgreSQL Database

```bash
# Backup
pg_dump -U postgres ttr_dashboard > backup.sql

# Backup with compression
pg_dump -U postgres ttr_dashboard | gzip > backup.sql.gz
```

### Restore PostgreSQL Database

```bash
# Restore
psql -U postgres -d ttr_dashboard < backup.sql

# Restore from compressed
gunzip -c backup.sql.gz | psql -U postgres -d ttr_dashboard
```

## Monitoring & Logging

### Django Admin

Access Django admin at `/admin/`:
- Monitor app status
- Manage users and permissions
- Review database records
- Monitor system alerts

### Application Logging

Logs are written to `backend/logs/django.log`. Configure log level in settings:

```python
LOGGING = {
    'handlers': {
        'file': {
            'level': 'INFO',  # Change to DEBUG for more detailed logs
            'filename': 'logs/django.log',
        }
    }
}
```

## Common Issues & Solutions

### Issue: App not found (404)
```bash
# Check app status
python manage.py app_status

# Verify app is enabled in environment
echo $ENABLE_TTMS
echo $ENABLE_PTMS
```

### Issue: Database migration errors
```bash
# Check migration status
python manage.py showmigrations

# Reapply migrations
python manage.py migrate --plan
python manage.py migrate
```

### Issue: Superuser doesn't exist
```bash
# Create superuser
python manage.py createsuperuser

# Or use init command
python manage.py init_apps --create-superuser
```

### Issue: Static files not loading in production
```bash
# Collect static files
python manage.py collectstatic --noinput

# Verify collection
ls staticfiles/
```

## Performance Tuning

### Database Optimization
```python
# settings.py
DATABASES = {
    'default': {
        'CONN_MAX_AGE': 600,  # Connection pooling
        'OPTIONS': {
            'connect_timeout': 10,
        }
    }
}
```

### Caching
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

### Query Optimization
- Use `select_related()` for foreign keys
- Use `prefetch_related()` for reverse relations
- Use `only()` and `defer()` for large models

## Monitoring Commands

```bash
# Check app status
python manage.py app_status

# Run health checks
python manage.py check

# Check for deployment issues
python manage.py check --deploy

# Database statistics
python manage.py dbshell
# Then: SELECT * FROM information_schema.tables WHERE table_schema = 'public';
```
