#!/bin/bash
set -a
source .env
set +a
export FLASK_APP=flask_app.py
export FLASK_ENV=development
export TOKENIZERS_PARALLELISM=false
python3 -m flask run --host=0.0.0.0 --port=8000
