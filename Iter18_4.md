## Iteration 18.4 - Improving Embeddings Quality and Step 2/3 Detail

### Goals
- Eliminate empty/weak embeddings during Step 1.
- Ensure Weaviate holds rich, searchable content for Step 2/3.
- Produce more detailed `requirements.md` and `mapping.md` (reduce “partial” notes).

### Summary of Findings
- Embedding calls occasionally return empty vectors from Ollama (`nomic-embed-text:latest`). We now log and proceed without vectors, but search quality suffers.
- Step 2 structures are sparse because Step 1 extraction JSON often lacks full class/method/field details.
- Weaviate collection vectorizer can be `text2vec-ollama` (server-side) or `none` (client vectors). We’ve enabled configuration and REST fallbacks; data is present and retrievable.

### Step-by-Step Plan

1) Baseline Diagnostics (quick)
- Use the diagnosis to verify per-project counts and sample file paths after each run:
  - `python scripts/diagnose_weaviate.py --project cuco-core --preview 5`
  - `python scripts/diagnose_weaviate.py --project cuco-ui-cct-common --preview 5`
- Capture: total objects, sample files, vectorizer mode. Store screenshots/snippets in `PIPELINE_STATUS.md` (optional).

2) Embedding Strategy Hardening
- Client-side embeddings (vectorizer=none):
  - Switch default embed model to a more robust one if available (e.g., `nomic-embed-text` stable tag or another local model known to return non-empty vectors). Add env override in `.env`:
    - `OLLAMA_EMBED_MODEL_NAME=nomic-embed-text`
  - In `OllamaClient.get_embedding`: already retries; add fallback to a second model if the primary returns empty.
- Server-side embeddings (vectorizer=text2vec-ollama):
  - Ensure Ollama is reachable and sized to handle concurrent requests. Monitor latency.
  - If inserts are slow, stage embeddings offline (client) and switch back to `none`.

3) Content Selection for Embeddings
- Embed richer, code-aware text:
  - Build embedding text from:
    - file path, package, imports
    - class/interface/enum names
    - method signatures and annotations
    - DAO/DTO/Service/Controller heuristics
  - Implement a helper to construct an embedding payload from extracted JSON. If Step 1 has no JSON yet, fall back to the first N lines of code + file path.

4) Chunking & Granularity
- Chunk larger files (e.g., > 800 lines) by class or by sections (interfaces, methods). Store multiple objects per file with `metadata` linking them (e.g., `parentFile`, `className`).
- Benefits: better recall and precision; smaller text windows for embeddings; more detailed Step 2 categorization.

5) Step 1 Extraction Prompt Improvements
- In `OllamaClient.extract_file_info`:
  - Emphasize extracting ALL methods and fields, including access modifiers, return types, annotations, and relationships.
  - Add instruction to identify DAO/DTO/Service/Controller/Entity using patterns and annotations.
  - For Java, request package name, imports, and class-level annotations explicitly.
- Validate JSON rigorously; if parsing fails, attempt a second pass with a reduced prompt (JSON-only response directive).

6) Step 2 Structuring Enhancements
- In `ProjectStructureTool` (Step 2):
  - Re-categorize files with stronger heuristics:
    - Detect DAOs by name (Dao) and `@Repository`/`@Mapper` patterns
    - DTO by suffix `DTO`/`Dto`
    - Service by suffix `Service` or `@Service`
    - Controller by `@Controller`/`@RestController`
    - Entity by `@Entity`
    - Frontend with JSP Htm html js files  
  - Build relationships: service→dao, controller→service, entity→dao.
- If Weaviate is empty for a project, merge Step 1 fallback JSON and re-run categorization (already supported, make sure dedup works by `filePath`).

7) Step 3 Prompt Enhancements
- For `requirements.md` and `mapping.md`:
  - Provide the full structured JSON from Step 2 (classes, methods, fields, annotations) per file to the LLM.
  - Instruct to produce exhaustive, sectioned outputs: Entities, DAOs, Services (with operations), Controllers (with endpoints), Business rules, SQL interactions, Data flows.
  - Prefer lists and tables for coverage; avoid generic prose like “20% demo.”

8) Reindex & Backfill Procedure
- For existing runs where vectors are missing:
  - Add a backfill script to:
    - Read `data/build/step1_extracted_data.json` per project.
    - Construct embedding text for each file using the helper (see Step 3).
    - Update or re-insert objects with vectors (if `vectorizer=none`).
  - Optionally recreate collection with `text2vec-ollama` then reinsert (using `scripts/seed_weaviate.py --recreate`).

9) Validation & KPIs
- Define metrics:
  - % files with non-empty embeddings
  - Avg Step 2 entities detected per project (DAOs, DTOs, Services, Controllers, Entities)
  - Step 3 output size (sections populated) and presence of endpoint/service/dao mappings
- Add a small report after each run to `PIPELINE_STATUS.md` summarizing KPIs.

### Concrete Implementation Tasks
- Config
  - Add `OLLAMA_EMBED_MODEL_NAME` default and fallback model via env.
- Embeddings
  - Implement `build_embedding_text(extracted_info, file_path, content_head)` in Step 1.
  - Wire it into Step 1 before insert; if vectorizer=none: call `get_embedding()` and attach vectors.
- Chunking (optional initial scope)
  - Start with per-class objects for files containing multiple classes.
- Step 2
  - Strengthen categorization + relationship construction; merge fallback cleanly.
- Step 3
  - Update prompts to require exhaustive coverage; include structured JSON context.
- Backfill script
  - New script `scripts/backfill_embeddings.py` to re-embed and update objects.

### Rollout Plan
- Phase 1 (Today):
  - Enable `WEAVIATE_VECTORIZER=text2vec-ollama` in prod or stick to `none` + client embeddings if Ollama is unstable.
  - Implement embedding text builder and prompt enhancements for Step 1/3.
- Phase 2:
  - Add backfill script; run on existing datasets.
  - Add KPIs to `PIPELINE_STATUS.md` after runs.
- Phase 3:
  - Introduce chunking and relationship graphs; refine Step 2 categorization rules.

### Quick Commands
- Verify collection/vectorizer:
  - `curl -sS http://localhost:8080/v1/schema/FileExtraction | jq '.vectorizer'`
- Diagnose per project:
  - `python scripts/diagnose_weaviate.py --project cuco-core --preview 5`
- Middle-size run:
  - `python scripts/run_middle.py --dir1 <path1> --dir2 <path2> --count 100 --project cuco-core --preview 5`

This plan focuses on producing higher-quality embeddings and richer structured data to feed Step 2/3. It includes incremental, testable steps with clear validation signals and minimal disruption to existing scripts.
