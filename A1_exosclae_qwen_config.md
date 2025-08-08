
#a1 .env file 
OPENAI_API_KEY=ollama
OPENAI_BASE_URL=http://localhost:11434/v1
OPENAI_MODEL=gpt-oss:120b

# or for bash 
export OPENAI_API_KEY="ollama"
export OPENAI_BASE_URL="http://localhost:11434/v1"
export OPENAI_MODEL="gpt-oss:120b"




 (if supported) to speed up attention calculations.
export OLLAMA_KEEP_ALIVE=15m

export OLLAMA_KEEP_ALIVE to keep models loaded longer, avoiding reload overhead.
# we need 
OLLAMA_TIMEOUT=900 ollama run gpt-oss:120b


#  watch -n 1 nvidia-smi

qwen needs to set timeout 
npm config set timeout 600000
and then 
qwen

