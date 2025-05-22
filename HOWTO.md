# How to Test and Load Java Code into the RAG System

This guide will walk you through the process of setting up, testing, and loading Java code into the RAG (Retrieval-Augmented Generation) system.

## Prerequisites

1. Python 3.11 or higher
2. Java Development Kit (JDK) installed
3. Git (for cloning repositories)

## Step 1: Set Up the Environment

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Step 2: Build Tree-sitter Java Parser

1. Create a build directory:
```bash
mkdir build
```

2. Build the Tree-sitter Java parser:
```bash
tree-sitter generate
tree-sitter build-wasm
```

3. Verify the build:
```bash
ls build/my-languages.so
```

## Step 3: Test the Java Code Processing

1. Create a test directory for Java files:
```bash
mkdir -p test/java
```

2. Create a sample Java file for testing:
```bash
cat > test/java/TestClass.java << 'EOF'
public class TestClass {
    private String name;
    
    public TestClass(String name) {
        this.name = name;
    }
    
    public String getName() {
        return name;
    }
    
    public void setName(String name) {
        this.name = name;
    }
}
EOF
```

3. Create a test script:
```bash
cat > test_processor.py << 'EOF'
from src.ingestion.file_processor import FileProcessor
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_java_processing():
    try:
        # Initialize the processor
        processor = FileProcessor(
            java_so_path="build/my-languages.so",
            max_workers=4,
            batch_size=100,
            chunk_size=1000,
            chunk_overlap=100
        )
        
        # Process the test directory
        processor.process_directory("test/java")
        
        # Test search functionality
        results = processor.search_code(
            query="class with name property",
            file_types=["java"],
            n_results=5
        )
        
        # Print results
        for result in results:
            print("\nFound code segment:")
            print(f"File: {result['metadata']['file_path']}")
            print(f"Type: {result['metadata']['type']}")
            print(f"Code:\n{result['code']}")
            
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        raise

if __name__ == "__main__":
    test_java_processing()
EOF
```

4. Run the test:
```bash
python test_processor.py
```

## Step 4: Load Your Java Codebase

1. Create a directory for your Java codebase:
```bash
mkdir -p java_codebase
```

2. Copy your Java files into the directory:
```bash
cp -r /path/to/your/java/files/* java_codebase/
```

3. Create a script to process your codebase:
```bash
cat > process_codebase.py << 'EOF'
from src.ingestion.file_processor import FileProcessor
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_java_codebase():
    try:
        start_time = time.time()
        
        # Initialize the processor
        processor = FileProcessor(
            java_so_path="build/my-languages.so",
            max_workers=4,
            batch_size=100,
            chunk_size=1000,
            chunk_overlap=100
        )
        
        # Process the codebase
        processor.process_directory("java_codebase")
        
        end_time = time.time()
        logger.info(f"Processing completed in {end_time - start_time:.2f} seconds")
        
    except Exception as e:
        logger.error(f"Processing failed: {str(e)}")
        raise

if __name__ == "__main__":
    process_java_codebase()
EOF
```

4. Run the processing script:
```bash
python process_codebase.py
```

## Step 5: Verify the Results

1. Create a search script:
```bash
cat > search_code.py << 'EOF'
from src.ingestion.file_processor import FileProcessor
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def search_java_code():
    try:
        # Initialize the processor
        processor = FileProcessor(
            java_so_path="build/my-languages.so"
        )
        
        # Example search queries
        queries = [
            "Find all class declarations",
            "Search for methods that handle user input",
            "Look for database connection code"
        ]
        
        for query in queries:
            print(f"\nSearching for: {query}")
            results = processor.search_code(
                query=query,
                file_types=["java"],
                n_results=5
            )
            
            for result in results:
                print("\nFound code segment:")
                print(f"File: {result['metadata']['file_path']}")
                print(f"Type: {result['metadata']['type']}")
                print(f"Code:\n{result['code']}")
                
    except Exception as e:
        logger.error(f"Search failed: {str(e)}")
        raise

if __name__ == "__main__":
    search_java_code()
EOF
```

2. Run the search script:
```bash
python search_code.py
```

## Troubleshooting

1. If you encounter Tree-sitter build issues:
   - Ensure you have the latest version of tree-sitter-cli
   - Check if the Java grammar is properly installed
   - Verify the build directory permissions

2. If ChromaDB connection fails:
   - Check your network connection
   - Verify the ChromaDB server is running
   - Check the server URL and port configuration

3. If file processing fails:
   - Check file permissions
   - Verify Java file encoding (should be UTF-8)
   - Check for syntax errors in Java files

## Best Practices

1. File Organization:
   - Keep Java files in a dedicated directory
   - Use consistent file naming conventions
   - Maintain proper package structure

2. Processing:
   - Process files in batches for large codebases
   - Monitor memory usage during processing
   - Use appropriate chunk sizes for your codebase

3. Search:
   - Use specific, targeted search queries
   - Filter by file types when appropriate
   - Review and refine search results

## Additional Resources

- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Tree-sitter Documentation](https://tree-sitter.github.io/tree-sitter/)
- [Java Language Specification](https://docs.oracle.com/javase/specs/) 