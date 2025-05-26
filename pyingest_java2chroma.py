import os
import logging
from typing import List
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import UnstructuredFileLoader
import glob
from tqdm import tqdm

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Validate required environment variables
required_vars = ['OPENAI_API_KEY']
missing_vars = [var for var in required_vars if not os.getenv(var)]
if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

def load_documents(directory: str) -> List:
    """Load documents from directory with error handling and progress tracking."""
    all_docs = []
    failed_files = []
    
    # Get list of all files
    files = glob.glob(f"{directory}/**/*.java", recursive=True)
    total_files = len(files)
    logger.info(f"Found {total_files} files to process")
    
    # Process files with progress bar
    for file_path in tqdm(files, desc="Loading files"):
        try:
            loader = UnstructuredFileLoader(file_path)
            docs = loader.load()
            all_docs.extend(docs)
            logger.info(f"Successfully processed: {file_path}")
        except Exception as e:
            logger.error(f"Error processing {file_path}: {str(e)}")
            failed_files.append(file_path)
            continue
    
    if failed_files:
        logger.warning(f"Failed to process {len(failed_files)} files")
        for file in failed_files:
            logger.warning(f"Failed file: {file}")
    
    return all_docs

def process_in_batches(chunks: List, batch_size: int = 100):
    """Process chunks in smaller batches to avoid memory issues and rate limits."""
    total_chunks = len(chunks)
    logger.info(f"Processing {total_chunks} chunks in batches of {batch_size}")
    
    for i in range(0, total_chunks, batch_size):
        batch = chunks[i:i + batch_size]
        try:
            logger.info(f"Processing batch {i//batch_size + 1} of {(total_chunks + batch_size - 1)//batch_size}")
            vectorstore.add_documents(batch)
            logger.info(f"Successfully added batch {i//batch_size + 1}")
        except Exception as e:
            logger.error(f"Error processing batch {i//batch_size + 1}: {str(e)}")
            # Continue with next batch even if current fails
            continue

def main():
    # Directory containing Java files
    directory = "/Users/thomaskamsker/Desktop/AKT_Docs/2025/AI/Cucocalc/code/cuco-master@d34bb6b6d1c"
    
    # Load documents
    logger.info("Loading documents...")
    documents = load_documents(directory)
    logger.info(f"Successfully loaded {len(documents)} documents")
    
    # Split documents into chunks
    logger.info("Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    chunks = text_splitter.split_documents(documents)
    logger.info(f"Split into {len(chunks)} chunks")
    
    # Initialize embeddings and vector store
    logger.info("Initializing embeddings and vector store...")
    embeddings = OpenAIEmbeddings()
    
    # Create/update collection
    collection_name = "cucocalc"
    logger.info(f"Creating/updating collection: {collection_name}")
    global vectorstore
    vectorstore = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory="./chroma_db"
    )
    
    # Process chunks in batches
    logger.info("Adding documents to collection...")
    process_in_batches(chunks)
    
    logger.info("Processing complete!")

if __name__ == "__main__":
    main()