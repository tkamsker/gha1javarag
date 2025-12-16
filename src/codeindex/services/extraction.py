"""
Extraction service for semantic code analysis.

Orchestrates parsers and AI to extract structural and semantic information.
"""

import logging
import re
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any
from datetime import datetime

from codeindex.models import ArtifactType
from codeindex.models.extraction import ExtractionResult
from codeindex.models.dto_artifact import DtoArtifact
from codeindex.parsers import (
    JavaParser,
    JSPParser,
    XMLParser,
    SQLParser,
)
from codeindex.parsers.java_parser import extract_dto_metadata
from codeindex.services.classifier import classify_dto
from codeindex.services.ollama_client import OllamaClient, create_ollama_client
from codeindex.services.gwt_analyzer_registry import get_gwt_analyzer_registry
from codeindex.utils.config import Config, get_config

logger = logging.getLogger(__name__)


# ==============================================================================
# Helper Functions
# ==============================================================================

def detect_file_encoding(file_path: Path) -> str:
    """
    Detect the encoding of a file, with special handling for XML files.

    For XML files, attempts to read the encoding from the XML declaration.
    Falls back to trying common encodings if UTF-8 fails.

    Args:
        file_path: Path to the file

    Returns:
        Detected encoding name (e.g., 'utf-8', 'windows-1252')
    """
    # Try to detect encoding from XML declaration (first 1024 bytes)
    try:
        with open(file_path, 'rb') as f:
            raw_content = f.read(1024)

        # Look for XML encoding declaration
        # Pattern: <?xml version="1.0" encoding="ENCODING"?>
        encoding_match = re.search(
            rb'<\?xml[^?]*encoding=["\']([^"\']+)["\']',
            raw_content,
            re.IGNORECASE
        )

        if encoding_match:
            detected_encoding = encoding_match.group(1).decode('ascii').upper()
            # Normalize encoding names
            encoding_map = {
                'WINDOWS-1252': 'cp1252',
                'ISO-8859-1': 'iso-8859-1',
                'UTF-8': 'utf-8',
                'UTF-16': 'utf-16',
                'US-ASCII': 'ascii'
            }
            normalized = encoding_map.get(detected_encoding, detected_encoding.lower())
            logger.debug(f"Detected encoding from XML declaration: {normalized} for {file_path.name}")
            return normalized

    except Exception as e:
        logger.debug(f"Could not detect encoding from XML declaration: {e}")

    # Default to UTF-8
    return 'utf-8'


