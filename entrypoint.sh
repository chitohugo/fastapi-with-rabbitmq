#!/bin/sh
set -e

# alembic revision --autogenerate -m "Initial"
alembic upgrade head
uvicorn main:app --workers 4 --reload --host 0.0.0.0
