- Set it once via .env and load it in scripts.
- Add sane defaults and guardrails for large runs.
- Reduce embedding warnings/noise and speed up Step 1.

Do this
- Put it in .env so you don’t have to export each time:
```bash
echo 'FORCE_MULTIPROJECT_DISCOVERY=true' >> .env
```
- Ensure scripts load .env automatically. Add near the top of `scripts/run_full.sh` and `scripts/run_small.sh`:
```bash
set -a
[ -f ".env" ] && . ./.env
set +a
# default to true if not set
export FORCE_MULTIPROJECT_DISCOVERY="${FORCE_MULTIPROJECT_DISCOVERY:-true}"
```
- Make README’s nohup one-liner preserve env by sourcing .env:
```bash
nohup bash -lc 'set -a; [ -f .env ] && . .env; set +a; ./scripts/run_full.sh' > "log_full_run_$(date +'%Y-%m-%d_%H-%M-%S').log" 2>&1 &
```

Recommended config additions (optional but useful)
- Add include/exclude and project filters in .env to keep runs focused:
```bash
JAVA_INCLUDE_GLOBS="**/*.java,**/*.jsp,**/*.xml"
PROJECT_INCLUDE="cuco-core,cuco-ui-app"     # only these projects
PROJECT_EXCLUDE="_deprecated,infra,docs"    # exclude noisy roots
```
- Add batching/concurrency to control throughput:
```bash
STEP1_MAX_FILES_PER_PROJECT=500
STEP1_CONCURRENCY=2
```
- Add an option to skip embeddings during Step 1 (store without vectors) to remove warnings and speed up:
```bash
DISABLE_EMBEDDINGS=true
```

Operational tips
- Use the new discovery reports to verify coverage before full runs:
```bash
python dry_run.py
# check data/build/source_check.json and data/build/source_discovery.json
```
- If embeddings are still noisy, set `OLLAMA_EMBED_MODEL_NAME=nomic-embed-text:latest` in .env (explicit tag) or `DISABLE_EMBEDDINGS=true` for Step 1, then re-embed later in a separate pass.

Outcome
- You won’t need to export manually each time.
- Full discovery remains enabled by default.
- Large codebases run more predictably with filters/batching.
- Embedding warnings won’t block or clutter logs.