# Java/JSP/GWT/JS → PRD Pipeline (iteration17b)

# nohup 
nohup ./new_run.sh > "lognew_run_$(date +'%Y-%m-%d_%H-%M-%S').log" 2>&1 &
#
nohup ./run_iteration.sh > "log_run_iteration$(date +'%Y-%m-%d_%H-%M-%S').log" 2>&1 &

A comprehensive Python application that analyzes Java/JSP/GWT/JavaScript codebases, extracts metadata and requirements, and generates Product Requirements Documents (PRDs) using Ollama (LLM + embeddings) and Weaviate (vector database).

## 🚀 Features
