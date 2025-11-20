# Step-by-Step Reload and Improvement Plan

## Summary of Improvements

### ✅ Completed Improvements

1. **Metadata Storage**: `meta` field now stored in Weaviate as JSON
2. **Enhanced CrewAI Prompts**: More detailed, area-specific requirements
3. **Enhanced Search Tool**: Returns metadata in results
4. **Search Enhancement**: Added `--all` flag for cross-project search

## Step-by-Step Execution Plan

### Step 1: Reload All Data

Run the automated reload script:

```bash
./reload_all_data.sh
```

This will:
1. ✅ Check Weaviate connection
2. ✅ Clear existing Weaviate data
3. ✅ Fix project names in artifacts
4. ✅ Re-index all artifacts with metadata
5. ✅ Verify indexing worked
6. ✅ Test searches

**Time:** 5-15 minutes

### Step 2: Verify Metadata is Stored

```bash
./weaviate_stats.sh
```

**Check for:**
- Total objects > 0 (should be 13,000+)
- All classes have data
- Projects are correctly named

### Step 3: Test Search with Metadata

```bash
# Test search with project filter
python main.py search --query "dao" --project "cuco-core"

# Test search across all projects
python main.py search --query "dao" --all
```

**Expected:** Results should show metadata information

### Step 4: Generate Requirements with Enhanced CrewAI

```bash
# Generate for all projects (background)
nohup python main.py requirements --all-projects --use-crewai > "logprod_crewai_$(date +'%Y-%m-%d_%H-%M-%S').log" 2>&1 &
```

**What's improved:**
- More detailed analysis (5-6 sections per analyst)
- Area-specific organization
- Metadata context included
- Better traceability

**Time:** 1-3 hours for all projects

### Step 5: Monitor Requirements Generation

```bash
# Watch the log
tail -f logprod_crewai_*.log

# Check progress
grep "CrewAI requirements generation complete" logprod_crewai_*.log
```

### Step 6: Review Generated Requirements

```bash
# List generated files
ls -la output/*_crewai_requirements.md

# Review a sample
head -200 output/cuco-core_crewai_requirements.md
```

**Expected improvements:**
- Detailed sections organized by functional areas
- Specific file paths, class names, SQL statement IDs
- Metadata context in analysis
- Traceability links
- Professional structure

## Quick Reference Commands

```bash
# Complete reload
./reload_all_data.sh

# Check what's indexed
./weaviate_stats.sh

# Test search
python main.py search --query "dao" --all

# Generate requirements
python main.py requirements --all-projects --use-crewai
```

## Expected Results

After completing all steps:

- ✅ **13,000+ artifacts** indexed with metadata
- ✅ **30+ projects** with correct names
- ✅ **Detailed requirements** organized by areas
- ✅ **Metadata preserved** and used in analysis
- ✅ **Traceability** links to source artifacts

