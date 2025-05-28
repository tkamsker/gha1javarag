# Product Requirements Document

## Overview
This document outlines the product requirements for the Doyen CrewAI codebase, organized by component and feature.

## User Stories


### Embedding Generator
**As a** developer, **I want** generate embeddings for code entities **so that** enable semantic search and analysis

**Component Location:** src/preprocessing


### Parser Agent
**As a** developer, **I want** analyze codebase structure **so that** understand code relationships and dependencies

**Component Location:** src/agents



## Component Details


### root


#### __init__
**Type:** module
**Documentation:** Doyen CrewAI package.




#### load_embeddings
**Type:** module
**Documentation:** Script for loading code embeddings into ChromaDB.


**Dependencies:**

- import logging

- import os

- from pathlib import Path

- import traceback

- from dotenv import load_dotenv

- from .preprocessing.xml_parser import DoxygenXMLParser

- from .preprocessing.embedding_generator import OllamaEmbeddingGenerator

- from .preprocessing.chroma_loader import ChromaDBLoader




#### main
**Type:** module
**Documentation:** Main entry point for the Doyen CrewAI application.


**Dependencies:**

- import logging

- import os

- from pathlib import Path

- import json

- from dotenv import load_dotenv

- from .agents.parser_agent import ParserAgent

- from .preprocessing.chroma_loader import ChromaDBLoader





### agents


#### __init__
**Type:** module
**Documentation:** 




#### parser_agent
**Type:** module
**Documentation:** Parser agent for analyzing codebase structure.


**Dependencies:**

- import logging

- import re

- from typing import Dict, Any, List

- from crewai import Agent, Task

- from ..preprocessing.chroma_loader import ChromaDBLoader

- from .parser_tools import (




#### parser_tools
**Type:** module
**Documentation:** Analyzes a code entity and its relationships.


**Dependencies:**

- import logging

- from typing import Type

- from crewai.tools.base_tool import BaseTool

- from pydantic import BaseModel, Field

- from ..preprocessing.chroma_loader import ChromaDBLoader





### utils


#### __init__
**Type:** module
**Documentation:** 





### preprocessing


#### xml_parser
**Type:** module
**Documentation:** Doxygen XML parser module for extracting code documentation and relationships.


**Dependencies:**

- import os

- from dataclasses import dataclass

- from pathlib import Path

- from typing import Dict, List, Optional

- from xml.etree import ElementTree

- import logging




#### chroma_loader
**Type:** module
**Documentation:** Module for loading and managing code embeddings in ChromaDB.


**Dependencies:**

- import logging

- import os

- from pathlib import Path

- from typing import Dict, List, Optional, Any, Tuple

- import numpy as np

- import chromadb

- from chromadb.config import Settings

- from dotenv import load_dotenv

- from .xml_parser import CodeEntity




#### __init__
**Type:** module
**Documentation:** Preprocessing module for code analysis.




#### embedding_generator
**Type:** module
**Documentation:** Module for generating embeddings using Ollama API.


**Dependencies:**

- import json

- import logging

- import time

- from typing import Dict, List, Optional

- import requests

- from dotenv import load_dotenv

- from .xml_parser import CodeEntity






## Non-Functional Requirements

### Performance
- All components should respond within acceptable time limits
- System should handle concurrent requests efficiently
- Embedding generation should be optimized for batch processing

### Security
- All components should follow security best practices
- Sensitive data should be properly protected
- API keys and credentials should be securely managed

### Maintainability
- Code should be well-documented
- Components should follow SOLID principles
- Dependencies should be clearly defined
- Test coverage should be maintained

### Scalability
- System should be able to handle increased load
- Components should be designed for horizontal scaling
- Embedding generation should support parallel processing 