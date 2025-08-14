#!/bin/bash
# 2025.08.14 Run all enhanced analysis scripts and then stop machine 
# Exit on error
set -e

# Function to format seconds into human readable time
format_duration() {
    local seconds=$1
    local hours=$((seconds / 3600))
    local minutes=$(((seconds % 3600) / 60))
    local secs=$((seconds % 60))
    printf "%02d:%02d:%02d" $hours $minutes $secs
}

# Record start time
START_TIME_EPOCH=$(date +%s)
START_TIME_FORMATTED=$(date +"%Y-%m-%d %H:%M:%S")

echo "🚀 Enhanced Analysis Job Started"
echo "================================="
echo "Start Date: $(date +"%Y-%m-%d")"
echo "Start Time: $(date +"%H:%M:%S")"
echo "Start Timestamp: $START_TIME_FORMATTED"
echo ""

# Run the main enhanced analysis
echo "📊 Running enhanced analysis pipeline..."
./all_stepps_enhanced.sh

# Record end time
END_TIME_EPOCH=$(date +%s)
END_TIME_FORMATTED=$(date +"%Y-%m-%d %H:%M:%S")

# Calculate duration
TOTAL_DURATION_SECONDS=$((END_TIME_EPOCH - START_TIME_EPOCH))
DURATION_FORMATTED=$(format_duration $TOTAL_DURATION_SECONDS)

echo ""
echo "🎉 Enhanced Analysis Job Completed"
echo "=================================="
echo "End Date: $(date +"%Y-%m-%d")"
echo "End Time: $(date +"%H:%M:%S")"
echo "End Timestamp: $END_TIME_FORMATTED"
echo ""
echo "⏱️  Job Duration:"
echo "   Total Seconds: $TOTAL_DURATION_SECONDS"
echo "   Formatted Time: $DURATION_FORMATTED (HH:MM:SS)"
echo "   Hours: $((TOTAL_DURATION_SECONDS / 3600))"
echo "   Minutes: $(((TOTAL_DURATION_SECONDS % 3600) / 60))"
echo "   Seconds: $((TOTAL_DURATION_SECONDS % 60))"
echo ""

# Wait before shutting down
echo "⏳ Waiting 60 seconds before shutdown..."
sleep 60

# Stop the machine
echo "🔌 Shutting down machine..."
curl -X POST -H "Content-Type: application/json" https://ccf-api.nonprod.at.cloud.inside/v1/exoscalevm/at-cuc-vm-vlcucad001-eatnl/stop -u tneusser:2DnEwsJ9r6ljnfp5

echo "✅ Shutdown command sent successfully"

