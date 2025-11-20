# Running Full Requirements Generation for All Projects

## Quick Start

### Option 1: Using the Automated Script (Recommended)

```bash
source venv/bin/activate
./start_requirements_generation.sh 1
```

This will:
- Verify Weaviate connection
- Check indexed data
- Generate requirements for ALL 37 projects
- Run in background with logging

### Option 2: Direct Command

```bash
source venv/bin/activate
nohup python main.py requirements --all-projects --use-crewai > "log_start_requirements_generationj_$(date +'%Y-%m-%d_%H-%M-%S').log" 2>&1 &
```

### Option 3: Using the Script with Nohup (Recommended)

```bash
source venv/bin/activate
nohup ./start_requirements_generation.sh 1 > "log_start_requirements_generationj_$(date +'%Y-%m-%d_%H-%M-%S').log" 2>&1 &
```

## What Projects Will Be Processed

Based on your Weaviate data, the following 37 projects will be processed:

1. PastExport
2. administration.ui
3. axis2
4. cuco
5. cuco-cct-core
6. cuco-core
7. cuco-core-test
8. cuco-ui-admin
9. cuco-ui-app
10. cuco-ui-cct
11. cuco-ui-cct-a1bn
12. cuco-ui-cct-a1cml
13. cuco-ui-cct-a1ps
14. cuco-ui-cct-a1tvres
15. cuco-ui-cct-a1voip
16. cuco-ui-cct-bfw
17. cuco-ui-cct-bi
18. cuco-ui-cct-ccs
19. cuco-ui-cct-common
20. cuco-ui-cct-etgt
21. cuco-ui-cct-marketingproduct
22. cuco-ui-cct-pshc
23. cuco-ui-common
24. cuco-ui-mycuco
25. cuco-ui-pkb
26. cuco-ui-visitreports
27. cuco.test.dao
28. cuco.test.service
29. framework.test.dao
30. framework.ui
31. pkb-core
32. pkb-ui-common
33. pkb.dbmaintain
34. pkb.offerserver
35. pkb.test.dao
36. pkb.test.service
37. pkb.ui

## Prerequisites

### 1. Verify Weaviate is Running

```bash
curl http://localhost:8080/v1/meta
```

Or use the stats script:
```bash
./weaviate_stats.sh
```

### 2. Verify Data is Indexed

```bash
./weaviate_stats.sh | grep "Total Objects"
```

Should show: **Total Objects: 10,495+** (at minimum)

### 3. Verify Ollama is Running

```bash
curl http://localhost:11434/api/tags
```

### 4. Check Available Disk Space

Requirements generation will create many files. Ensure you have sufficient space:

```bash
df -h .
```

## Execution Steps

### Step 1: Start the Generation

```bash
cd /path/to/gha1javarag
source venv/bin/activate

# Start generation for all projects
./start_requirements_generation.sh 1
```

Or manually:
```bash
nohup python main.py requirements --all-projects --use-crewai > "logprod_crewai_$(date +'%Y-%m-%d_%H-%M-%S').log" 2>&1 &
```

### Step 2: Monitor Progress

**Find the log file:**
```bash
ls -lt log_start_requirements_generationj_*.log | head -1
```

**Watch in real-time:**
```bash
tail -f log_start_requirements_generationj_*.log
```

**Check current project being processed:**
```bash
tail -f log_start_requirements_generationj_*.log | grep -E "Processing project|Starting CrewAI|CrewAI requirements generation complete"
```

**Check for errors:**
```bash
tail -f log_start_requirements_generationj_*.log | grep -i error
```

### Step 3: Check Progress Periodically

**Count completed projects:**
```bash
# Count how many requirements files have been created
ls -1 output/*_crewai_requirements.md 2>/dev/null | wc -l

# Should eventually reach 37 (or close to it)
```

**Check which projects are done:**
```bash
ls -1 output/*_crewai_requirements.md | sed 's|output/||' | sed 's|_crewai_requirements.md||' | sort
```

**Check file sizes (larger = more detailed):**
```bash
ls -lhS output/*_crewai_requirements.md | head -10
```

## Time Estimates

### Per Project:
- **Small projects** (PastExport, etc.): 10-20 minutes
- **Medium projects** (cuco-ui-cct-*): 20-40 minutes
- **Large projects** (cuco-core, cuco-ui-app): 40-60 minutes

### Total Time:
- **All 37 projects**: **8-15 hours** (depending on project sizes and Ollama response time)
- **Top 10 projects**: **3-5 hours**

## Monitoring Commands

### Check if Process is Running

```bash
ps aux | grep "main.py requirements" | grep -v grep
```

### Check System Resources

```bash
# CPU and Memory usage
top -p $(pgrep -f "main.py requirements")

# Or simpler
htop
```

