from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class Project:
    project_name: str

@dataclass
class DiscoveredFile:
    project_name: str
    file_path: str
    file_type: str

@dataclass
class CodeArtifact:
    artifact_id: str
    project_name: str
    file_path: str
    artifact_type: str
    language: str
    content_for_embedding: str
    framework: str = ""
    details: Dict[str, Any] = field(default_factory=dict)
