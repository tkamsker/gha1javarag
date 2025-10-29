#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if [ -d "venv" ]; then
  # shellcheck disable=SC1091
  source venv/bin/activate
fi

export PYTHONPATH=.

# Use defaults from .env; ensure broad globs for full run
export JAVA_INCLUDE_GLOBS="${JAVA_INCLUDE_GLOBS:-**/*.java}"
export JSP_INCLUDE_GLOBS="${JSP_INCLUDE_GLOBS:-**/*.jsp,**/*.jspf}"
export JS_INCLUDE_GLOBS="${JS_INCLUDE_GLOBS:-**/*.js}"
export GWT_INCLUDE_GLOBS="${GWT_INCLUDE_GLOBS:-**/*.gwt.xml,**/*.ui.xml,**/*EntryPoint*.java,**/*Activity*.java,**/*Place*.java,**/*Service*.java,**/*RequestFactory*.java}"
export HTML_INCLUDE_GLOBS="${HTML_INCLUDE_GLOBS:-**/*.htm,**/*.html}"
export XML_INCLUDE_GLOBS="${XML_INCLUDE_GLOBS:-**/*.xml,**/*.xhtml}"
export SQL_INCLUDE_GLOBS="${SQL_INCLUDE_GLOBS:-**/*.sql}"

export LOG_LEVEL="${LOG_LEVEL:-INFO}"

echo "[run_full] Validating setup..."
python validate_setup.py || true

echo "[run_full] Starting pipeline (full run)..."
python main.py 2>&1 | tee data/output/logs/pipeline_full.log

echo "[run_full] Done. Key outputs:"
echo "  - data/output/pipeline_summary.json"
echo "  - data/output/*/requirements.md"
echo "  - data/output/*/mapping.md"


