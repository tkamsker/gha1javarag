Step 1: Read and parse source files  →  generate file-level metadata
Step 2: Batch-send content to AI     →  receive structured JSON analysis
Step 3: Update metadata with AI output
Step 4: Save to JSON + store in ChromaDB


Detailed Breakdown

✅ 1. Initial File Processing
This is handled by:

files_metadata = file_processor.process_files()
Module: FileProcessor
What it does:
Scans source directory recursively
Reads file content
Creates initial Dict for each file like:
{
  "file_path": "src/com/example/Controller.java",
  "file_type": "Java source file",
  "content": "...full file content...",
  "ai_analysis": null,
  "analysis_status": "pending"
}
📝 No AI data is added yet – this is raw file-level metadata.

✅ 2. AI-Based Requirements Analysis
analyzed_metadata = await batch_analyzer.analyze_files(files_metadata)
This uses:

class BatchAIAnalyzer:
    async def analyze_files_batch(...)
Files are grouped into batches of 3 (configurable).
A custom prompt is created asking for detailed requirements in JSON format:
{
  "purpose": "...",
  "components": [
    { "name": "...", "type": "...", "description": "..." }
  ],
  ...
}
This JSON is then injected back into the metadata like this:
file_meta.update({
  'ai_analysis': ai_analysis,  # parsed JSON
  'analysis_status': 'completed'
})
So now each file has something like:

{
  "file_path": "...",
  "file_type": "...",
  "content": "...",
  "ai_analysis": {
    "purpose": "...",
    "components": [...],
    "data_structures": [...],
    "business_rules": [...],
    "dependencies": [...]
  },
  "analysis_status": "completed"
}
✅ 3. Saving to JSON
file_processor.save_metadata(analyzed_metadata, metadata_file)
This writes metadata.json with the full analyzed metadata for later loading, e.g. in the RequirementsProcessor.

✅ 4. Storing in ChromaDB
chroma_connector.store_enhanced_metadata(file_path, content, ai_analysis)
Each file’s metadata is stored in ChromaDB as enhanced documents. Internally this likely:

Chunks the code (function/class level)
Adds AI analysis to chunk metadata
Stores:
chunk_id
start_line, end_line
function_name, class_name
complexity_score
AI-generated summaries or requirements
This results in a vector-searchable, enriched knowledge base.

🧠 Example Final Metadata for One File (in memory or metadata.json)

{
  "file_path": "src/com/example/Service.java",
  "file_type": "Java source file",
  "content": "public class Service { ... }",
  "ai_analysis": {
    "purpose": "Handles business logic for user authentication",
    "components": [
      {
        "name": "Service",
        "type": "class",
        "description": "Contains methods for login and session validation"
      }
    ],
    "data_structures": [
      {
        "name": "UserSession",
        "fields": ["token", "userId", "expiry"],
        "relationships": ["User"]
      }
    ],
    "business_rules": [
      {
        "description": "Session must expire after 30 minutes",
        "location": "validateSession()"
      }
    ],
    "dependencies": ["UserRepository", "TokenProvider"]
  },
  "analysis_status": "completed"
}
📌 Summary of Metadata Generation Flow

Stage	Responsible	Output
1. Read files	FileProcessor.process_files()	Basic metadata: path, type, content
2. AI Analysis	BatchAIAnalyzer.analyze_files_batch()	Adds ai_analysis JSON
3. Save	file_processor.save_metadata()	Writes to metadata.json
4. Store in ChromaDB	store_enhanced_metadata()	Adds chunk-level vector-searchable data



#####-------


📦 store_enhanced_metadata(file_path, content, ai_analysis)

This function likely stores AI-enriched code chunks into ChromaDB with detailed metadata for semantic search and reasoning.

Let’s reconstruct a probable version of store_enhanced_metadata():

✅ Expected Purpose
Break down a file into code chunks (functions, classes), and store each with:

the code content
metadata (location, class/method name, etc.)
the AI-generated analysis (e.g. purpose, components, business rules)
🔍 Likely Internal Structure of store_enhanced_metadata()

from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from chromadb.config import Settings
import chromadb
import hashlib
import uuid

class EnhancedChromaDBConnector:
    def __init__(self):
        self.client = chromadb.Client(Settings(persist_directory="./chroma_db"))
        self.collection = self.client.get_or_create_collection(name="code_chunks")

        # Could also use OpenAI embeddings or custom ones
        self.embedding_fn = OpenAIEmbeddingFunction(api_key=os.getenv("OPENAI_API_KEY"))

    def store_enhanced_metadata(self, file_path: str, content: str, ai_analysis: dict):
        chunks = self._chunk_code(content)
        
        for i, chunk in enumerate(chunks):
            doc_id = self._generate_chunk_id(file_path, i)
            metadata = {
                "file_path": file_path,
                "chunk_index": i,
                "chunk_type": chunk.get("type"),
                "function_name": chunk.get("function_name", ""),
                "class_name": chunk.get("class_name", ""),
                "start_line": chunk.get("start_line", ""),
                "end_line": chunk.get("end_line", ""),
                "language": "java",
                "complexity_score": chunk.get("complexity_score", "1.0"),
                "ai_analysis": json.dumps(ai_analysis)  # Store as string
            }

            self.collection.add(
                documents=[chunk["content"]],
                metadatas=[metadata],
                ids=[doc_id]
            )

    def _chunk_code(self, content: str) -> List[dict]:
        # Very simplified chunking logic for demo purposes
        chunks = []
        lines = content.splitlines()
        current_chunk = []
        current_function = None
        start_line = 0

        for idx, line in enumerate(lines):
            if "class " in line or "void " in line or "public " in line:
                if current_chunk:
                    chunks.append({
                        "type": "function",
                        "function_name": current_function or "unknown",
                        "content": "\n".join(current_chunk),
                        "start_line": start_line,
                        "end_line": idx,
                        "complexity_score": "1.0"
                    })
                    current_chunk = []
                current_function = line.strip()
                start_line = idx
            current_chunk.append(line)

        if current_chunk:
            chunks.append({
                "type": "function",
                "function_name": current_function or "unknown",
                "content": "\n".join(current_chunk),
                "start_line": start_line,
                "end_line": len(lines),
                "complexity_score": "1.0"
            })

        return chunks

    def _generate_chunk_id(self, file_path: str, index: int) -> str:
        return hashlib.sha256(f"{file_path}-{index}".encode()).hexdigest()[:32]
🔎 Summary of Internal Logic

Step	Description
content	Full file code is passed in
_chunk_code()	Splits the file into functions/classes (chunks)
metadata	Adds file path, chunk type, AI results, etc.
embedding function	Embeds each chunk (e.g., via OpenAI or SentenceTransformers)
ChromaDB collection	Stores each chunk with its metadata and vector
🧠 What Makes it "Enhanced"

Each chunk stores:
semantic vector
AI output (purpose, rules, etc.)
function/class name
line range
complexity score
This enables querying like:
“Show me complex authentication logic”
“Find all classes related to payment processing”
Optional Add-ons
You could also store:

git_commit_hash (to track code version)
dependencies from AI analysis
a requirements_summary extracted per chunk