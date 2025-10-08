# Model Consistency Fix

## Problem
The codebase had inconsistent model usage:
- `.env` file specified `OLLAMA_MODEL_NAME=llama3.1:8b` and `OLLAMA_EMBED_MODEL_NAME=nomic-embed-text`
- `step1_setup.sh` was hardcoded to pull `llama3.2:3b` and `nomic-embed-text`
- This caused confusion and potential issues

## Solution
Updated all code and scripts to consistently use models from `.env` configuration.

## Changes Made

### 1. Updated `step1_setup.sh`
- **Before**: Hardcoded models `llama3.2:3b` and `nomic-embed-text`
- **After**: Reads models from `.env` using Python settings
- **Code**: Uses `settings.ollama_model_name` and `settings.ollama_embed_model_name`

### 2. Updated `src/store/weaviate_client.py`
- **Before**: Basic `text2vec-ollama` configuration
- **After**: Added `moduleConfig` with model and API endpoint from settings
- **Code**: 
  ```python
  "moduleConfig": {
      "text2vec-ollama": {
          "model": settings.ollama_embed_model_name,
          "apiEndpoint": settings.ollama_base_url
      }
  }
  ```

### 3. Updated `run_iteration17b.sh`
- **Before**: Hardcoded model reference in help text
- **After**: Generic reference to `<model_from_env>`

### 4. Verified Existing Code
- ✅ `src/chunk/build_chunks.py` - Already uses `settings.ollama_embed_model_name`
- ✅ `src/synth/prd_markdown.py` - Already uses `settings.ollama_model_name`
- ✅ `src/config/settings.py` - Already properly configured

## Current Configuration

### .env File
```bash
OLLAMA_MODEL_NAME=llama3.1:8b
OLLAMA_EMBED_MODEL_NAME=nomic-embed-text
OLLAMA_BASE_URL=http://localhost:11434
```

### Usage
All scripts and code now consistently use these models:
- **Main LLM**: `llama3.1:8b` (for text generation)
- **Embedding Model**: `nomic-embed-text` (for vectorization)
- **API Endpoint**: `http://localhost:11434`

## Benefits
1. **Consistency**: All components use the same models
2. **Configurability**: Easy to change models by updating `.env`
3. **Maintainability**: Single source of truth for model configuration
4. **Flexibility**: Different environments can use different models

## Testing
To verify the fix:
```bash
# Check current model configuration
source venv/bin/activate
python -c "
import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute() / 'src'))
from config.settings import settings
print(f'Main model: {settings.ollama_model_name}')
print(f'Embed model: {settings.ollama_embed_model_name}')
print(f'Ollama URL: {settings.ollama_base_url}')
"
```

## Next Steps
1. Run `./step1_setup.sh` to pull the correct models
2. Run `./step2_fetch.sh all <project> <frontend>` to test the pipeline
3. Verify that Weaviate uses the correct embedding model for vectorization
