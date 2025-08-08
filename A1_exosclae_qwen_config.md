
#a1 .env file 
OPENAI_API_KEY=ollama
OPENAI_BASE_URL=http://localhost:11434/v1
OPENAI_MODEL=gpt-oss:120b

# or for bash 
export OPENAI_API_KEY="ollama"
export OPENAI_BASE_URL="http://localhost:11434/v1"
export OPENAI_MODEL="gpt-oss:120b"

# we need 
OLLAMA_TIMEOUT=900 ollama run gpt-oss:120b
