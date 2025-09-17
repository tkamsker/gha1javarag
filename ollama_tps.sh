
set -euo pipefail

MODEL="${1:-llama3}"
PROMPT="${2:-Write ~600 words about performance testing.}"
NUM_PREDICT="${NUM_PREDICT:-512}"    # override: NUM_PREDICT=1024 ./ollama_tps.sh ...

# Warm-up (ignore output)
curl -s --fail http://localhost:11434/api/generate -d "{
  \"model\":\"$MODEL\",
  \"prompt\":\"Warm up.\",
  \"stream\": false,
  \"options\": {\"temperature\":0, \"num_predict\":128}
}" >/dev/null || { echo "Warm-up failed. Is Ollama running?"; exit 1; }

# Actual measurement
RESP="$(curl -s --fail http://localhost:11434/api/generate -d "{
  \"model\":\"$MODEL\",
  \"prompt\":\"$PROMPT\",
  \"stream\": false,
  \"options\": {\"temperature\":0, \"num_predict\":$NUM_PREDICT}
}")" || { echo "Request failed"; exit 1; }

# If Ollama returned an error JSON, show it and exit
ERR="$(printf '%s' "$RESP" | jq -r 'select(.error) | .error // empty')"
if [ -n "$ERR" ]; then
  echo "Ollama error: $ERR"
  printf '%s\n' "$RESP" | jq .
  exit 2
fi

# Print safe metrics
printf '%s' "$RESP" | jq -r '
  def sec: ( . // 0 ) / 1e9;
  def safe_div(a;b): (if (b // 0) == 0 then null else (a // 0) / (b // 0) end);

  {
    model,
    prompt_tokens: (.prompt_eval_count // 0),
    gen_tokens: (.eval_count // 0),
    prompt_sec: ((.prompt_eval_duration // 0) | sec),
    gen_sec: ((.eval_duration // 0) | sec),
    total_sec: ((.total_duration // 0) | sec),
    prompt_tps: (safe_div(.prompt_eval_count; ((.prompt_eval_duration // 0) / 1e9))),
    gen_tps: (safe_div(.eval_count; ((.eval_duration // 0) / 1e9))),
    note: "TPS is null if duration/token count was zero or missing; increase num_predict."
  }'
