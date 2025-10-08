#!/bin/bash

# =============================
# Step 3: Detailed Requirements Generation
# =============================

set -e

BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

info(){ echo -e "${BLUE}[INFO]${NC} $1"; }
ok(){ echo -e "${GREEN}[SUCCESS]${NC} $1"; }
err(){ echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

if [ -z "$VIRTUAL_ENV" ]; then
  err "No virtual environment detected. Activate with: source venv/bin/activate"
fi

PROJECT=${1:-}
if [ -z "$PROJECT" ]; then
  err "Usage: ./step3_requirements.sh <project_name>"
fi

info "Generating detailed requirements for project: $PROJECT"
python main.py requirements --project "$PROJECT"
ok "Requirements generated"
echo "Index: data/output/requirements/$PROJECT/INDEX.md"

