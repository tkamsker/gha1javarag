I added a seeding script that can recreate the collection with your desired vectorizer and insert test objects with optional embeddings.

**Run examples:**

Recreate with vectorizer=none, insert 5 with embeddings via Ollama:

python scripts/seed_weaviate.py --project cuco-ui-cct-common --count 5 --vectorizer none --recreate --embed

Switch to Weaviate-side vectorization (text2vec-ollama), insert 3 without manual vectors:

python scripts/seed_weaviate.py --project cuco-ui-cct-common --count 3 --vectorizer text2vec-ollama --recreate

Control what text is embedded (when --embed is used):

python scripts/seed_weaviate.py --project cuco-ui-cct-common --count 2 --vectorizer none --embed --embed-text "filePath extractedInfo"

Verify:

python scripts/diagnose_weaviate.py --project cuco-ui-cct-common --preview 5

Notes:

Script: scripts/seed_weaviate.py

It can:
    - Ensure or recreate FileExtraction with vectorizer=none or text2vec-ollama.
    - Generate embeddings via Ollama (Config.OLLAMA_BASE_URL, Config.OLLAMA_EMBED_MODEL_NAME) and attach vectors on insert.
    - Insert via REST (tries vectors.default, falls back to vector).