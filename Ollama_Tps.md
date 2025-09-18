# we tried ollama tps for check 

# exo machine 

./ollama_tps.sh  qwen3:30b-a3b-thinking-2507-q8_0
{
  "model": "qwen3:30b-a3b-thinking-2507-q8_0",
  "prompt_tokens": 18,
  "gen_tokens": 512,
  "prompt_sec": 0.068347286,
  "gen_sec": 6.920972731,
  "total_sec": 7.027028862,
  "prompt_tps": 263.3608597128495,
  "gen_tps": 73.97804035647775,
  "note": "TPS is null if duration/token count was zero or missing; increase num_predict."
}

## MX max mac 
./ollama_tps.sh bjoernb/qwen3-coder-30b-1m
{
  "model": "bjoernb/qwen3-coder-30b-1m",
  "prompt_tokens": 18,
  "gen_tokens": 512,
  "prompt_sec": 0.100032208,
  "gen_sec": 11.536347917,
  "total_sec": 11.710545542,
  "prompt_tps": 179.94204426638268,
  "gen_tps": 44.38146315312796,
  "note": "TPS is null if duration/token count was zero or missing; increase num_predict."
}

## danielsheep/Qwen3-Coder-30B-A3B-Instruct-1M-Unsloth

./ollama_tps.sh danielsheep/Qwen3-Coder-30B-A3B-Instruct-1M-Unsloth
{
  "model": "danielsheep/Qwen3-Coder-30B-A3B-Instruct-1M-Unsloth",
  "prompt_tokens": 18,
  "gen_tokens": 512,
  "prompt_sec": 0.074303372,
  "gen_sec": 7.355789591,
  "total_sec": 7.525642944,
  "prompt_tps": 242.25010945667444,
  "gen_tps": 69.6050360965253,
  "note": "TPS is null if duration/token count was zero or missing; increase num_predict."
}
