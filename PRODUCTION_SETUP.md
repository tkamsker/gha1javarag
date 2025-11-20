# Production Setup from Scratch

Complete guide to set up Weaviate and generate requirements from scratch in production.

## Quick Start

Run the automated setup script:

```bash
./setup_production_from_scratch.sh
```

This script will:
1. ✅ Check Weaviate is running
2. ✅ Optionally clear existing Weaviate data
3. ✅ Fix project names in artifacts
4. ✅ Index all artifacts in Weaviate
5. ✅ Verify indexing worked
6. ✅ Test searches
7. ✅ Optionally generate requirements documents

## Manual Steps (if you prefer)

### Step 1: Start Weaviate

```bash
# Option A: Using docker-compose
docker-compose up -d

# Option B: Using the simple script
./start_weaviate_simple.sh

# Verify it's running
curl http://localhost:8080/v1/meta
```

### Step 2: Clear Weaviate (Optional but Recommended)

If you want a clean start:

```bash
# Delete all classes
python3 << 'EOF'
from store.weaviate_client import WeaviateClient
wc = WeaviateClient(ensure_schema=False)
classes = ['DaoCall', 'IbatisStatement', 'BackendDoc', 'JspForm', 
           'DbTable', 'GwtModule', 'GwtUiBinder', 'GwtActivityPlace',
           'GwtEndpoint', 'JsArtifact']
for class_name in classes:
    try:
        wc._client.schema.delete_class(class_name)
        print(f"Deleted: {class_name}")
    except:
        pass
EOF
```

Or restart Weaviate container:

```bash
docker-compose down
docker-compose up -d
```

### Step 3: Fix Project Names

Ensure project names are correct in artifacts:

```bash
source venv/bin/activate
python fix_project_names.py
```

This will:
- Fix project names in all artifact files
- Use `JAVA_SOURCE_DIR` from `.env` to extract correct project names
- Show summary of changes

### Step 4: Index All Artifacts

Index all artifacts with correct project names:

```bash
python main.py index --all-projects
```

Expected output:
```
Loading 13359 DAO call files from java_calls directory...
Loaded 13359 DAO call artifacts
Found X projects in artifacts: ...
Indexing dao_calls...
Indexing ibatis_statements...
...
Indexed X artifacts in Weaviate
```

### Step 5: Verify Indexing

Check what's actually in Weaviate:

```bash
./weaviate_stats.sh
```

Or:

```bash
python weaviate_stats.py
```

This shows:
- Total objects indexed
- Objects by class
- Projects overview
- Search test results

### Step 6: Test Search

Verify searches work:

```bash
# Test search for a project
python main.py search --query "dao" --project "cuco-core"

# Test search for another project
python main.py search --query "dao" --project "cuco-ui-cct-a1voip"
```

### Step 7: Generate Requirements

Generate requirements documents for all projects:

```bash
# Run in background with logging
nohup python main.py requirements --all-projects --use-crewai > "logprod_crewai_$(date +'%Y-%m-%d_%H-%M-%S').log" 2>&1 &
```

Monitor progress:

```bash
# Watch the log
tail -f logprod_crewai_*.log

# Check if process is running
ps aux | grep "main.py requirements"
```

## Troubleshooting

### Weaviate Not Accessible

```bash
# Check if Weaviate is running
docker ps | grep weaviate

# Check Weaviate logs
docker-compose logs weaviate

# Restart Weaviate
docker-compose restart
```

### No Data Indexed

1. **Check artifacts exist:**
   ```bash
   ls -la data/build/java_calls/*.json | wc -l
   # Should show 13359+ files
   ```

2. **Check project names:**
   ```bash
   python find_project_names.py
   ```

3. **Re-run indexing:**
   ```bash
   python main.py index --all-projects
   ```

### Search Returns No Results

1. **Check what's indexed:**
   ```bash
   ./weaviate_stats.sh
   ```

2. **Verify project name:**
   - Project names are case-sensitive
   - Must match exactly: "cuco-ui-cct-a1voip" not "Cuco-Ui-Cct-A1Voip"

3. **Test without project filter:**
   ```bash
   python main.py search --query "dao"
   ```
   If this works, the issue is with project filtering.

### Requirements Generation Fails

1. **Check logs:**
   ```bash
   tail -f logprod_crewai_*.log
   ```

2. **Check Ollama is running:**
   ```bash
   curl http://localhost:11434/api/tags
   ```

3. **Check Weaviate is accessible:**
   ```bash
   curl http://localhost:8080/v1/meta
   ```

## Expected Results

After successful setup:

- **13,000+ artifacts indexed** in Weaviate
- **30+ projects** with correct names
- **Searches working** for all projects
- **Requirements documents** generated in `output/` directory

## Files Generated

After requirements generation:

- `output/*_crewai_requirements.md` - One file per project
- `output/requirements/*/crewai/` - Detailed analysis files
- `logprod_crewai_*.log` - Generation log

## Time Estimates

- **Indexing**: 5-15 minutes (depending on data size)
- **Requirements generation**: 1-3 hours for all projects (depends on Ollama speed)

## Production Checklist

- [ ] Weaviate is running and accessible
- [ ] Artifacts exist in `data/build/`
- [ ] Project names are fixed
- [ ] All artifacts are indexed
- [ ] Searches work for test projects
- [ ] Requirements generation started
- [ ] Logs are being monitored

