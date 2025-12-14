"""
Extraction service for semantic code analysis.

Orchestrates parsers and AI to extract structural and semantic information.
"""

import logging
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any
from datetime import datetime

from codeindex.models import ArtifactType
from codeindex.models.extraction import ExtractionResult
from codeindex.parsers import (
    JavaParser,
    JSPParser,
    XMLParser,
    SQLParser,
)
from codeindex.services.ollama_client import OllamaClient, create_ollama_client
from codeindex.utils.config import Config, get_config

logger = logging.getLogger(__name__)


# ==============================================================================
# ExtractionService Class
# ==============================================================================

class ExtractionService:
    """
    Service for extracting structural and semantic information from code files.

    Combines parser output (structural) with AI analysis (semantic).
    """

    def __init__(
        self,
        config: Optional[Config] = None,
        ollama_client: Optional[OllamaClient] = None
    ):
        """
        Initialize extraction service.

        Args:
            config: Configuration instance
            ollama_client: Optional Ollama client (for testing)
        """
        self.config = config or get_config()
        self.logger = logging.getLogger(__name__)

        # Initialize Ollama client
        if ollama_client:
            self.ollama_client = ollama_client
        else:
            self.ollama_client = create_ollama_client(
                base_url=self.config.ollama_base_url,
                model=self.config.ollama_model_name
            )

        # Initialize parsers
        self.java_parser = JavaParser()
        self.jsp_parser = JSPParser()
        self.xml_parser = XMLParser()
        self.sql_parser = SQLParser()

    def extract_file(
        self,
        file_path: Path,
        artifact_type: ArtifactType,
        pom_context: Optional[str] = None
    ) -> ExtractionResult:
        """
        Extract structural and semantic information from a file.

        Args:
            file_path: Path to file
            artifact_type: Type of artifact
            pom_context: Optional POM context for Java files

        Returns:
            ExtractionResult with structural and semantic data

        Raises:
            FileNotFoundError: If file doesn't exist
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        self.logger.info(f"Extracting {artifact_type.value}: {file_path}")

        try:
            # 1. Extract structural information
            structural_data = self._extract_structural(file_path, artifact_type)

            # 2. Extract semantic information
            semantic_data = self._extract_semantic(
                file_path,
                artifact_type,
                pom_context
            )

            # 3. Create result
            result = ExtractionResult(
                file_path=str(file_path),
                artifact_type=artifact_type,
                structural_data=structural_data,
                semantic_data=semantic_data,
                extracted_at=datetime.utcnow()
            )

            self.logger.debug(f"Extraction complete: {file_path.name}")
            return result

        except Exception as e:
            self.logger.error(f"Error extracting {file_path}: {e}", exc_info=True)

            # Return partial result with error
            return ExtractionResult(
                file_path=str(file_path),
                artifact_type=artifact_type,
                structural_data={},
                semantic_data={'error': str(e)},
                extracted_at=datetime.utcnow(),
                error=str(e)
            )

    def extract_batch(
        self,
        files: List[Tuple[Path, ArtifactType]],
        pom_context: Optional[str] = None
    ) -> List[ExtractionResult]:
        """
        Extract multiple files in batch.

        Args:
            files: List of (file_path, artifact_type) tuples
            pom_context: Optional POM context

        Returns:
            List of extraction results
        """
        results = []

        for file_path, artifact_type in files:
            try:
                result = self.extract_file(file_path, artifact_type, pom_context)
                results.append(result)
            except Exception as e:
                self.logger.error(f"Error in batch extraction: {e}")
                # Create error result
                error_result = ExtractionResult(
                    file_path=str(file_path),
                    artifact_type=artifact_type,
                    structural_data={},
                    semantic_data={},
                    extracted_at=datetime.utcnow(),
                    error=str(e)
                )
                results.append(error_result)

        return results

    def extract_from_inventory(
        self,
        inventory_path: Path
    ) -> List[ExtractionResult]:
        """
        Extract files from discovery inventory.

        Args:
            inventory_path: Path to discovery inventory JSONL

        Returns:
            List of extraction results
        """
        self.logger.info(f"Extracting from inventory: {inventory_path}")

        # Load inventory
        inventory = load_inventory(inventory_path)

        # Build file list
        files = []
        for file_info in inventory.get('files', []):
            file_path = Path(file_info['path'])
            artifact_type = ArtifactType[file_info['type']]
            files.append((file_path, artifact_type))

        # Extract in batch
        return self.extract_batch(files)

    def _extract_structural(
        self,
        file_path: Path,
        artifact_type: ArtifactType
    ) -> Dict[str, Any]:
        """
        Extract structural information using appropriate parser.

        Args:
            file_path: Path to file
            artifact_type: Type of artifact

        Returns:
            Dictionary with structural data
        """
        try:
            if artifact_type in (ArtifactType.JAVA_SOURCE, ArtifactType.JAVA_TEST):
                return self.java_parser.parse_file(file_path)

            elif artifact_type == ArtifactType.JSP_VIEW:
                return self.jsp_parser.parse_file(file_path)

            elif artifact_type in (
                ArtifactType.XML_CONFIG,
                ArtifactType.IBATIS_MAPPING,
                ArtifactType.ORM_MAPPING,
                ArtifactType.GWT_MODULE,
                ArtifactType.GWT_UI_BINDER
            ):
                return self.xml_parser.parse_file(file_path)

            elif artifact_type in (ArtifactType.SQL_SCHEMA, ArtifactType.SQL_QUERY):
                return self.sql_parser.parse_file(file_path)

            else:
                # Unsupported type - return minimal data
                self.logger.warning(f"No parser for artifact type: {artifact_type}")
                return {
                    'type': artifact_type.value,
                    'file_name': file_path.name
                }

        except Exception as e:
            self.logger.error(f"Structural extraction error: {e}", exc_info=True)
            return {'parse_error': str(e)}

    def _extract_semantic(
        self,
        file_path: Path,
        artifact_type: ArtifactType,
        pom_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Extract semantic information using AI.

        Args:
            file_path: Path to file
            artifact_type: Type of artifact
            pom_context: Optional POM context

        Returns:
            Dictionary with semantic data
        """
        # Skip semantic extraction for binary file types (images, fonts, etc.)
        if artifact_type == ArtifactType.STATIC_ASSET:
            return self._create_fallback_semantic(file_path, artifact_type)

        try:
            # Read file content
            content = file_path.read_text(encoding='utf-8')

            # Call Ollama for semantic extraction
            semantic_data = self.ollama_client.extract_semantics(
                str(file_path),
                content,
                artifact_type,
                pom_context
            )

            return semantic_data

        except (ConnectionError, TimeoutError) as e:
            # Ollama unavailable - return minimal fallback
            self.logger.warning(f"Ollama unavailable, using fallback: {e}")
            return self._create_fallback_semantic(file_path, artifact_type)

        except Exception as e:
            self.logger.error(f"Semantic extraction error: {e}", exc_info=True)
            return self._create_fallback_semantic(file_path, artifact_type)

    def _create_fallback_semantic(
        self,
        file_path: Path,
        artifact_type: ArtifactType
    ) -> Dict[str, Any]:
        """
        Create fallback semantic data when AI is unavailable.

        Args:
            file_path: Path to file
            artifact_type: Type of artifact

        Returns:
            Minimal semantic data
        """
        return {
            'summary': f"{artifact_type.value}: {file_path.name}",
            'roles': [],
            'entities': [],
            'tags': [artifact_type.value],
            'language': artifact_type.value,
            'frameworks': [],
            'concerns': [],
            'dependencies': [],
            'ai_unavailable': True
        }


