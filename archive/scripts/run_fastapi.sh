#!/bin/bash
set -a
source .env
set +a
uvicorn fastapi_app:app --host 0.0.0.0 --port=8000