### Check Log File Size

```bash
ls -lh log_start_requirements_generationj_*.log
```

### Count Tool Calls (to verify agents are working)

```bash
grep -c "search_weaviate\|read_source_file" log_start_requirements_generationj_*.log
```

## Expected Output

### Output Files Location

```
output/
├── PastExport_crewai_requirements.md
├── cuco-core_crewai_requirements.md
├── cuco-ui-app_crewai_requirements.md
├── cuco-ui-cct-bi_crewai_requirements.md
└── ... (37 total files)
```

### Output File Structure

Each requirements file should contain:

1. **Executive Summary**
2. **Project Overview**
3. **Frontend Requirements (Next.js + React)**
   - Pages and Routes
   - UI Components
   - State Management
   - API Integration
   - User Experience
4. **Backend Requirements (NestJS + PostgreSQL)**
   - API Layer
   - Service Layer
   - Data Access Layer
   - Database Schema
   - Business Logic
5. **Integration Requirements**
6. **Technical Architecture**
7. **Non-Functional Requirements**
8. **Traceability Matrix**

### Quality Checks

After completion, verify quality:

```bash
# Check for placeholders (should be zero)
for file in output/*_crewai_requirements.md; do
    count=$(grep -ci "placeholder\|unable to retrieve\|needs to be identified" "$file" || echo "0")
    if [ "$count" -gt 0 ]; then
        echo "$file: $count placeholders found"
    fi
done

# Check for specific details (should have many)
for file in output/*_crewai_requirements.md; do
    count=$(grep -cE "\.java|\.jsp|\.xml|/mnt/" "$file" || echo "0")
    echo "$(basename $file): $count file references"
done

# Check file sizes (should be substantial)
ls -lhS output/*_crewai_requirements.md
```

## Troubleshooting

### If Process Stops

1. **Check for errors:**
   ```bash
   grep -i "error\|exception\|failed" log_start_requirements_generationj_*.log | tail -20
   ```

2. **Check if Ollama is still running:**
   ```bash
   curl http://localhost:11434/api/tags
   ```

3. **Check if Weaviate is still accessible:**
   ```bash
   curl http://localhost:8080/v1/meta
   ```

4. **Resume from where it stopped:**
   ```bash
   # Find which projects are already done
   DONE=$(ls -1 output/*_crewai_requirements.md | sed 's|output/||' | sed 's|_crewai_requirements.md||')
   
   # Run for remaining projects manually
   # (You'll need to modify the script or run individually)
   ```

### If Running Out of Memory

```bash
# Check memory usage
free -h

# If needed, process projects in batches
# Process top 10 first, then continue with rest
```

### If Taking Too Long

- Check Ollama response time
- Consider processing in batches (top 10, then rest)
- Check system resources (CPU, memory, disk I/O)

## Alternative: Process in Batches

If you want to process in smaller batches:

### Batch 1: Top 10 Projects

```bash
TOP_PROJECTS=(
    "cuco-core"
    "cuco-ui-app"
    "cuco-ui-common"
    "cuco-ui-admin"
    "pkb-core"
    "cuco-ui-visitreports"
    "cuco-ui-cct-bi"
    "administration.ui"
    "cuco-cct-core"
    "pkb-ui-common"
)

for project in "${TOP_PROJECTS[@]}"; do
    echo "Processing $project..."
    python main.py requirements --project "$project" --use-crewai
done
```

### Batch 2: Remaining Projects

```bash
# After batch 1 completes, continue with remaining projects
python main.py requirements --all-projects --use-crewai
```

## Completion Verification

After all projects are processed:

```bash
# 1. Count output files
echo "Total requirements files: $(ls -1 output/*_crewai_requirements.md 2>/dev/null | wc -l)"

# 2. Check total size
du -sh output/

# 3. Verify no placeholders
echo "Files with placeholders:"
grep -l -i "placeholder\|unable to retrieve" output/*_crewai_requirements.md || echo "None - all good!"

# 4. List all generated files
ls -lh output/*_crewai_requirements.md | awk '{print $9, $5}'
```

## Next Steps After Completion

1. **Review sample requirements files** to verify quality
2. **Share with development teams** for review
3. **Use for migration planning** and estimation
4. **Update as codebase evolves**

## Summary

**To run full requirements generation:**

```bash
source venv/bin/activate
./start_requirements_generation.sh 1
```

**Monitor with:**
```bash
tail -f logprod_crewai_*.log
```

**Check progress:**
```bash
ls -1 output/*_crewai_requirements.md | wc -l
```

**Expected time:** 8-15 hours for all 37 projects

**Expected output:** 37 detailed requirements files with zero placeholders

