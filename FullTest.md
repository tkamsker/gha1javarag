### Recommended full test iteration (external terminal)

- Create venv and install
```bash
cd /Users/thomaskamsker/Documents/Atom/vron.one/playground/a1javarag
python3 -m venv venv && source venv/bin/activate
pip install -U pip && pip install -r requirements.txt
```

- Start Weaviate with persistence
better 
./docker-weaviate.sh up

curl -s http://localhost:8080/v1/meta | jq .version


```bash
docker run -d --rm --name weaviate \
  -p 8080:8080 \
  -e QUERY_DEFAULTS_LIMIT=25 \
  -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
  -e PERSISTENCE_DATA_PATH=/var/lib/weaviate \
  -e DEFAULT_VECTORIZER_MODULE=text2vec-ollama \
  -e ENABLE_MODULES=text2vec-ollama,generative-ollama \
  -e CLUSTER_HOSTNAME=node1 \
  -v "$(pwd)/weaviate-data:/var/lib/weaviate" \
  semitechnologies/weaviate:1.30.18
```

- Configure .env (adjust paths/providers as needed)
```bash
cat > .env << 'ENV'
OUTPUT_DIR=./output
JAVA_SOURCE_DIR=/Users/thomaskamsker/Documents/Atom/vron.one/playground/java/cuco-ui-admin
WEAVIATE_URL=http://localhost:8080
AI_PROVIDER=ollama
EMBEDDING_PROVIDER=ollama
EMBEDDING_MODEL=nomic-embed-text
ENV
```

- Run the full iteration with comparison
```bash
./run_iteration.sh --rotate-output --force-step1 --repeat-step2 \
  --step3=both --step3-parallel --step3-max-workers 3
```

- Quick health checks
```bash
source venv/bin/activate
python -m src.cli stats
ls -R output_* | sed -n '1,80p'
```

- Re-run individual steps if needed
```bash
./step1.sh
./step2.sh
./step3-pgm.sh --enhanced --parallel --max-workers 3
./step3-crewai.sh
```

- Where to look for results
  - `output_YYYYMMDD_HHMMSS/requirements/`
  - `output_YYYYMMDD_HHMMSS/requirements/pgm/` and `/crewai/`
  - `output_YYYYMMDD_HHMMSS/requirements/_comparison/index.md`



  ### crewai fix 
  bash -lc "cd /Users/thomaskamsker/Documents/Atom/vron.one/playground/a1javarag && source venv/bin/activate && OUTPUT_DIR=./output_20251007_132632 ./step3-crewai.sh --no-verbose | sed -n '1,80p'"


  I'll update the CrewAI processor to explicitly use the Ollama model through CrewAI's LLM interface and attach it to all agents, preventing the fallback to OpenAI via LiteLLM. Then you can rerun step3-crewai.

[2 tools called]

- Root cause: CrewAI defaulted to OpenAI via LiteLLM, causing invalid OpenAI API key errors.
- Fix applied: Configured CrewAI to use the local Ollama model explicitly and disabled memory/RAG. Also kept sequential process.

To rerun
- OUTPUT_DIR=./output_20251007_132632 ./step3-crewai.sh --no-verbose

Now CrewAI logs show it using Ollama successfully.

## 
OUTPUT_DIR=./output_20251007_132632 STEP3_CREWAI_SCOPE=backend ./step3-crewai.sh --no-verbose

OUTPUT_DIR=./output_20251007_132632 STEP3_CREWAI_SCOPE=frontend ./step3-crewai.sh --no-verbose

## malloc issue 
export OLLAMA_NUM_CTX=32768
export OLLAMA_KEEP_ALIVE=5m
export LITELLM_TIMEOUT=180
export LITELLM_MAX_TOKENS=800
OUTPUT_DIR=./output_20251007_132632 ./step3-crewai.sh --no-verbose


####

bash -lc "cd /Users/thomaskamsker/Documents/Atom/vron.one/playground/a1javarag && source venv/bin/activate && export OLLAMA_NUM_CTX=32768 OLLAMA_KEEP_ALIVE=5m LITELLM_TIMEOUT=180 LITELLM_MAX_TOKENS=800 && OUTPUT_DIR=./output_20251007_132632 ./step3-crewai.sh --no-verbose | sed -n '1,140p'"