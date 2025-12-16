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
