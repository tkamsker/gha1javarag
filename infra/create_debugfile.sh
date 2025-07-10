#!/usr/bin/env bash
#
# list_source_files.sh
# --------------------
# Usage:  ./list_source_files.sh [DIRECTORY]
# If no DIRECTORY is supplied, the current working directory is used.
#
# Example:
#   ./list_source_files.sh ~/projects/legacy-app > source_files.txt
#
# The script works on stock macOS (Bash or Zsh).  It tries to use `realpath`
# (available on macOS 12+ or via Homebrew coreutils).  If that’s missing,
# it falls back to `greadlink -f` (coreutils) and finally to Python 3,
# which is bundled with modern macOS versions.

set -euo pipefail

# Resolve the target directory to an absolute path
TARGET_DIR=${1:-"."}
TARGET_DIR=$(cd "$TARGET_DIR" && pwd)

# 1. Collect matching files with `find`
file_list=$(find "$TARGET_DIR" -type f \
  \( -iname "*.java" -o -iname "*.xml" -o -iname "*.html" -o -iname "*.jsp" -o -iname "*.sql" \))

# 2. Convert each path to an absolute form if necessary
if command -v realpath >/dev/null 2>&1; then
  # macOS 12+ or coreutils realpath
  echo "$file_list" | while IFS= read -r f; do realpath "$f"; done
elif command -v greadlink >/dev/null 2>&1; then
  # coreutils greadlink (brew install coreutils)
  echo "$file_list" | while IFS= read -r f; do greadlink -f "$f"; done
else
  # Pure-Python fallback (Python 3 is available by default on macOS 12+)
  echo "$file_list" | /usr/bin/python3 - <<'PY'
import sys, pathlib
for line in sys.stdin:
    print(pathlib.Path(line.rstrip()).resolve())
PY
fi
