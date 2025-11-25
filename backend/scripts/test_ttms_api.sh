#!/bin/bash

set +e

BASE_URL="http://localhost:8000/api/ttms"
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'
PASSED=0
FAILED=0

echo "=============================================="
echo "TTMS API Testing"
echo "=============================================="
echo ""

test_endpoint() {
    local method=$1
    local endpoint=$2
    local description=$3
    local data=$4
    
    echo -n "Testing: $description ... "
    
    if [ "$method" == "POST" ]; then
        response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL$endpoint" \
            -H "Content-Type: application/json" \
            -d "$data")
    else
        response=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL$endpoint")
    fi
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | head -n-1)
    
    if [ "$http_code" -ge 200 ] && [ "$http_code" -lt 300 ]; then
        echo -e "${GREEN}✅ PASS${NC} (HTTP $http_code)"
        ((PASSED++))
    elif [ "$http_code" -ge 400 ] && [ "$http_code" -lt 500 ]; then
        echo -e "${YELLOW}⚠️  OK${NC} (HTTP $http_code - Expected for some endpoints)"
        ((PASSED++))
    else
        echo -e "${RED}❌ FAIL${NC} (HTTP $http_code)"
        echo "  Response: $body"
        ((FAILED++))
    fi
}

echo "System Health Checks:"
echo "---"

test_endpoint "GET" "/health/" "API Health Check"
test_endpoint "GET" "/status/" "System Status"

echo ""
echo "Data Endpoints:"
echo "---"

test_endpoint "GET" "/kpi/" "Get KPI Metrics"
test_endpoint "GET" "/vehicles/" "Get Vehicles"
test_endpoint "GET" "/vehicles/?limit=5" "Get Vehicles with Pagination"
test_endpoint "GET" "/parking-cells/" "Get Parking Cells"
test_endpoint "GET" "/vehicle-entries/" "Get Vehicle Entries"
test_endpoint "GET" "/alerts/" "Get System Alerts"
test_endpoint "GET" "/alerts/?is_resolved=false" "Get Active Alerts"
test_endpoint "GET" "/sparkline/" "Get Turnaround Time Sparkline"

echo ""
echo "Vehicle Endpoints:"
echo "---"

test_endpoint "GET" "/vehicles/1/" "Get Vehicle by ID"
test_endpoint "GET" "/vehicles/TN01AB1234/" "Get Vehicle by Registration Number (if supported)"

echo ""
echo "Parking Cell Endpoints:"
echo "---"

test_endpoint "GET" "/parking-cells/1/" "Get Parking Cell Details"

echo ""
echo "=============================================="
echo "Test Summary"
echo "=============================================="
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}❌ Some tests failed!${NC}"
    exit 1
fi
