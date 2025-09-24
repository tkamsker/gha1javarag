#!/usr/bin/env bash
# Kill all bash+script processes attached to a TTY (default: current TTY),
# including all their descendants. Skips the interactive "-bash" login shell.

set -Eeuo pipefail

# TTY to target, e.g. "pts/0". Default: your current TTY (if available).
TARGET_TTY="${1:-$(/usr/bin/tty 2>/dev/null | sed -E 's#^/dev/##' || true)}"
if [[ -z "${TARGET_TTY:-}" ]]; then
  echo "Could not determine current TTY. Pass one explicitly, e.g.: $0 pts/0"
  exit 1
fi

echo "Target TTY: $TARGET_TTY"

# Find candidate PIDs: rows where TTY matches and command starts with /bin/bash or /usr/bin/bash,
# but NOT the interactive login shell "-bash".
mapfile -t PIDS < <(
  ps -ax -o pid=,tty=,args= \
  | awk -v tty="$TARGET_TTY" '
      $2 == tty {
        cmd=""; for (i=3; i<=NF; i++) cmd = cmd $i " ";
        if (cmd ~ /^-bash(\s|$)/) next;                                     # skip login shell
        if (cmd ~ /^((\/usr)?\/bin\/bash)(\s|$)/) print $1;                 # only bash+script
      }' \
  | sort -n | uniq
)

if ((${#PIDS[@]} == 0)); then
  echo "No bash script processes found on $TARGET_TTY."
  exit 0
fi

echo "Found candidate PIDs: ${PIDS[*]}"

kill_tree() {
  local pid="$1"

  # Recurse into children first
  local kids
  kids=$(pgrep -P "$pid" || true)
  for k in $kids; do
    kill_tree "$k"
  done

  if kill -0 "$pid" 2>/dev/null; then
    echo "TERM $pid  ($(ps -p "$pid" -o args=))"
    kill -TERM "$pid" 2>/dev/null || true

    # Wait up to 5 seconds for graceful exit
    for _ in 1 2 3 4 5; do
      sleep 1
      if ! kill -0 "$pid" 2>/dev/null; then
        break
      fi
    done

    if kill -0 "$pid" 2>/dev/null; then
      echo "KILL $pid"
      kill -KILL "$pid" 2>/dev/null || true
    fi
  fi
}

for pid in "${PIDS[@]}"; do
  kill_tree "$pid"
done

echo "Done."
