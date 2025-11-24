#!/bin/bash

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Django Backend Startup Script${NC}"
echo "=================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python -m venv venv
fi

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -r requirements.txt --quiet

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Dependencies installed${NC}"
else
    echo -e "${RED}✗ Failed to install dependencies${NC}"
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env file from .env.example...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✓ .env file created (please update with your database credentials)${NC}"
fi

# Run migrations
echo -e "${YELLOW}Running database migrations...${NC}"
python manage.py migrate

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Database migrations completed${NC}"
else
    echo -e "${RED}✗ Migration failed${NC}"
    exit 1
fi

# Check if superuser exists
echo -e "${YELLOW}Checking for superuser...${NC}"
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); print('Superuser exists') if User.objects.filter(is_superuser=True).exists() else print('No superuser')" | grep -q "Superuser exists"

if [ $? -ne 0 ]; then
    echo -e "${YELLOW}Creating superuser...${NC}"
    python manage.py createsuperuser
fi

# Start development server
echo -e "${GREEN}=================================="
echo -e "Starting Django Development Server"
echo -e "==================================${NC}"
echo -e "${GREEN}API URL: http://localhost:8000/api/${NC}"
echo -e "${GREEN}Admin URL: http://localhost:8000/admin/${NC}"
echo -e "${GREEN}${NC}"

python manage.py runserver
