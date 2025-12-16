Perfect! I've fixed the cross-platform compatibility issues. Here's what was done:

  Fixes Applied

  1. ✅ Shell Script Non-Interactive Mode (Previous Commit)

  - Added --yes flag to run-cuco.sh for nohup/background execution
  - Fixed "Bad file descriptor" error on Ubuntu

  2. ✅ Platform-Aware Ollama Endpoint (This Commit)

  - Problem: Schema files hardcoded host.docker.internal:11434 which doesn't work on Linux
  - Solution: Added automatic platform detection
    - macOS: Uses host.docker.internal:11434 (Docker Desktop DNS)
    - Linux: Uses 127.0.0.1:11434 (works with network_mode: host)

  Changes Made

  src/codeindex/schemas/weaviate.py:
  - Added get_ollama_endpoint_for_weaviate() function with platform detection
  - Replaced all hardcoded URLs in Project and CodeArtifact schemas

  src/codeindex/schemas/dto_artifact_schema.py:
  - Imported and used platform-aware endpoint function

  Ubuntu Deployment Instructions

  Run these commands on your Ubuntu production system:

  cd /home/tkamsker/development/Iteration20/gha1javarag/

  # Pull latest fixes (weaviate_store.py + platform detection)
  git pull origin main

  # Verify you got both commits
  git log --oneline -3

  # Reinstall package with new code
  source .venv/bin/activate
  pip install -e .

  # Clean Weaviate data (schemas need to be recreated with new endpoints)
  ./docker-weaviate.sh clean  # Type 'yes' to confirm

  # Restart Weaviate
  ./docker-weaviate.sh restart

  # Verify Ollama is running
  curl -s http://localhost:11434/api/tags

  # Run pipeline with non-interactive flag
  nohup ./run-cuco.sh --yes /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/cuco-ui-admin > cuco-pipeline.log 2>&1 &

  # Monitor progress
  tail -f cuco-pipeline.log

  What Works Now

  ✅ macOS: All functionality unchanged, still uses host.docker.internal
  ✅ Ubuntu Linux: Schemas now use 127.0.0.1:11434 which works with network_mode: host
  ✅ Non-Interactive: --yes flag allows nohup/background execution
  ✅ No .env Changes: Platform detection is automatic

  The pipeline should now complete successfully on both platforms!

## ---------

Perfect! I've fixed the cross-platform configuration issue. Here's what was wrong and how to fix it:

  🔍 Root Cause

  Your Ubuntu .env file has:
  OLLAMA_BASE_URL=http://host.docker.internal:11434  # ❌ WRONG for host execution!

  This URL only works INSIDE Docker containers (like Weaviate calling Ollama). Your Python code runs on the HOST, so it needs:
  OLLAMA_BASE_URL=http://localhost:11434  # ✅ CORRECT for host execution

  ✅ Fixes Applied

  1. Validation in run-cuco.sh

  The script now checks for this mistake and shows a clear error:
  [ERROR] Invalid OLLAMA_BASE_URL in .env file!

  Your .env has: OLLAMA_BASE_URL=http://host.docker.internal:11434

  This URL only works INSIDE Docker containers.
  For host-side Python code (run-cuco.sh), use:

    OLLAMA_BASE_URL=http://localhost:11434

  Please update your .env file and try again.

  2. Enhanced .env.example

  Added comprehensive documentation explaining:
  - Host-side Python code: localhost:11434 (both macOS & Linux)
  - Container-side (Weaviate): Handled automatically by Docker Compose files

  3. New check-env.sh Tool

  Diagnostic script to check and fix configuration:
  ./check-env.sh         # Check for issues
  ./check-env.sh --fix   # Auto-fix issues

  📋 Ubuntu Fix Instructions

  Run these commands on your Ubuntu production server:

  cd /home/tkamsker/development/Iteration20/gha1javarag/

  # Pull latest fixes (validation + diagnostic tool)
  git pull origin main

  # Make check-env.sh executable (if needed)
  chmod +x check-env.sh

  # Option 1: Auto-fix (recommended)
  ./check-env.sh --fix

  # Option 2: Manual fix
  nano .env
  # Change line:
  #   FROM: OLLAMA_BASE_URL=http://host.docker.internal:11434
  #   TO:   OLLAMA_BASE_URL=http://localhost:11434
  # Save and exit (Ctrl+X, Y, Enter)

  # Verify configuration is correct
  ./check-env.sh

  # Should show:
  # [OK] All checks passed! ✓

  # Reinstall package (pick up schema changes from earlier commit)
  source .venv/bin/activate
  pip install -e .

  # Restart pipeline
  nohup ./run-cuco.sh --yes /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/cuco-ui-admin > cuco-pipeline.log 2>&1 &

  # Monitor - should no longer see host.docker.internal errors
  tail -f cuco-pipeline.log

  📊 How URLs Work

  | Execution Context                 | Ollama URL                        | Why                                                  |
  |-----------------------------------|-----------------------------------|------------------------------------------------------|
  | Host Python (run-cuco.sh, CLI)    | http://localhost:11434            | Python runs on your machine, not in Docker           |
  | macOS Docker (Weaviate container) | http://host.docker.internal:11434 | Docker Desktop provides this special DNS             |
  | Linux Docker (Weaviate container) | http://127.0.0.1:11434            | Uses network_mode: host in docker-compose.ubuntu.yml |

  The key insight: Different execution contexts need different URLs, and they're handled automatically in the right places.

  ✅ Expected Result

  After the fix, your extraction logs should show:
  2025-12-16 14:05:34 [INFO] Extracting java_source: .../InitializationHandler.java
  ✅ No errors about host.docker.internal
  ✅ Ollama connections work immediately
  ✅ Semantic extraction proceeds normally

  Let me know once you've run the fix and we can verify it works!