#!/bin/bash
# Usage: ./top10.sh logfile.log

LOGFILE="$1"

if [[ -z "$LOGFILE" || ! -f "$LOGFILE" ]]; then
  echo "Usage: $0 logfile"
  exit 1
fi

# Extract numbers ending with 'seconds', sort descending, take top 10
grep -oE '[0-9]+\.[0-9]+ seconds' "$LOGFILE" | \
  awk '{print $1}' | \
  sort -nr | \
  head -n 10
