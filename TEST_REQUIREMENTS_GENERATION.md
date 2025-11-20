# Testing Requirements Generation

## Quick Test (Single Project)

Test with one project first to verify tools are being called:

```bash
source venv/bin/activate
python main.py requirements --project "PastExport" --use-crewai
```

## Monitor Execution

### Option 1: Watch Logs in Real-Time

```bash
# In one terminal, start the generation
python main.py requirements --project "PastExport" --use-crewai 2>&1 | tee test_pastexport.log

# Or run in background and tail the log
python main.py requirements --project "PastExport" --use-crewai > test_pastexport.log 2>&1 &
tail -f test_pastexport.log
```

### Option 2: Check for Tool Calls

Look for these indicators that tools are being called:

```bash
# Check if search_weaviate is being called
grep -i "search_weaviate\|searching weaviate\|found.*artifacts" test_pastexport.log

# Check if read_source_file is being called
grep -i "read_source_file\|reading source\|found.*file" test_pastexport.log

# Check for tool execution
grep -i "tool\|action\|calling" test_pastexport.log
```

## What to Look For

### ✅ Good Signs (Tools Are Working)

1. **Tool Calls in Logs:**
   ```
   INFO - Trying data_object.get for DaoCall with project filter
   INFO - data_object.get returned X objects for DaoCall
   INFO - Found X file(s) matching pattern
   ```

2. **Multiple Tool Calls:**
   - Should see multiple search_weaviate calls
   - Should see read_source_file calls if search fails
   - Agents should iterate multiple times (max_iter=20)

3. **Detailed Output:**
   - Requirements file should have specific file paths
   - Should include actual code examples
   - Should map to NestJS/Next.js architecture

### ❌ Bad Signs (Tools Not Working)

1. **No Tool Calls:**
   - Agents complete immediately
   - Only see "Final Answer" without tool execution
   - Logs show JSON-like text but no actual tool calls

2. **Generic Output:**
   - Requirements say "Due to inability to retrieve artifacts"
   - Placeholder text
   - No specific file paths or code examples

## Step-by-Step Test Procedure

### Step 1: Test Single Project

```bash
cd /path/to/gha1javarag
source venv/bin/activate

# Test with PastExport (small project, 51 DAO calls)
python main.py requirements --project "PastExport" --use-crewai 2>&1 | tee test_pastexport.log
```

### Step 2: Monitor Progress

While it's running, check:

```bash
# In another terminal
tail -f test_pastexport.log | grep -E "tool|search|read|Found|Agent"
```

### Step 3: Check Output

After completion:

```bash
# Check if requirements file was created
ls -lh output/PastExport_crewai_requirements.md

# Check file content
head -100 output/PastExport_crewai_requirements.md

# Look for specific details (should NOT have placeholders)
grep -i "placeholder\|unable to retrieve\|no results found" output/PastExport_crewai_requirements.md

# Should find actual file paths
grep -E "\.java|\.jsp|\.xml|/mnt/" output/PastExport_crewai_requirements.md | head -20
```

### Step 4: Verify Tool Usage

```bash
# Count tool calls in log
grep -c "search_weaviate\|read_source_file" test_pastexport.log

# Should see multiple calls (at least 5-10)
# Check for actual tool execution
grep -A 5 "search_weaviate\|read_source_file" test_pastexport.log | head -50
```

## Expected Behavior

### For PastExport Project:

1. **Backend Analyst should:**
   - Call search_weaviate for DaoCall artifacts (should find 51)
   - Call search_weaviate for IbatisStatement (should find 11)
   - Call read_source_file for *Dao.java files
   - Call read_source_file for *Service.java files
   - Generate detailed analysis with file paths

2. **Dependency Analyst should:**
   - Call read_source_file for pom.xml
   - Call search_weaviate for GwtModule
   - Generate dependency mapping

3. **Frontend Analyst should:**
   - Call read_source_file for *.jsp files
   - Call read_source_file for *Activity.java
   - Call read_source_file for *Place.java
   - Generate frontend mapping

4. **Technical Writer should:**
   - Synthesize all analyses
   - Create comprehensive requirements document
   - Include specific examples and file paths

## Troubleshooting

### If Tools Are Not Being Called

1. **Check CrewAI version:**
   ```bash
   pip show crewai
   ```

2. **Check if tools are properly registered:**
   ```bash
   python -c "from src.synth.crewai_requirements import WeaviateSearchTool, SourceFileReaderTool; print('Tools OK')"
   ```

3. **Test tools directly:**
   ```python
   from src.synth.crewai_requirements import WeaviateSearchTool, SourceFileReaderTool
   
   # Test WeaviateSearchTool
   tool = WeaviateSearchTool(project="PastExport")
   result = tool._run("dao", "DaoCall", 5)
   print(result)
   
   # Test SourceFileReaderTool
   reader = SourceFileReaderTool(project="PastExport")
   result = reader._run("*Dao.java", "PastExport", 5, "java")
   print(result)
   ```

### If Search Returns No Results

1. **Verify Weaviate has data:**
   ```bash
   ./weaviate_stats.sh
   ```

2. **Test search directly:**
   ```bash
   python main.py search --query "dao" --project "PastExport" --limit 5
   ```

3. **Check project name:**
   ```bash
   # Verify project name is correct
   python -c "
   from src.store.weaviate_client import WeaviateClient
   client = WeaviateClient(ensure_schema=False)
   results = client.search_artifacts('DaoCall', 'dao', project='PastExport', limit=5)
   print(f'Found {len(results)} results')
   "
   ```

## Full Test (All Projects)

Once single project test works:

```bash
# Test with all projects (will take 1-3 hours)
./start_requirements_generation.sh 1
```

Monitor with:
```bash
tail -f logprod_crewai_*.log
```

## Success Criteria

✅ **Requirements file contains:**
- Specific file paths (not placeholders)
- Actual code examples
- NestJS/Next.js mappings
- Detailed analysis by area
- No "unable to retrieve artifacts" messages

✅ **Logs show:**
- Multiple tool calls (5-10+ per agent)
- Actual search results
- File reading operations
- Agent iterations (not completing immediately)

✅ **Output quality:**
- Professional structure
- Frontend → Backend organization
- Traceability to source code
- Actionable requirements

