I'll fix the file discovery bug causing few matches, add discovery and processing reports, and harden Step 2 to merge fallback data for full coverage. Then I'll review the embedding warnings and add retries/defaults.

[11 tools called]

- I fixed the low file count issue. Your discovery used rglob with an incorrect lstrip that mangled patterns like **/*.java. I removed that so recursion now matches all files.

What I added
- Discovery/coverage reports
  - Pipeline now writes `data/build/source_discovery.json` with all discovered projects/files right after discovery.
  - Pipeline writes a flattened `data/build/files_passed.json` with pass/fail per file after Step 1.
  - `dry_run.py` writes `data/build/source_check.json` with counts per project and type, plus samples.
- Stronger Step 2 coverage
  - If Weaviate has some files, Step 2 now merges any missing files from `data/build/step1_extracted_data.json` and re-categorizes entities from the full set.
- Embedding warning handling
  - Ollama embeddings now retry twice and normalize model tags. If still empty, we store without vectors; warnings are reduced and more resilient.

Key code references
```57:66:/Users/thomaskamsker/Documents/Atom/vron.one/playground/a1javarag/src/agents/step1_agents.py
for glob_pattern in globs:
    try:
        # Use glob pattern as-is; do not lstrip characters (that breaks patterns like **/*.java)
        found_files = list(directory.rglob(glob_pattern))
```

```35:45:/Users/thomaskamsker/Documents/Atom/vron.one/playground/a1javarag/src/pipeline.py
logger.info(f"Discovered {total_files} files across {len(projects)} projects")
# Persist discovery for auditing and cross-checking
Config.BUILD_DIR.mkdir(parents=True, exist_ok=True)
discovery_file = Config.BUILD_DIR / "source_discovery.json"
discovery_file.write_text(json.dumps(discovery_result, indent=2), encoding='utf-8')
```

```95:104:/Users/thomaskamsker/Documents/Atom/vron.one/playground/a1javarag/src/pipeline.py
files_passed_file = Config.BUILD_DIR / "files_passed.json"
files_passed_file.write_text(json.dumps(files_passed, indent=2), encoding='utf-8')
```

```124:170:/Users/thomaskamsker/Documents/Atom/vron.one/playground/a1javarag/src/pipeline.py
# Merge fallback extracted data to ensure completeness
extracted_file = Config.BUILD_DIR / "step1_extracted_data.json"
...
# Merge missing files by filePath
existing_paths = {f.get("filePath") for f in project_structure.get("files", [])}
new_files = [f for f in project_files if f.get("filePath") not in existing_paths]
...
# Re-categorize files based on full set
project_structure["entities"] = { "daos": [], "dtos": [], "services": [], "controllers": [], "entities": [], "ui_files": [], "sql_files": [] }
```

```150:187:/Users/thomaskamsker/Documents/Atom/vron.one/playground/a1javarag/src/utils/ollama_client.py
# Retry up to 2 times if empty embedding is returned
for attempt in range(2):
    response = httpx.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=60.0)
    ...
logger.warning(f"Empty embedding returned from Ollama for model {model_name}")
return None
```

```59:86:/Users/thomaskamsker/Documents/Atom/vron.one/playground/a1javarag/dry_run.py
# Write machine-readable check report
check = {"sourceDir": str(Config.JAVA_SOURCE_DIR), "projectCount": len(projects), "totalFiles": total_files, "projects": {}}
...
(Config.BUILD_DIR / "source_check.json").write_text(json.dumps(check, indent=2), encoding='utf-8')
```

How to run checks
- Dry-run (discovery only; writes source_check.json):
```bash
python dry_run.py
```
- Full pipeline (writes source_discovery.json, files_passed.json, and step1_extracted_data.json along the way):
```bash
export FORCE_MULTIPROJECT_DISCOVERY=true
python main.py
```

What to look for
- source_discovery.json vs files_passed.json:
  - Compare counts to confirm all discovered files are attempted and tracked.
- Step 2 should now structure all files (Weaviate + fallback merged).
- Embedding warnings should remain but be retried and non-blocking.

- Fixes:
  - Discovery recursion now matches all expected files.
  - Added completeness artifacts to prevent overlooking any file.
  - Step 2 now digs into every available file, not just what Weaviate returns.