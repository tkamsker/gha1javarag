# Iteration 4: Semantic Code Search & Clustering Application

## Overview
This document details the implementation of a Java code analysis tool that uses ChromaDB for semantic search/clustering and works from a `semantic/` directory. The system ingests Doxygen-generated XML, creates embeddings, clusters code artifacts, and enables AI-generated requirement extraction.

---

## Directory Structure
semantic/
├── config/
│ └── app.properties # Configuration file
├── data/
│ ├── doxygen_xml/ # Input Doxygen XML files
│ └── chroma_db/ # ChromaDB persistent storage
├── src/
│ ├── main/
│ │ └── java/
│ │ └── semantic/
│ │ ├── Core.java # Main workflow
│ │ ├── DoxygenParser.java # XML → AST converter
│ │ ├── Embedder.java # Code → embeddings
│ │ └── ClusterEngine.java # K-means/DBSCAN impl
│ └── test/ # Unit tests
├── requirements.txt # Python/Java dependencies
└── README.md # Setup/usage instructions


---

## Step-by-Step Implementation

### 1. Environment Setup
Create virtual environment (Python 3.10+ required)

python -m venv .venv
source .venv/bin/activate
Install core dependencies

pip install chromadb==0.5.0 sentence-transformers scikit-learn


### 2. Doxygen XML Parsing
Implement `DoxygenParser.java` to convert XML to AST-like structure:
public class DoxygenParser {
public Map<String, CodeArtifact> parse(String xmlPath) {
// 1. Read compounddef elements from index.xml
// 2. For each <memberdef kind="function">, extract:
// - Method signature (name, params, return type)
// - JavaDoc comments (strip HTML tags)
// - Class hierarchy context
// 3. Store as CodeArtifact objects 
}
}

*Sample CodeArtifact structure:*
public record CodeArtifact(
String id, // SHA-256 hash of signature
String code, // Method body (trimmed)
String comments, // Cleaned JavaDoc
String className,
String packageName
) {}


### 3. Embedding Generation
Configure `Embedder.java` using all-MiniLM-L6-v2 model:
public class Embedder {
private static final String MODEL = "sentence-transformers/all-MiniLM-L6-v2";
public float[] generateEmbedding(CodeArtifact artifact) {
// Combine code + comments for context
String text = artifact.comments() + "\n" + artifact.code();

// Use Python interop via Jython to run embedding model
ProcessBuilder pb = new ProcessBuilder("python", "embed.py", text);
Process p = pb.start();
// Parse float[] from stdout [2][6]

*embed.py (Python helper):*


but do it using python 
from sentence_transformers import SentenceTransformer
import sys
model = SentenceTransformer('all-MiniLM-L6-v2')
text = sys.argv
embedding = model.encode(text).tolist()
print(','.join(map(str, embedding)))


### 4. ChromaDB Initialization
Configure persistent ChromaDB in `data/chroma_db`:
public class ChromaConnector {
private final ChromaClient client;
private final Collection collection;
public ChromaConnector() {
client = new ChromaClient.Builder()
.path("data/chroma_db")
.build();

collection = client.createCollection("code_artifacts")
    .addMetadataIndex("class", MetadataFilterType.STRING)
    .addMetadataIndex("cluster", MetadataFilterType.INT);


### 5. Data Ingestion Workflow

