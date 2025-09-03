#!/bin/sh
set -e

# Wait for PostgreSQL to be ready
sleep 10

alembic upgrade head

echo "Starting FastAPI..."
exec uvicorn src.main:app --host 0.0.0.0 --port 8000