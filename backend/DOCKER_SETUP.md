# Docker Setup and Deployment Guide

## Overview

This guide covers setting up and deploying TTMS and PTMS applications using Docker and Docker Compose. Both applications run independently with their own databases, authentication systems, and services.

## Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- PostgreSQL 15+ (included in Docker images)
- Git

## Directory Structure

```
backend/
├── Docker/
│   ├── Dockerfile.ttms           # TTMS container image
│   ├── Dockerfile.ptms           # PTMS container image
│   ├── docker-compose.yml        # Development environment
│   ├── docker-compose.prod.yml   # Production environment
│   ├── entrypoint.ttms.sh        # TTMS startup script
│   ├── entrypoint.ptms.sh        # PTMS startup script
│   ├── init-databases.sh         # Database initialization
│   └── nginx.conf                # Nginx reverse proxy config (optional)
├── .dockerignore                 # Files to exclude from Docker image
├── .env.example                  # Environment variables template
└── requirements.txt              # Python dependencies
```

## Development Setup

### 1. Prepare Environment File

```bash
cd backend

# Copy example env file
cp .env.example .env

# Update .env with your configuration
nano .env
```

**Key variables for development:**
```
DEBUG=True
SECRET_KEY=django-insecure-your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1,ttms,ptms
DB_PASSWORD=postgres
TTMS_DB_NAME=ttms_db
PTMS_DB_NAME=ptms_db
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
```

### 2. Start Development Containers

```bash
# Build and start both services with their databases
docker-compose -f Docker/docker-compose.yml up -d

# Watch the logs
docker-compose -f Docker/docker-compose.yml logs -f

# To stop
docker-compose -f Docker/docker-compose.yml down
```

### 3. Verify Services

```bash
# Check running containers
docker-compose -f Docker/docker-compose.yml ps

# Expected output:
# NAME                COMMAND             SERVICE      STATUS      PORTS
# ttms_app            python manage.py... ttms         running     0.0.0.0:8000->8000/tcp
# ttms_postgres       postgres            ttms_postgres running    0.0.0.0:5432->5432/tcp
# ptms_app            python manage.py... ptms         running     0.0.0.0:8001->8000/tcp
# ptms_postgres       postgres            ptms_postgres running    0.0.0.0:5433->5432/tcp
```

### 4. Access Applications

**TTMS:**
- API: http://localhost:8000/api/ttms/
- Admin: http://localhost:8000/admin/
- Default credentials: admin@ttms.local / admin123

**PTMS:**
- API: http://localhost:8001/api/ptms/
- Admin: http://localhost:8001/admin/
- Default credentials: admin@ptms.local / admin123

### 5. Database Access

```bash
# TTMS PostgreSQL
PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d ttms_db

# PTMS PostgreSQL
PGPASSWORD=postgres psql -h localhost -p 5433 -U postgres -d ptms_db
```

## Development Commands

### Run Migrations

```bash
# TTMS migrations
docker-compose -f Docker/docker-compose.yml exec ttms \
  python manage.py migrate --settings=core.settings_ttms

# PTMS migrations
docker-compose -f Docker/docker-compose.yml exec ptms \
  python manage.py migrate --settings=core.settings_ptms
```

### Create Superuser

```bash
# TTMS superuser
docker-compose -f Docker/docker-compose.yml exec ttms \
  python manage.py createsuperuser --settings=core.settings_ttms

# PTMS superuser
docker-compose -f Docker/docker-compose.yml exec ptms \
  python manage.py createsuperuser --settings=core.settings_ptms
```

### Run Shell

```bash
# TTMS shell
docker-compose -f Docker/docker-compose.yml exec ttms \
  python manage.py shell --settings=core.settings_ttms

# PTMS shell
docker-compose -f Docker/docker-compose.yml exec ptms \
  python manage.py shell --settings=core.settings_ptms
```

### View Logs

```bash
# All services
docker-compose -f Docker/docker-compose.yml logs -f

# Specific service
docker-compose -f Docker/docker-compose.yml logs -f ttms
docker-compose -f Docker/docker-compose.yml logs -f ptms

# Recent logs only
docker-compose -f Docker/docker-compose.yml logs --tail=50 -f ttms
```

### Restart Services

```bash
# Restart TTMS
docker-compose -f Docker/docker-compose.yml restart ttms

# Restart PTMS
docker-compose -f Docker/docker-compose.yml restart ptms

# Restart everything
docker-compose -f Docker/docker-compose.yml restart
```

### Clean Up

```bash
# Stop containers
docker-compose -f Docker/docker-compose.yml down

# Remove volumes (WARNING: deletes databases!)
docker-compose -f Docker/docker-compose.yml down -v

# Remove all images
docker-compose -f Docker/docker-compose.yml down --rmi all
```

## Production Setup

