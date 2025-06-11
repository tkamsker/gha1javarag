# Iteration 4: Semantic Code Search & Clustering Application

**Goal:**  
Implement a semantic code search and clustering tool that ingests Doxygen XML from Java projects, generates code embeddings, clusters similar code artifacts, and enables requirement generation using GenAI.  
**Constraint:**  
The application must run from the `semantic/` directory and use **Python** (not Java).

---

## Directory Structure

semantic/
├── config/
│ └── app.yaml # Configuration file
├── data/
│ ├── doxygen_xml/ # Input Doxygen XML files
│ └── chroma_db/ # ChromaDB persistent storage
├── src/
│ ├── doxygen_parser.py # XML → code artifact extraction
│ ├── embedder.py # Embedding generation
│ ├── chroma_connector.py # ChromaDB interface
│ ├── cluster_engine.py # Clustering logic
│ ├── requirement_gen.py # GenAI requirement generation
│ └── main.py # Main workflow
├── requirements.txt # Python dependencies
└── README.md # Setup/usage instructions



---

## Step-by-Step Implementation

### 1. Environment Setup

cd semantic
python -m venv .venv
source .venv/bin/activate
pip install chromadb sentence-transformers scikit-learn openai lxml pyyaml



---

### 2. Doxygen XML Parsing (`doxygen_parser.py`)

- Use `lxml` to parse Doxygen XML files.
- Extract code artifacts: classes, methods, comments, signatures.

**Example:**
from lxml import etree
from pathlib import Path
def parse_doxygen_xml(xml_dir):
artifacts = []
for xml_file in Path(xml_dir).glob("*.xml"):
tree = etree.parse(str(xml_file))
for member in tree.xpath("//memberdef[@kind='function']"):
artifact = {
"id": member.findtext("id"),
"name": member.findtext("name"),
"definition": member.findtext("definition"),
"args": member.findtext("argsstring"),
"doc": "".join(member.findtext("detaileddescription") or ""),
"class": member.getparent().findtext("compoundname"),
}
artifacts.append(artifact)
return artifacts


---

### 3. Embedding Generation (`embedder.py`)

- Use `sentence-transformers` (e.g., `all-MiniLM-L6-v2`) to generate vector embeddings for each artifact.

**Example:**

from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
def embed_artifacts(artifacts):
texts = [f"{a['definition']} {a['doc']}" for a in artifacts]
embeddings = model.encode(texts)
for artifact, emb in zip(artifacts, embeddings):
artifact['embedding'] = emb
return artifacts


---

### 4. ChromaDB Storage (`chroma_connector.py`)

- Store each artifact and its embedding in ChromaDB.

**Example:**

import chromadb
def store_in_chromadb(artifacts, db_path):
client = chromadb.PersistentClient(path=db_path)
collection = client.get_or_create_collection("code_artifacts")
for artifact in artifacts:
collection.add(
ids=[artifact['id']],
embeddings=[artifact['embedding']],
metadatas=[{
"name": artifact['name'],
"class": artifact['class']
}],
documents=[artifact['definition']]
)


---

### 5. Clustering (`cluster_engine.py`)

- Use `scikit-learn` (e.g., KMeans or DBSCAN) to cluster embeddings.

**Example:**

from sklearn.cluster import KMeans
import numpy as np
def cluster_artifacts(artifacts, n_clusters=10):
embeddings = np.array([a['embedding'] for a in artifacts])
kmeans = KMeans(n_clusters=n_clusters, random_state=42).fit(embeddings)
for artifact, label in zip(artifacts, kmeans.labels_):
artifact['cluster'] = int(label)
return artifacts


---

### 6. Semantic Search (`chroma_connector.py`)

- Implement a function to search ChromaDB using a query embedding.

**Example:**
def semantic_search(query, model, collection, top_k=5):
query_emb = model.encode([query])
results = collection.query(query_embeddings=query_emb, n_results=top_k)
return results


---

### 7. Requirement Generation (`requirement_gen.py`)

- Use OpenAI (or another LLM) to generate requirements for each artifact or cluster.

**Example:**

import openai
def generate_requirement(artifact, openai_api_key):
prompt = (
f"Given the following Java method and its documentation, "
f"write a requirement that this code fulfills:\n\n"
f"Class: {artifact['class']}\n"
f"Definition: {artifact['definition']}\n"
f"Documentation: {artifact['doc']}\n\n"
"Requirement:"
)
openai.api_key = openai_api_key
response = openai.ChatCompletion.create(
model="gpt-4-turbo",
messages=[{"role": "user", "content": prompt}]
)
return response.choices.message['content']


---

### 8. Main Workflow (`main.py`)

- Orchestrate the above steps.

**Outline:**

from doxygen_parser import parse_doxygen_xml
from embedder import embed_artifacts
from chroma_connector import store_in_chromadb
from cluster_engine import cluster_artifacts
from requirement_gen import generate_requirement
1. Parse Doxygen XML

artifacts = parse_doxygen_xml("data/doxygen_xml")
2. Generate embeddings

artifacts = embed_artifacts(artifacts)
3. Store in ChromaDB

store_in_chromadb(artifacts, "data/chroma_db")
4. Cluster artifacts

artifacts = cluster_artifacts(artifacts, n_clusters=10)
5. Generate requirements (for each cluster or artifact)

for artifact in artifacts:
requirement = generate_requirement(artifact, openai_api_key="YOUR_API_KEY")
artifact['requirement'] = requirement


---

## Validation Checklist

- **Ingestion:** All Doxygen methods are parsed and stored.
- **Clustering:** Each artifact has a cluster label.
- **Semantic Search:** Query returns relevant code artifacts.
- **Requirements:** Each artifact (or cluster) has a generated requirement.
- **Traceability:** Requirements are linked to code artifacts in ChromaDB.

---

## References

- [Doxygen XML Documentation](https://www.doxygen.nl/manual/output.html#xmloutput)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Sentence Transformers](https://www.sbert.net/)
- [OpenAI API](https://platform.openai.com/docs/)

---

**This document describes a step-by-step, Python-based, directory-structured solution for semantic code search and requirement extraction, suitable for ingestion by cursor.ai and deployment from the `semantic/` directory.**

