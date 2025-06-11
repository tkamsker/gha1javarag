# Iteration 4b: Semantic Code Search & Clustering Application improvement 

**Goal:**  
keep in mind all from @iteration4.md file as base 
improve the semantic code search and clustering app when you ingests Doxygen XML from Java projects, serach also for the depending source code starting from JAVA_SOURCE_DIR in consideration when you embed the code.
the xml structure of doxygen is only the map through the whole code and to group applications. the sourcecode needs to be embedded as well with propper meta data for further use. We will have the main programm to generate the chroma db embeddings as of now. And then we have several query applications which extract several requirements like get_persistence to retrieve datbase structures and dao objetcs. 

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


JAVA_SOURCE_DIR should be set to /Users/thomaskamsker/Desktop/AKT_Docs/2025/AI/Cucocalc/code/HospitalManagementSysyem