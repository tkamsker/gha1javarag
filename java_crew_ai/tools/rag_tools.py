import os
from typing import Dict, Any
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from tree_sitter import Language, Parser
import logging

# Configure logging
logger = logging.getLogger(__name__)

class ChromaSearchInput(BaseModel):
    query: str = Field(description="The search query to find relevant code snippets")

class CodeAnalysisInput(BaseModel):
    code: str = Field(description="The Java code to analyze")

def chroma_search(query: str) -> str:
    """Search the Java codebase using ChromaDB for relevant code snippets and documentation."""
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma(
        collection_name="cucocalc",
        embedding_function=embeddings,
        persist_directory="./chroma_db"
    )
    docs = vectorstore.similarity_search(query, k=4)
    results = []
    for doc in docs:
        results.append(f"Source: {doc.metadata.get('source')}\nContent: {doc.page_content}\n")
    return "\n".join(results)

def code_analysis(code: str) -> str:
    """Analyze Java code structure and patterns."""
    # This is a placeholder for more sophisticated code analysis
    return f"Analyzing code structure and patterns for: {code[:100]}..."

class ChromaSearchTool(BaseTool):
    name = "chroma_search"
    description = "Search for code snippets in the codebase using Chroma vector store"
    
    def _run(self, query: str) -> str:
        try:
            results = self.chroma.similarity_search(query, k=3)
            return "\n\n".join([doc.page_content for doc in results])
        except Exception as e:
            return f"Error searching codebase: {str(e)}"

class CodeAnalysisTool(BaseTool):
    name = "code_analysis"
    description = "Analyze Java code and extract information about classes, methods, and their relationships"
    parser: Parser = Field(default=None, description="Tree-sitter parser for Java")
    
    def __init__(self):
        super().__init__()
        self.parser = self._initialize_parser()
    
    def _initialize_parser(self) -> Parser:
        try:
            os.makedirs('build', exist_ok=True)
            if not os.path.exists('build/my-languages.so'):
                Language.build_library(
                    'build/my-languages.so',
                    ['vendor/tree-sitter-java']
                )
            parser = Parser()
            JAVA_LANGUAGE = Language('build/my-languages.so', 'java')
            parser.set_language(JAVA_LANGUAGE)
            return parser
        except Exception as e:
            logger.error(f"Failed to initialize parser: {str(e)}")
            raise
    
    def _run(self, codebase_path: str) -> Dict[str, Any]:
        java_files = []
        for root, dirs, files in os.walk(codebase_path):
            for file in files:
                if file.endswith('.java'):
                    java_files.append(os.path.join(root, file))
        
        parsed_files = []
        for file_path in java_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                tree = self.parser.parse(bytes(code, 'utf8'))
                parsed_files.append({
                    'file': file_path,
                    'tree': str(tree.root_node.sexp())
                })
            except Exception as e:
                parsed_files.append({
                    'file': file_path,
                    'error': str(e)
                })
        return {
            'java_files': java_files,
            'parsed_files': parsed_files
        }

# Create tool instances
chroma_search_tool = ChromaSearchTool()
code_analysis_tool = CodeAnalysisTool() 