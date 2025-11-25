#!/bin/bash
# PTMS Django Application Entrypoint Script
# Handles database migrations, static files collection, and app startup

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}PTMS Application Startup${NC}"
echo -e "${YELLOW}========================================${NC}"

# Wait for database to be ready
echo -e "${YELLOW}Waiting for PTMS PostgreSQL database to be ready...${NC}"
until python manage.py shell --settings=core.settings_ptms -c "import django; django.setup()" 2>/dev/null; do
    echo -e "${YELLOW}Retrying in 5 seconds...${NC}"
    sleep 5
done
echo -e "${GREEN}✓ Database is ready${NC}"

# Run migrations
echo -e "${YELLOW}Running database migrations...${NC}"
python manage.py migrate --settings=core.settings_ptms --noinput
echo -e "${GREEN}✓ Migrations completed${NC}"

# Create superuser if it doesn't exist (development only)
if [ "$DEBUG" = "True" ]; then
    echo -e "${YELLOW}Checking for superuser...${NC}"
    python manage.py shell --settings=core.settings_ptms << END
from ptms.auth.models import PTMSUser
import os

if not PTMSUser.objects.filter(email='admin@ptms.local').exists():
    PTMSUser.objects.create_superuser(
        email='admin@ptms.local',
        password='admin123',
        first_name='PTMS',
        last_name='Admin'
    )
    print('Superuser created: admin@ptms.local')
else:
    print('Superuser already exists')
END
fi

# Collect static files (production)
if [ "$DEBUG" != "True" ]; then
    echo -e "${YELLOW}Collecting static files...${NC}"
    python manage.py collectstatic --settings=core.settings_ptms --noinput
    echo -e "${GREEN}✓ Static files collected${NC}"
fi

echo -e "${YELLOW}Loading initial data (if available)...${NC}"
if [ -f "ptms/fixtures/initial_data.json" ]; then
    python manage.py loaddata ptms/fixtures/initial_data.json --settings=core.settings_ptms
    echo -e "${GREEN}✓ Initial data loaded${NC}"
else
    echo -e "${YELLOW}No initial data to load${NC}"
fi

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}PTMS Application Ready!${NC}"
echo -e "${GREEN}========================================${NC}"

# Execute the main command
exec "$@"
