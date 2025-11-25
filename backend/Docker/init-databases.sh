#!/bin/bash
# Database initialization script for TTMS and PTMS
# This script runs when PostgreSQL containers start for the first time

set -e

echo "Initializing databases..."

# Create TTMS database
psql -U postgres -c "
CREATE DATABASE IF NOT EXISTS ${TTMS_DB_NAME:-ttms_db}
  WITH ENCODING 'UTF-8'
  LOCALE 'en_US.UTF-8'
  TEMPLATE template0;
"

echo "✓ TTMS database created: ${TTMS_DB_NAME:-ttms_db}"

# Create PTMS database (if using same postgres)
# This line can be commented out if using separate postgres instances
# psql -U postgres -c "
# CREATE DATABASE IF NOT EXISTS ${PTMS_DB_NAME:-ptms_db}
#   WITH ENCODING 'UTF-8'
#   LOCALE 'en_US.UTF-8'
#   TEMPLATE template0;
# "

# echo "✓ PTMS database created: ${PTMS_DB_NAME:-ptms_db}"

# Grant privileges
psql -U postgres -c "
GRANT ALL PRIVILEGES ON DATABASE ${TTMS_DB_NAME:-ttms_db} TO ${DB_USER:-postgres};
"

echo "✓ Database initialization completed"
