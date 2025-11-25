# Local PostgreSQL Setup Guide

Run the TTMS and PTMS backends on your local machine using your existing PostgreSQL database instead of Docker.

## Prerequisites

- **PostgreSQL**: Version 12+ installed and running
- **Python**: Version 3.9+ installed
- **pip**: Python package manager

Verify installation:

```bash
psql --version
python --version
pip --version
```

---

## Step 1: Create PostgreSQL Databases

Create separate databases for TTMS and PTMS:

```bash
# Connect to PostgreSQL
psql -U postgres

# Create TTMS database
CREATE DATABASE ttms_local;

# Create PTMS database  
CREATE DATABASE ptms_local;

# List databases to verify
\l

# Exit
\q
```

If you use a different PostgreSQL user, note the credentials for later.

---

## Step 2: Configure Environment Variables

### Option A: Using .env File (Recommended)

Copy the template and update if needed:

```bash
cd backend
cp .env.local .env
```

Edit `.env` with your PostgreSQL credentials:

```env
DB_NAME=ttms_local
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DEBUG=True
SECRET_KEY=django-insecure-dev-key-change-in-production
```

### Option B: Export Environment Variables

```bash
export DB_NAME=ttms_local
export DB_USER=postgres
export DB_PASSWORD=postgres
export DB_HOST=localhost
export DB_PORT=5432
```

### Option C: Use Python-dotenv

Add to your development script or use automatically with `python-dotenv`:

```bash
pip install python-dotenv
```

Then in your shell:

```bash
cd backend
python -m dotenv run python manage.py migrate
```

---

## Step 3: Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

If `requirements.txt` doesn't exist, install Django packages:

```bash
pip install Django==4.2
pip install djangorestframework==3.14.0
pip install djangorestframework-simplejwt==5.2.2
pip install django-cors-headers==4.0.0
pip install psycopg2-binary==2.9.6
pip install python-dotenv==1.0.0
```

---

## Step 4: Run Migrations

### For TTMS

```bash
cd backend
export DJANGO_SETTINGS_MODULE=core.settings_ttms
python manage.py migrate
```

Or with .env file:

```bash
python -m dotenv run python manage.py migrate --settings core.settings_ttms
```

### For PTMS

```bash
export DJANGO_SETTINGS_MODULE=core.settings_ptms
python manage.py migrate
```

Or with .env file:

```bash
python -m dotenv run python manage.py migrate --settings core.settings_ptms
```

---

## Step 5: Create Superuser (Optional)

Create an admin user for each application:

### For TTMS

```bash
export DJANGO_SETTINGS_MODULE=core.settings_ttms
python manage.py createsuperuser
```

### For PTMS

```bash
export DJANGO_SETTINGS_MODULE=core.settings_ptms
python manage.py createsuperuser
```

---

## Step 6: Load Sample Data

```bash
# Load TTMS sample data
export DJANGO_SETTINGS_MODULE=core.settings_ttms
python manage.py loaddata ttms/fixtures/sample_data.json

# Load PTMS sample data
export DJANGO_SETTINGS_MODULE=core.settings_ptms
python manage.py loaddata ptms/fixtures/sample_data.json
```

---

## Step 7: Start Development Servers

You'll need two terminal windows to run TTMS and PTMS simultaneously.

### Terminal 1 - TTMS Server

```bash
cd backend
export DJANGO_SETTINGS_MODULE=core.settings_ttms
export DB_NAME=ttms_local
python manage.py runserver 8000
```

Expected output:

```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### Terminal 2 - PTMS Server

```bash
cd backend
export DJANGO_SETTINGS_MODULE=core.settings_ptms
export DB_NAME=ptms_local
python manage.py runserver 8001
```

Expected output:

```
Starting development server at http://127.0.0.1:8001/
Quit the server with CONTROL-C.
```

---

## Step 8: Verify Setup

### Test TTMS API

```bash
# Check KPI endpoint
curl http://localhost:8000/api/ttms/kpi/

# Check vehicles
curl http://localhost:8000/api/ttms/vehicles/

# Check admin
curl http://localhost:8000/admin/
```

### Test PTMS API

```bash
# Check projects
curl http://localhost:8001/api/ptms/projects/

# Check tasks
curl http://localhost:8001/api/ptms/tasks/

# Check admin
curl http://localhost:8001/admin/
```

---

## Using Python-dotenv Automatically

To automatically load `.env` files without exporting variables each time, create a `.env` file in the `backend/` directory:

```bash
cd backend
cat > .env << EOF
DJANGO_SETTINGS_MODULE=core.settings_ttms
DB_NAME=ttms_local
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DEBUG=True
SECRET_KEY=django-insecure-dev-key-change-in-production
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001,http://localhost:5173
EOF
```

Then use with `python-dotenv`:

```bash
pip install python-dotenv

# Run any command with automatic env loading
python -m dotenv run python manage.py migrate
python -m dotenv run python manage.py runserver 8000
```

---

## Shell Script for Automation

Create `backend/run_local.sh`:

```bash
#!/bin/bash

# Load environment variables
if [ -f .env.local ]; then
    export $(cat .env.local | grep -v '#' | xargs)
fi

# Allow command as argument
COMMAND=${1:-help}

