# step 1 First, clean up any existing environment:
rm -rf venv chroma_db

# step 2 Run the setup script
./setup.sh

# step 3 Start the API server
python src/api/main.py

# step 4 heck the health of the service:
curl http://localhost:8000/health


curl -v -H "X-Chroma-Api-Version: v2" -H "X-Chroma-Token: admin:admin" https://chromadb.dev.motorenflug.at/api/v2/collections

# ------

source venv/bin/activate

   python search_code.py "your search query"
      python search_code.py "your search query" --results 3


Here are some example queries you can try:
Search for main application entry point:
Apply to Ablauf.md
Run
"
Search for database-related code:
Apply to Ablauf.md
Run
"
Search for authentication methods:
Apply to Ablauf.md
Run
"
Search for calculation-related code:
Apply to Ablauf.md
Run
"
The search results will show:
File path
Type (method or class)
Class name (if it's a method)
Method name (if it's a method)
The actual code content


(venv) (base) thomaskamsker@MacBook-Pro a1javarag % curl -X GET "https://chromadb.dev.motorenflug.at/api/v2/tenants/default_tenant/databases" -H "accept: application/json" -H "x-chroma-token: admin:admin"