def read_file_with_fallback(file_path: Path) -> str:
    """
    Read file content with automatic encoding detection and fallback.

    Tries encodings in this order:
    1. Detected encoding from XML declaration (if XML file)
    2. UTF-8
    3. WINDOWS-1252 (common for German/European files)
    4. ISO-8859-1 (Latin-1)
    5. CP1252 (Windows Western European)
    6. UTF-8 with error replacement (guaranteed to work)

    Args:
        file_path: Path to the file

    Returns:
        File content as string

    Raises:
        IOError: If file cannot be read
    """
    # Detect encoding from XML declaration if applicable
    detected_encoding = detect_file_encoding(file_path)

    # List of encodings to try
    encodings_to_try = [detected_encoding]

    # Add fallback encodings (avoid duplicates)
    fallback_encodings = ['utf-8', 'cp1252', 'iso-8859-1', 'latin-1']
    for enc in fallback_encodings:
        if enc not in encodings_to_try:
            encodings_to_try.append(enc)

    # Try each encoding
    for encoding in encodings_to_try:
        try:
            content = file_path.read_text(encoding=encoding)
            if encoding != 'utf-8':
                logger.debug(f"Successfully read {file_path.name} with encoding: {encoding}")
            return content
        except (UnicodeDecodeError, LookupError) as e:
            logger.debug(f"Failed to read {file_path.name} with {encoding}: {e}")
            continue

    # Last resort: UTF-8 with error replacement
    logger.warning(
        f"All encoding attempts failed for {file_path.name}, "
        "using UTF-8 with character replacement"
    )
    return file_path.read_text(encoding='utf-8', errors='replace')


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
                # Parse Java file normally
                structural_data = self.java_parser.parse_file(file_path)

                # Run DTO classification (T062)
                try:
                    classification_result = classify_dto(file_path)

                    # If classified as DTO, extract full DTO metadata (T063)
                    if classification_result.is_dto:
                        self.logger.debug(
                            f"DTO detected: {file_path.name} "
                            f"(confidence: {classification_result.confidence:.1f})"
                        )

                        # Extract DTO metadata (fields, validation annotations, etc.)
                        dto_metadata = extract_dto_metadata(file_path)

                        # Create DtoArtifact from classification and metadata
                        from codeindex.models.dto_artifact import DtoField

                        # Convert metadata fields to DtoField objects
                        dto_fields = []
                        for field_data in dto_metadata.get('fields', []):
                            dto_field = DtoField(
                                name=field_data['name'],
                                field_type=field_data['field_type'],
                                modifiers=field_data.get('modifiers', []),
                                is_nested_dto=field_data.get('is_nested_dto', False),
                                validation_annotations=field_data.get('validation_annotations', []),
                                is_collection=field_data.get('is_collection', False),
                                collection_type=field_data.get('collection_type'),
                                generic_types=field_data.get('generic_types', [])
                            )
                            dto_fields.append(dto_field)

                        # Create DtoArtifact
                        dto_artifact = DtoArtifact.from_classification(
                            file_path=file_path,
                            classification=classification_result,
                            fields=dto_fields
                        )

                        # Store DtoArtifact in structural data
                        structural_data['dto_artifact'] = dto_artifact
                        structural_data['is_dto'] = True
                        structural_data['dto_confidence'] = classification_result.confidence
                    else:
                        structural_data['is_dto'] = False

                except Exception as dto_error:
                    self.logger.warning(
                        f"DTO classification failed for {file_path.name}: {dto_error}"
                    )
                    structural_data['is_dto'] = False

                return structural_data

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
            # Read file content with automatic encoding detection
            content = read_file_with_fallback(file_path)

            # Check if GWT analyzer can handle this file
            gwt_registry = get_gwt_analyzer_registry()
            gwt_metadata = None

            if gwt_registry.can_analyze(file_path, artifact_type):
                self.logger.debug(f"Routing {file_path.name} to GWT analyzer")
                gwt_metadata = gwt_registry.analyze(
                    file_path,
                    artifact_type,
                    content,
                    semantic_data=None  # GWT analyzer runs first, before Ollama
                )

            # Call Ollama for semantic extraction
            semantic_data = self.ollama_client.extract_semantics(
                str(file_path),
                content,
                artifact_type,
                pom_context
            )

            # Merge GWT metadata with Ollama semantic data
            if gwt_metadata:
                self.logger.debug(f"Merging GWT metadata for {file_path.name}")
                semantic_data.update(gwt_metadata)

            return semantic_data

        except TimeoutError as e:
            # Ollama timeout - skip this file to avoid long delays
            self.logger.warning(
                f"Skipping {file_path.name}: Ollama timeout after 60s (file too complex/large). "
                f"Using structural-only analysis."
            )
            return self._create_fallback_semantic(file_path, artifact_type, timeout=True)

        except ConnectionError as e:
            # Ollama unavailable - return minimal fallback
            self.logger.warning(f"Ollama unavailable, using fallback: {e}")
            return self._create_fallback_semantic(file_path, artifact_type)

        except Exception as e:
            self.logger.error(f"Semantic extraction error: {e}", exc_info=True)
            return self._create_fallback_semantic(file_path, artifact_type)

    def _create_fallback_semantic(
        self,
        file_path: Path,
        artifact_type: ArtifactType,
        timeout: bool = False
    ) -> Dict[str, Any]:
        """
        Create fallback semantic data when AI is unavailable.

        Args:
            file_path: Path to file
            artifact_type: Type of artifact
            timeout: Whether fallback is due to timeout

        Returns:
            Minimal semantic data
        """
        summary_prefix = "(TIMEOUT) " if timeout else ""
        return {
            'summary': f"{summary_prefix}{artifact_type.value}: {file_path.name}",
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
