# Quick Start Guide

Get the TTMS and PTMS systems running in under 10 minutes.

## Prerequisites

Before you begin, ensure you have installed:

- **Docker**: Version 20.10+ ([Install Docker](https://docs.docker.com/get-docker/))
- **Docker Compose**: Version 1.29+ (included with Docker Desktop)
- **Node.js**: Version 18+ ([Install Node.js](https://nodejs.org/))
- **Git**: Version 2.30+ (for cloning the repository)

### Verify Installation

```bash
# Check Docker
docker --version
docker-compose --version

# Check Node.js
node --version
npm --version

# Check Git
git --version
```

---

## Backend Setup (5 Steps - 3 minutes)

### Step 1: Navigate to Backend Directory

```bash
cd backend/Docker
```

### Step 2: Create Environment File

Create a `.env` file in the `backend/Docker` directory:

```env
# Database Configuration
DB_USER=postgres
DB_PASSWORD=postgres
TTMS_DB_NAME=ttms_db
PTMS_DB_NAME=ptms_db

# Django Settings
SECRET_KEY=django-insecure-your-secret-key-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
```

### Step 3: Start Docker Containers

```bash
# Start both TTMS and PTMS services
docker-compose -f docker-compose.yml up -d

# Verify containers are running
docker-compose ps
```

Expected output:
```
NAME                 COMMAND                  SERVICE             STATUS              PORTS
ptms_app             "python manage.py ru…"   ptms                Up 2 seconds        0.0.0.0:8001->8000/tcp
ptms_postgres        "docker-entrypoint.s…"   ptms_postgres       Up 3 seconds        0.0.0.0:5433->5432/tcp
ttms_app             "python manage.py ru…"   ttms                Up 2 seconds        0.0.0.0:8000->8000/tcp
ttms_postgres        "docker-entrypoint.s…"   ttms_postgres       Up 3 seconds        0.0.0.0:5432->5432/tcp
```

### Step 4: Load Sample Data

```bash
# Navigate back to backend
cd ..

# Make the script executable
chmod +x scripts/load_sample_data.sh

# Load sample data
bash scripts/load_sample_data.sh
```

Expected output:
```
==================================================
Loading Sample Data for TTMS and PTMS
==================================================

📊 Loading TTMS Sample Data...
✅ TTMS sample data loaded successfully!

📊 Loading PTMS Sample Data...
✅ PTMS sample data loaded successfully!

==================================================
✅ All sample data loaded successfully!
==================================================
```

### Step 5: Verify Backend Setup

```bash
# Run health check script
chmod +x scripts/health_check.sh
bash scripts/health_check.sh
```

Test the APIs:

```bash
# Test TTMS API
curl http://localhost:8000/api/ttms/kpi/

# Test PTMS API
curl http://localhost:8001/api/ptms/projects/
```

---

## Frontend Setup (3 Steps - 4 minutes)

### Step 1: Navigate to Frontend Directory

```bash
cd ../..
```

### Step 2: Install Dependencies

```bash
# Install all dependencies
npm install

# Verify installation
npm list | head -20
```

### Step 3: Create Environment Configuration

Create a `.env.local` file in the project root:

```env
# TTMS API Configuration
VITE_TTMS_API_URL=http://localhost:8000/api/ttms
VITE_TTMS_API_BASE=http://localhost:8000

# PTMS API Configuration
VITE_PTMS_API_URL=http://localhost:8001/api/ptms
VITE_PTMS_API_BASE=http://localhost:8001

# Environment
VITE_ENV=development
VITE_DEBUG=true
```

### Step 4: Start Development Server

```bash
npm run dev
```

Expected output:
```
  VITE v5.0.0  ready in 234 ms

  ➜  Local:   http://localhost:5173/
  ➜  Press h to show help
```

The application will open at `http://localhost:5173`

---

## Testing the Setup

### 1. Check Backend Health

```bash
bash backend/scripts/health_check.sh
```

### 2. Test TTMS API

```bash
bash backend/scripts/test_ttms_api.sh
```

Expected output:
```
============================================
Testing: API Health Check ... ✅ PASS (HTTP 200)
Testing: Get KPI Metrics ... ✅ PASS (HTTP 200)
Testing: Get Vehicles ... ✅ PASS (HTTP 200)
...
============================================
Test Summary
============================================
Passed: 15
Failed: 0

✅ All tests passed!
```

### 3. Test PTMS API

```bash
bash backend/scripts/test_ptms_api.sh
```

### 4. Access the Application

1. Open your browser to `http://localhost:5173`
2. Navigate to the login page
3. Use default credentials (set up during backend initialization)
4. See populated dashboards with sample data

---

## Accessing the APIs

### TTMS API
- **Base URL**: `http://localhost:8000/api/ttms`
- **Health Check**: `http://localhost:8000/api/ttms/kpi/`
- **Vehicles**: `http://localhost:8000/api/ttms/vehicles/`
- **Alerts**: `http://localhost:8000/api/ttms/alerts/`

### PTMS API
- **Base URL**: `http://localhost:8001/api/ptms`
- **Projects**: `http://localhost:8001/api/ptms/projects/`
- **Tasks**: `http://localhost:8001/api/ptms/tasks/`

---

## Common Issues & Solutions

### Issue 1: Port Already in Use

**Error**: `Address already in use`

**Solution**:
```bash
# Find process using port
lsof -i :8000  # TTMS
lsof -i :8001  # PTMS
lsof -i :5173  # Frontend

# Kill process (replace PID)
kill -9 <PID>

# Or change port in docker-compose.yml
```

### Issue 2: Docker Permission Denied

**Error**: `permission denied while trying to connect to Docker daemon`

**Solution**:
```bash
# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Or use sudo
sudo docker-compose up -d
```

### Issue 3: Database Connection Failed

**Error**: `psycopg2.OperationalError: could not connect to server`

**Solution**:
```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs ttms_postgres

# Restart database
docker-compose restart ttms_postgres ptms_postgres

# Wait 10 seconds and try again
sleep 10
docker-compose ps
```

### Issue 4: CORS Error in Frontend

**Error**: `Access to XMLHttpRequest has been blocked by CORS policy`

**Solution**:
```bash
# Check CORS_ALLOWED_ORIGINS in .env
cat backend/Docker/.env | grep CORS

# Update if needed
# Make sure frontend port (5173) is included

# Restart backend
docker-compose restart ttms ptms
```

### Issue 5: Sample Data Not Loading

**Error**: `Error loading fixture...`

**Solution**:
```bash
# Check if migrations ran
docker-compose exec ttms python manage.py migrate
docker-compose exec ptms python manage.py migrate

# Then load data
bash backend/scripts/load_sample_data.sh
```

### Issue 6: Frontend Won't Connect to Backend

**Error**: `Cannot GET /api/ttms/...` or connection timeout

**Solution**:
1. Verify backend is running: `docker-compose ps`
2. Test backend directly: `curl http://localhost:8000/api/ttms/kpi/`
3. Check `.env.local` API URLs
4. Verify Vite proxy in `vite.config.ts`
5. Check browser console for detailed error

---

## File Structure Overview

```
.
├── backend/
│   ├── Docker/              # Docker configuration
│   │   ├── docker-compose.yml
│   │   ├── Dockerfile.ttms
│   │   └── .env             # Backend environment
│   ├── scripts/
│   │   ├── load_sample_data.sh
│   │   ├── test_ttms_api.sh
│   │   ├── test_ptms_api.sh
│   ���   └── health_check.sh
│   ├── ttms/                # TTMS Django app
│   │   ├── fixtures/
│   │   │   └── sample_data.json
│   │   └── models.py
│   ├── ptms/                # PTMS Django app
│   │   ├── fixtures/
│   │   │   └── sample_data.json
│   │   └── models.py
│   └── manage.py
├── src/                     # Frontend source
│   ├── services/
│   │   ├── auth.service.ts
│   │   ├── api.ts
│   │   ├── ttms.service.ts
│   │   └── ptms.service.ts
│   ├── components/
│   ├── pages/
│   └── App.tsx
├── .env.local               # Frontend environment
├── FRONTEND_INTEGRATION.md  # Integration guide
├── API_REFERENCE.md         # API documentation
└── QUICKSTART.md            # This file
```

---

## Development Workflow

### Making Code Changes

1. **Backend Changes**:
   ```bash
   # Edit files in backend/
   # Django will auto-reload
   docker-compose logs -f ttms
   ```

2. **Frontend Changes**:
   ```bash
   # Edit files in src/
   # Vite will hot-reload
   # Check terminal for compilation status
   ```

3. **Database Changes**:
   ```bash
   docker-compose exec ttms python manage.py migrate
   docker-compose exec ptms python manage.py migrate
   ```

### Viewing Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f ttms
docker-compose logs -f ptms

# With timestamps
docker-compose logs -f --timestamps
```

### Stopping Services

```bash
# Stop all
docker-compose down

# Stop specific service
docker-compose stop ttms

# Remove volumes (careful - deletes data!)
docker-compose down -v
```

---

## Next Steps

1. ✅ **Backend Running**: Docker containers are up
2. ✅ **Sample Data Loaded**: Test data is available
3. ✅ **Frontend Running**: Application is accessible
4. **Explore APIs**: Check [API_REFERENCE.md](./API_REFERENCE.md)
5. **Integrate Frontend**: See [FRONTEND_INTEGRATION.md](./FRONTEND_INTEGRATION.md)

---

## Useful Commands

```bash
# Check service status
docker-compose ps

# View recent logs
docker-compose logs --tail=50

# Access database
docker-compose exec ttms_postgres psql -U postgres -d ttms_db

# Run Django shell
docker-compose exec ttms python manage.py shell

# Create superuser
docker-compose exec ttms python manage.py createsuperuser

# Reset database
docker-compose exec ttms python manage.py flush

# Clear cache
docker system prune -a
```

---

## Resources

- **API Reference**: [API_REFERENCE.md](./API_REFERENCE.md)
- **Frontend Integration**: [FRONTEND_INTEGRATION.md](./FRONTEND_INTEGRATION.md)
- **Docker Documentation**: https://docs.docker.com/
- **Django Documentation**: https://docs.djangoproject.com/
- **React Documentation**: https://react.dev/
- **Vite Documentation**: https://vitejs.dev/

---

## Support

If you encounter issues:

1. Check [Common Issues & Solutions](#common-issues--solutions) section
2. Review service logs: `docker-compose logs`
3. Run health check: `bash backend/scripts/health_check.sh`
4. Test APIs: `bash backend/scripts/test_ttms_api.sh`
5. Check browser console for frontend errors

---

**You're all set! The system should now be fully operational.** 🚀

For detailed development instructions, see [FRONTEND_INTEGRATION.md](./FRONTEND_INTEGRATION.md) and [API_REFERENCE.md](./API_REFERENCE.md).