# ==============================================================================
# Helper Functions
# ==============================================================================

def load_inventory(inventory_path: Path) -> Dict[str, Any]:
    """
    Load discovery inventory from JSONL.

    Args:
        inventory_path: Path to inventory file

    Returns:
        Inventory data structure
    """
    import json

    if not inventory_path.exists():
        raise FileNotFoundError(f"Inventory not found: {inventory_path}")

    inventory = {
        'files': []
    }

    # Read JSONL
    with inventory_path.open('r') as f:
        for line in f:
            if line.strip():
                data = json.loads(line)

                # First line is metadata
                if 'scan_timestamp' in data:
                    inventory.update(data)
                # Subsequent lines are file entries
                elif 'file_path' in data or 'path' in data:
                    inventory['files'].append(data)

    return inventory


# ==============================================================================
# Standalone Functions
# ==============================================================================

def extract_file(
    file_path: Path,
    artifact_type: ArtifactType,
    pom_context: Optional[str] = None
) -> ExtractionResult:
    """
    Extract file (convenience function).

    Args:
        file_path: Path to file
        artifact_type: Type of artifact
        pom_context: Optional POM context

    Returns:
        Extraction result
    """
    service = ExtractionService()
    return service.extract_file(file_path, artifact_type, pom_context)


def extract_from_inventory(inventory_path: Path) -> List[ExtractionResult]:
    """
    Extract from inventory (convenience function).

    Args:
        inventory_path: Path to inventory JSONL

    Returns:
        List of extraction results
    """
    service = ExtractionService()
    return service.extract_from_inventory(inventory_path)
