#!/bin/bash
# Monitor overnight extraction progress

PID_FILE="output/gwt-validation/extract.pid"
LOG_FILE="output/gwt-validation/extract-overnight.log"

echo "=== GWT Extraction Monitor ==="
echo ""

# Check if PID file exists
if [ ! -f "$PID_FILE" ]; then
    echo "❌ PID file not found: $PID_FILE"
    exit 1
fi

# Read PID
PID=$(cat "$PID_FILE")
echo "Process ID: $PID"

# Check if process is running
if ps -p $PID > /dev/null 2>&1; then
    echo "✅ Status: RUNNING"
else
    echo "⚠️  Status: COMPLETED or STOPPED"
fi

echo ""
echo "=== Progress ==="

# Count lines in log (rough progress indicator)
if [ -f "$LOG_FILE" ]; then
    LOG_LINES=$(wc -l < "$LOG_FILE")
    echo "Log lines: $LOG_LINES"

    # Extract progress from log
    PROGRESS=$(grep -E "Progress: [0-9]+/183" "$LOG_FILE" | tail -1)
    if [ ! -z "$PROGRESS" ]; then
        echo "Latest: $PROGRESS"
    fi

    # Count errors
    ERROR_COUNT=$(grep -c "ERROR" "$LOG_FILE" || echo "0")
    echo "Errors: $ERROR_COUNT"

    # Count UiBinder successes
    UIBINDER_COUNT=$(grep -c "Extracting gwt_ui_binder" "$LOG_FILE" || echo "0")
    UIBINDER_ERRORS=$(grep -c "ERROR.*ui.xml" "$LOG_FILE" || echo "0")
    echo "UiBinder files processed: $UIBINDER_COUNT (errors: $UIBINDER_ERRORS)"
fi

echo ""
echo "=== Timing ==="

# Get start time
if [ -f "output/gwt-validation/timing.txt" ]; then
    START_TIME=$(grep "Start timestamp:" output/gwt-validation/timing.txt | tail -1 | awk '{print $3}')
    if [ ! -z "$START_TIME" ]; then
        CURRENT_TIME=$(date +%s)
        ELAPSED=$((CURRENT_TIME - START_TIME))
        MINUTES=$((ELAPSED / 60))
        SECONDS=$((ELAPSED % 60))
        echo "Running time: ${MINUTES}m ${SECONDS}s"

        # Estimate completion
        if [ ! -z "$PROGRESS" ]; then
            CURRENT=$(echo "$PROGRESS" | grep -oE "[0-9]+/183" | cut -d'/' -f1)
            if [ "$CURRENT" -gt 0 ]; then
                TIME_PER_FILE=$((ELAPSED / CURRENT))
                REMAINING=$((183 - CURRENT))
                EST_SECONDS=$((REMAINING * TIME_PER_FILE))
                EST_MINUTES=$((EST_SECONDS / 60))
                echo "Estimated time remaining: ~${EST_MINUTES} minutes"

                # Calculate ETA
                ETA_TIMESTAMP=$((CURRENT_TIME + EST_SECONDS))
                ETA_TIME=$(date -r $ETA_TIMESTAMP "+%Y-%m-%d %H:%M:%S")
                echo "Estimated completion: $ETA_TIME"
            fi
        fi
    fi
fi

echo ""
echo "=== Recent Activity ==="
tail -20 "$LOG_FILE" | grep -E "INFO|ERROR|Progress" | tail -10

echo ""
echo "=== Quick Commands ==="
echo "  Full log:        tail -f $LOG_FILE"
echo "  Check errors:    grep ERROR $LOG_FILE | tail -20"
echo "  Check progress:  grep 'Progress:' $LOG_FILE"
echo "  Stop process:    kill $PID"
echo ""
