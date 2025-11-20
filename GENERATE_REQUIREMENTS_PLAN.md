# Generate Detailed Requirements - Complete Plan

## Current Status ✅

- ✅ Search is working correctly
- ✅ 226,406 DaoCall objects indexed
- ✅ 495 IbatisStatement objects indexed
- ✅ 36,453 total artifacts indexed
- ✅ Project filtering works
- ✅ Enhanced CrewAI prompts ready
- ✅ Metadata support enabled

## Pre-Flight Checklist

Before generating requirements, verify everything is ready:

### 1. Verify Data is Indexed

```bash
source venv/bin/activate
./weaviate_stats.sh
```

**Expected:**
- Total Objects: 36,000+
- All classes have data
- Projects are correctly named

### 2. Test Search Works

```bash
# Test search with project filter
python main.py search --query 'dao' --project 'cuco-core' --limit 5

# Test search across all projects
python main.py search --query 'dao' --all --limit 5
```

**Expected:** Results should be returned

### 3. Check CrewAI is Installed

```bash
pip show crewai
```

**Expected:** Version 0.203.1 or compatible

## Step-by-Step Requirements Generation

### Option A: Generate for All Projects (Recommended)

This will generate requirements for all 38 projects found in your artifacts.

```bash
source venv/bin/activate

# Generate requirements for all projects using CrewAI
nohup python main.py requirements --all-projects --use-crewai > "logprod_crewai_$(date +'%Y-%m-%d_%H-%M-%S').log" 2>&1 &
```

**Time:** 1-3 hours for all projects
**Output:** Requirements files in `output/` directory

### Option B: Generate for Specific Projects

If you want to test with a few projects first:

```bash
# Generate for one project
python main.py requirements --project 'cuco-core' --use-crewai

# Generate for multiple projects (run separately)
python main.py requirements --project 'PastExport' --use-crewai
python main.py requirements --project 'cuco-ui-cct-a1voip' --use-crewai
```

**Time:** 10-30 minutes per project

### Option C: Generate for Top Projects Only

Generate for the most important projects:

```bash
# Top projects by artifact count
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
    echo "Generating requirements for $project..."
    python main.py requirements --project "$project" --use-crewai
done
```

## Monitoring Progress

### Check Log File

```bash
# Find the latest log file
ls -lt logprod_crewai_*.log | head -1

# Monitor in real-time
tail -f logprod_crewai_*.log

# Check for errors
grep -i error logprod_crewai_*.log

# Check progress
grep "CrewAI requirements generation complete" logprod_crewai_*.log
```

### Check Output Files

```bash
# List generated requirements
ls -lh output/*_crewai_requirements.md

# Check file sizes (larger = more detailed)
ls -lhS output/*_crewai_requirements.md | head -10

# Preview a requirements file
head -100 output/cuco-core_crewai_requirements.md
```

### Monitor System Resources

```bash
# Check if process is running
ps aux | grep "main.py requirements"

# Check system load
top

# Check Weaviate/Ollama are running
docker ps | grep -E "weaviate|ollama"
```

## Expected Output

### Requirements File Structure

Each requirements file should contain:

1. **Executive Summary**
   - Project overview
   - Key findings

2. **Project Overview**
   - Project description
   - Technology stack
   - Architecture overview

3. **Functional Requirements** (organized by area)
   - Backend Architecture
   - Database Layer
   - Data Flow and Business Logic
   - Technical Architecture Patterns
   - Integration Points

4. **Technical Requirements**
   - Dependencies
   - Build configurations
   - Runtime requirements

5. **UI Specifications**
   - Forms and User Input
   - Navigation Flows
   - UI Components
   - User Roles and Permissions

6. **Database Schema**
   - Tables and relationships
   - SQL statements

7. **API Contracts**
   - Service interfaces
   - Endpoints

8. **Non-Functional Requirements**
   - Performance
   - Security
   - Scalability

9. **Traceability Matrix**
   - Links to source artifacts
   - File paths
   - Class names

### Quality Indicators

Good requirements files should have:
- ✅ **Detailed sections** (not generic)
- ✅ **Specific examples** with file paths
- ✅ **Class names and method signatures**
- ✅ **SQL statement IDs**
- ✅ **Metadata context**
- ✅ **Traceability links**

## Troubleshooting

### If Requirements are Still Generic

1. **Check if search is finding results:**
   ```bash
   python main.py search --query 'dao' --project 'cuco-core' --limit 5
   ```

2. **Check CrewAI logs for errors:**
   ```bash
   grep -i "error\|exception\|failed" logprod_crewai_*.log
   ```

3. **Verify metadata is stored:**
   ```bash
   python diagnose_indexing.py
   ```

### If Generation is Too Slow

1. **Generate for fewer projects at once**
2. **Check Ollama is running and responsive:**
   ```bash
   curl http://localhost:11434/api/tags
   ```
3. **Consider using a faster model** (if available)

### If Generation Fails

1. **Check timeout settings** (currently 20 minutes per agent)
2. **Check Weaviate is accessible:**
   ```bash
   curl http://localhost:8080/v1/meta
   ```
3. **Check Ollama is accessible:**
   ```bash
   curl http://localhost:11434/api/tags
   ```

## Post-Generation Verification

After generation completes:

### 1. Check All Files Were Created

```bash
# Count generated files
ls -1 output/*_crewai_requirements.md | wc -l

# Should match number of projects (or close to it)
```

### 2. Verify Content Quality

```bash
# Check file sizes (should be substantial)
ls -lhS output/*_crewai_requirements.md

# Check for detailed content
grep -l "Backend Architecture Analysis" output/*_crewai_requirements.md
grep -l "Traceability Matrix" output/*_crewai_requirements.md
```

### 3. Review Sample Requirements

```bash
# Review a sample file
cat output/cuco-core_crewai_requirements.md | head -200

# Check for specific examples
grep -E "\.java|\.xml|\.jsp" output/cuco-core_crewai_requirements.md | head -20
```

## Next Steps After Generation

1. **Review requirements files** for quality
2. **Compare with previous versions** (if any)
3. **Use for development planning**
4. **Share with development teams**
5. **Update as codebase evolves**

## Quick Start Command

For immediate start with all projects:

```bash
source venv/bin/activate && \
nohup python main.py requirements --all-projects --use-crewai > "logprod_crewai_$(date +'%Y-%m-%d_%H-%M-%S').log" 2>&1 & \
echo "Requirements generation started. Monitor with: tail -f logprod_crewai_*.log"
```

## Estimated Timeline

- **Per Project:** 10-30 minutes
- **All 38 Projects:** 1-3 hours
- **Top 10 Projects:** 2-5 hours

Time depends on:
- Number of artifacts per project
- Complexity of codebase
- Ollama response time
- System resources