### 1. Prepare Environment

```bash
# Copy and configure environment for production
cp .env.example .env.prod

# Edit with production values
nano .env.prod
```

**Production environment variables:**
```
DEBUG=False
SECRET_KEY=<generate-strong-secret-key>
ALLOWED_HOSTS=ttms.example.com,ptms.example.com
DB_PASSWORD=<strong-postgres-password>
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
```

### 2. Generate Secret Key

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 3. Start Production Services

```bash
# Load production environment
export $(cat .env.prod | xargs)

# Start services with production compose file
docker-compose -f Docker/docker-compose.prod.yml up -d
```

### 4. Verify Production Deployment

```bash
# Check container health
docker-compose -f Docker/docker-compose.prod.yml ps

# Check logs
docker-compose -f Docker/docker-compose.prod.yml logs -f ttms
docker-compose -f Docker/docker-compose.prod.yml logs -f ptms
```

### 5. Backup and Maintenance

```bash
# Backup TTMS database
docker-compose -f Docker/docker-compose.prod.yml exec ttms_postgres \
  pg_dump -U postgres ttms_db > /backups/ttms/ttms_db_$(date +%Y%m%d_%H%M%S).sql

# Backup PTMS database
docker-compose -f Docker/docker-compose.prod.yml exec ptms_postgres \
  pg_dump -U postgres ptms_db > /backups/ptms/ptms_db_$(date +%Y%m%d_%H%M%S).sql

# Restore TTMS database
docker-compose -f Docker/docker-compose.prod.yml exec -T ttms_postgres \
  psql -U postgres ttms_db < /backups/ttms/ttms_db_YYYYMMDD_HHMMSS.sql
```

## Scaling and Optimization

### Horizontal Scaling

For production, you can scale services using Docker Swarm or Kubernetes. Here's a basic example:

```bash
# Scale TTMS to 3 replicas
docker-compose -f Docker/docker-compose.prod.yml up --scale ttms=3

# Scale PTMS to 3 replicas
docker-compose -f Docker/docker-compose.prod.yml up --scale ptms=3
```

### Performance Tuning

**Database Optimization:**
```sql
-- Add indexes for common queries
CREATE INDEX idx_ttms_user_email ON ttms_auth_ttmsuser(email);
CREATE INDEX idx_ttms_vehicle_regnumber ON ttms_vehicle(reg_no);
CREATE INDEX idx_ptms_user_email ON ptms_auth_ptmsuser(email);
```

**Django Optimization:**
- Use database connection pooling with pgBouncer
- Enable Redis caching for sessions and API responses
- Configure Nginx caching for static assets
- Use CDN for media files

## Networking

### Networks Used

- `ttms_network`: Internal network for TTMS services
- `ptms_network`: Internal network for PTMS services
- Both services can communicate through Docker's internal DNS

### Connecting External Services

If you need to connect to external databases or services:

```yaml
# In docker-compose.yml, add external network reference
networks:
  external_network:
    external: true
```

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose logs ttms

# Check if port is already in use
lsof -i :8000

# Rebuild the image
docker-compose build --no-cache ttms
```

### Database Connection Issues

```bash
# Test database connectivity
docker-compose exec ttms python manage.py dbshell --settings=core.settings_ttms

# Check database status
docker-compose exec ttms_postgres pg_isready -U postgres
```

### Slow Performance

```bash
# Check resource usage
docker stats

# Increase resource limits in docker-compose.yml
services:
  ttms:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

### Permission Issues

```bash
# Check file permissions
docker-compose exec ttms ls -la /app

# Fix permissions
docker-compose exec -u root ttms chown -R django:django /app
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build and push Docker image
        run: |
          docker build -f Docker/Dockerfile.ttms -t ttms:latest .
          docker build -f Docker/Dockerfile.ptms -t ptms:latest .
      
      - name: Deploy with Docker Compose
        run: |
          docker-compose -f Docker/docker-compose.prod.yml up -d
```

## Security Best Practices

1. **Never commit secrets** - Use `.env` files in `.gitignore`
2. **Use strong passwords** - Generate random secrets for production
3. **Enable HTTPS** - Use Nginx reverse proxy with SSL certificates
4. **Limit container access** - Use firewall rules and network policies
5. **Regular updates** - Keep Docker images and dependencies updated
6. **Database backups** - Implement automated backup strategy
7. **Log monitoring** - Set up centralized logging with ELK stack

## References

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Django Deployment Guide](https://docs.djangoproject.com/en/4.2/howto/deployment/)
- [PostgreSQL Docker Image](https://hub.docker.com/_/postgres)

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review Docker logs: `docker-compose logs -f`
3. Check Django logs: `docker-compose exec ttms tail -f /var/log/django.log`
4. Consult official documentation

---

**Last Updated**: 2024
**Version**: 1.0
