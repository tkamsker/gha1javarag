import os
from dotenv import load_dotenv
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

# Initialize the same embeddings used during ingestion
embeddings = OpenAIEmbeddings()

# Initialize Chroma with the same configuration used during ingestion
vectorstore = Chroma(
    collection_name="cucocalc",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)

# Create a retriever that fetches the top 4 relevant chunks
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4}
)

# Initialize the LLM
llm = ChatOpenAI(
    model_name="gpt-4",
    temperature=0
)

# Build the RetrievalQA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True
)

def ask_question(question: str):
    """Ask a question and print the answer with sources."""
    print(f"\n>> Question: {question}")
    result = qa_chain({"query": question})
    print(f"Answer: {result['result']}\n")
    print("Source Chunks:")
    for doc in result['source_documents']:
        print(f"- {doc.metadata.get('source')}")

# Example questions
questions = [
    "How does the `DatabaseConnectionPool` class manage idle connections?",
    "What parameters are required to initialize the `AuthService`?",
    "Describe the error-handling strategy in the `FileUtils` utility class.",
    "Which method in `UserController` handles user registration, and what validations does it perform?",
    "How is the singleton pattern implemented for the `Logger` class?"
]

if __name__ == "__main__":
    # Ask each question
    for question in questions:
        ask_question(question)