case $COMMAND in
    migrate)
        echo "Running migrations for TTMS..."
        DJANGO_SETTINGS_MODULE=core.settings_ttms python manage.py migrate
        echo "Running migrations for PTMS..."
        DJANGO_SETTINGS_MODULE=core.settings_ptms python manage.py migrate
        ;;
    loaddata)
        echo "Loading sample data for TTMS..."
        DJANGO_SETTINGS_MODULE=core.settings_ttms python manage.py loaddata ttms/fixtures/sample_data.json
        echo "Loading sample data for PTMS..."
        DJANGO_SETTINGS_MODULE=core.settings_ptms python manage.py loaddata ptms/fixtures/sample_data.json
        ;;
    ttms)
        echo "Starting TTMS server on port 8000..."
        DJANGO_SETTINGS_MODULE=core.settings_ttms python manage.py runserver 8000
        ;;
    ptms)
        echo "Starting PTMS server on port 8001..."
        DJANGO_SETTINGS_MODULE=core.settings_ptms python manage.py runserver 8001
        ;;
    *)
        echo "Usage: $0 {migrate|loaddata|ttms|ptms}"
        echo ""
        echo "Examples:"
        echo "  $0 migrate   - Run migrations"
        echo "  $0 loaddata  - Load sample data"
        echo "  $0 ttms      - Start TTMS server"
        echo "  $0 ptms      - Start PTMS server"
        ;;
esac
```

Make it executable:

```bash
chmod +x backend/run_local.sh
```

Use it:

```bash
# Run migrations
./backend/run_local.sh migrate

# Load sample data
./backend/run_local.sh loaddata

# Start TTMS (in one terminal)
./backend/run_local.sh ttms

# Start PTMS (in another terminal)
./backend/run_local.sh ptms
```

---

## Database Connection Issues

### Issue: "could not connect to server"

**Cause**: PostgreSQL not running or connection parameters incorrect

**Solution**:
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Start PostgreSQL if needed
sudo systemctl start postgresql

# Test connection
psql -h localhost -U postgres -d ttms_local
```

### Issue: "password authentication failed"

**Cause**: Wrong PostgreSQL user or password

**Solution**:
```bash
# Reset PostgreSQL password
sudo -u postgres psql

# In psql:
ALTER USER postgres WITH PASSWORD 'new_password';
\q

# Update DB_PASSWORD in .env
```

### Issue: "database does not exist"

**Cause**: Database not created

**Solution**:
```bash
# Check existing databases
psql -U postgres -l

# Create missing databases
psql -U postgres -c "CREATE DATABASE ttms_local;"
psql -U postgres -c "CREATE DATABASE ptms_local;"
```

### Issue: "port 8000 already in use"

**Cause**: Another process using the port

**Solution**:
```bash
# Find process using port
lsof -i :8000

# Kill process (replace PID)
kill -9 <PID>

# Or use different port
python manage.py runserver 8002
```

---

## Quick Reference

```bash
# Initial setup
cd backend
cp .env.local .env
pip install -r requirements.txt

# Run migrations
export DJANGO_SETTINGS_MODULE=core.settings_ttms && python manage.py migrate
export DJANGO_SETTINGS_MODULE=core.settings_ptms && python manage.py migrate

# Load sample data
export DJANGO_SETTINGS_MODULE=core.settings_ttms && python manage.py loaddata ttms/fixtures/sample_data.json
export DJANGO_SETTINGS_MODULE=core.settings_ptms && python manage.py loaddata ptms/fixtures/sample_data.json

# Start servers
# Terminal 1:
export DJANGO_SETTINGS_MODULE=core.settings_ttms && python manage.py runserver 8000

# Terminal 2:
export DJANGO_SETTINGS_MODULE=core.settings_ptms && python manage.py runserver 8001
```

---

## Frontend Integration

Once backends are running locally, set up frontend:

```bash
# Create .env.local in project root
cat > .env.local << EOF
VITE_TTMS_API_URL=http://localhost:8000/api/ttms
VITE_TTMS_API_BASE=http://localhost:8000
VITE_PTMS_API_URL=http://localhost:8001/api/ptms
VITE_PTMS_API_BASE=http://localhost:8001
VITE_ENV=development
EOF

# Install dependencies
npm install

# Start frontend
npm run dev
```

Access the application at `http://localhost:5173`

---

## Switching Between Docker and Local

### Use Docker
```bash
cd backend/Docker
docker-compose up -d
```

Don't set `DB_HOST` environment variable - defaults will use `ttms_postgres` and `ptms_postgres`.

### Use Local PostgreSQL
```bash
export DB_HOST=localhost
export DB_NAME=ttms_local  # or ptms_local
```

Settings files automatically choose defaults based on `DB_HOST` environment variable.

---

## Next Steps

1. ✅ PostgreSQL databases created
2. ✅ Environment variables configured
3. ✅ Python dependencies installed
4. ✅ Migrations run
5. ✅ Sample data loaded
6. ✅ Servers started
7. Continue with [Frontend Integration Guide](./FRONTEND_INTEGRATION.md)

---

For more details, see:
- [QUICKSTART.md](./QUICKSTART.md)
- [API_REFERENCE.md](./API_REFERENCE.md)
- [FRONTEND_INTEGRATION.md](./FRONTEND_INTEGRATION.md)
