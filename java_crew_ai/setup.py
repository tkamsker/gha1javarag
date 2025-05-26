from setuptools import setup, find_packages

setup(
    name="java_crew_ai",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "crewai>=0.11.0",
        "langchain>=0.1.0",
        "langchain-community>=0.0.10",
        "langchain-openai>=0.0.2",
        "chromadb>=0.4.22",
        "python-dotenv>=1.0.0",
        "openai>=1.12.0",
        "tqdm>=4.66.1"
    ],
) 