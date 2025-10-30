#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if [ -d "venv" ]; then
  # shellcheck disable=SC1091
  source venv/bin/activate
fi

export PYTHONPATH=.
export FORCE_MULTIPROJECT_DISCOVERY=true

# Override env for a small, fast run (limit to a couple Java files; skip others)
export JAVA_INCLUDE_GLOBS="**/ServiceDao.java,**/ServiceDaoImpl.java"
export JSP_INCLUDE_GLOBS=""
export JS_INCLUDE_GLOBS=""
export GWT_INCLUDE_GLOBS=""
export HTML_INCLUDE_GLOBS=""
export XML_INCLUDE_GLOBS=""
export SQL_INCLUDE_GLOBS=""

# Optional: quieter logging
export LOG_LEVEL="INFO"

echo "[run_small] Validating setup..."
python validate_setup.py || true

echo "[run_small] Starting pipeline (small run)..."
python main.py 2>&1 | tee data/output/logs/pipeline_small.log

echo "[run_small] Done. Key outputs:"
echo "  - data/output/pipeline_summary.json"
echo "  - data/output/*/requirements.md"
echo "  - data/output/*/mapping.md"


