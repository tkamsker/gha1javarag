from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from crewai.tools.base_tool import Tool
from pydantic import BaseModel, Field

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

# Create tool instances using CrewAI's Tool class
chroma_search_tool = Tool(
    name="chroma_search",
    description="Search the Java codebase using ChromaDB for relevant code snippets and documentation",
    func=chroma_search,
    args_schema=ChromaSearchInput
)

code_analysis_tool = Tool(
    name="code_analysis",
    description="Analyze Java code structure and patterns",
    func=code_analysis,
    args_schema=CodeAnalysisInput
) 