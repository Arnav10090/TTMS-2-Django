#!/bin/bash

set -e

echo "=================================================="
echo "Loading Sample Data for TTMS and PTMS"
echo "=================================================="

PROJECT_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)

TTMS_CONTAINER="ttms_app"
PTMS_CONTAINER="ptms_app"

echo ""
echo "📊 Loading TTMS Sample Data..."
if docker-compose -f "$PROJECT_ROOT/Docker/docker-compose.yml" exec -T "$TTMS_CONTAINER" python manage.py loaddata ttms/fixtures/sample_data.json; then
    echo "✅ TTMS sample data loaded successfully!"
else
    echo "❌ Failed to load TTMS sample data"
    exit 1
fi

echo ""
echo "📊 Loading PTMS Sample Data..."
if docker-compose -f "$PROJECT_ROOT/Docker/docker-compose.yml" exec -T "$PTMS_CONTAINER" python manage.py loaddata ptms/fixtures/sample_data.json; then
    echo "✅ PTMS sample data loaded successfully!"
else
    echo "❌ Failed to load PTMS sample data"
    exit 1
fi

echo ""
echo "=================================================="
echo "✅ All sample data loaded successfully!"
echo "=================================================="
echo ""
echo "Next steps:"
echo "1. Access TTMS API: http://localhost:8000/api/ttms/"
echo "2. Access PTMS API: http://localhost:8001/api/ptms/"
echo "3. Check dashboard for populated data"
echo ""
