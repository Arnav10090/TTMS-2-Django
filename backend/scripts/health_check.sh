#!/bin/bash

set +e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "=============================================="
echo "System Health Check"
echo "=============================================="
echo ""

check_service() {
    local service_name=$1
    local port=$2
    local url=$3
    
    echo -n "Checking $service_name ($port) ... "
    
    if nc -z localhost "$port" 2>/dev/null; then
        echo -e "${GREEN}✅ RUNNING${NC}"
        
        if [ ! -z "$url" ]; then
            response=$(curl -s -o /dev/null -w "%{http_code}" "$url")
            if [ "$response" == "200" ] || [ "$response" == "404" ]; then
                echo "  └─ HTTP Response: ${GREEN}$response${NC}"
            else
                echo "  └─ HTTP Response: ${YELLOW}$response${NC}"
            fi
        fi
        return 0
    else
        echo -e "${RED}❌ NOT RUNNING${NC}"
        return 1
    fi
}

check_container() {
    local container_name=$1
    
    echo -n "Checking Docker container: $container_name ... "
    
    if docker ps --filter "name=$container_name" --filter "status=running" | grep -q "$container_name"; then
        echo -e "${GREEN}✅ RUNNING${NC}"
        return 0
    elif docker ps -a --filter "name=$container_name" | grep -q "$container_name"; then
        echo -e "${YELLOW}⚠️  EXISTS BUT NOT RUNNING${NC}"
        return 1
    else
        echo -e "${RED}❌ NOT FOUND${NC}"
        return 1
    fi
}

echo "${BLUE}Docker Containers:${NC}"
echo "---"
check_container "ttms_app"
check_container "ptms_app"
check_container "ttms_postgres"
check_container "ptms_postgres"

echo ""
echo "${BLUE}Services & Databases:${NC}"
echo "---"
check_service "TTMS PostgreSQL" "5432" ""
check_service "PTMS PostgreSQL" "5433" ""
check_service "TTMS Django API" "8000" "http://localhost:8000/api/ttms/health/"
check_service "PTMS Django API" "8001" "http://localhost:8001/api/ptms/health/"

echo ""
echo "${BLUE}Database Connections:${NC}"
echo "---"

check_db_connection() {
    local db_name=$1
    local port=$2
    local user=${3:-postgres}
    local password=${4:-postgres}
    
    echo -n "TTMS Database ($db_name) ... "
    
    PGPASSWORD="$password" psql -h localhost -p "$port" -U "$user" -d "$db_name" -c "SELECT 1;" &>/dev/null
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ CONNECTED${NC}"
    else
        echo -e "${RED}❌ FAILED${NC}"
    fi
}

echo ""
echo "${BLUE}API Endpoint Verification:${NC}"
echo "---"

check_api_endpoint() {
    local endpoint=$1
    local port=$2
    local description=$3
    
    echo -n "$description ... "
    
    response=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:$port$endpoint")
    
    if [ "$response" == "200" ] || [ "$response" == "404" ]; then
        echo -e "${GREEN}✅ HTTP $response${NC}"
    elif [ "$response" == "000" ]; then
        echo -e "${RED}❌ Connection Failed${NC}"
    else
        echo -e "${YELLOW}⚠️  HTTP $response${NC}"
    fi
}

check_api_endpoint "/api/ttms/kpi/" "8000" "TTMS KPI Endpoint"
check_api_endpoint "/api/ttms/vehicles/" "8000" "TTMS Vehicles Endpoint"
check_api_endpoint "/api/ttms/alerts/" "8000" "TTMS Alerts Endpoint"
check_api_endpoint "/api/ptms/projects/" "8001" "PTMS Projects Endpoint"
check_api_endpoint "/api/ptms/tasks/" "8001" "PTMS Tasks Endpoint"

echo ""
echo "=============================================="
echo "Health Check Complete"
echo "=============================================="
echo ""
echo "To start services if not running:"
echo "  cd backend/Docker && docker-compose up -d"
echo ""
echo "To load sample data:"
echo "  cd backend && bash scripts/load_sample_data.sh"
echo ""
echo "To test APIs:"
echo "  bash backend/scripts/test_ttms_api.sh"
echo "  bash backend/scripts/test_ptms_api.sh"
echo ""
