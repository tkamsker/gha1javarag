# step 1 First, clean up any existing environment:
rm -rf venv chroma_db

# step 2 Run the setup script
./setup.sh

# step 3 Start the API server
python src/api/main.py

# step 4 heck the health of the service:
curl http://localhost:8000/health