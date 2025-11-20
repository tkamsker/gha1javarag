#!/bin/bash
# Nohup wrapper for requirements generation
# 
# Usage:
#   ./run_requirements_nohup.sh [MODE] [PROJECTS...]
#
# Examples:
#   ./run_requirements_nohup.sh 1                    # All projects
#   ./run_requirements_nohup.sh 2 cuco-core PastExport  # Specific projects
#   ./run_requirements_nohup.sh 3                    # Top 10 projects

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

LOG_FILE="nohup_requirements_$(date +'%Y-%m-%d_%H-%M-%S').log"

echo "Starting requirements generation in background..."
echo "Log file: $LOG_FILE"
echo "Command: ./start_requirements_generation.sh $@"
echo ""

nohup ./start_requirements_generation.sh "$@" > "$LOG_FILE" 2>&1 &
PID=$!

echo "Process started with PID: $PID"
echo "Monitor with: tail -f $LOG_FILE"
echo "Check status with: ps -p $PID"
echo ""
echo "To stop: kill $PID"

