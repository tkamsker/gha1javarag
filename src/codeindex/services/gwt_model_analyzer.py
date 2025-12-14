"""
GWT Model Analyzer

Analyzes GWT Data Transfer Objects (DTOs) to extract:
- Field definitions with types and descriptions
- Validation rules (@NotNull, @Size, @Email, @Pattern, etc.)
- GWT serialization checks (IsSerializable, default constructor)
- Nested DTO references

Implements FR-006 from the specification.
"""

import logging
import re
from pathlib import Path
from typing import List, Dict, Any, Optional

from codeindex.parsers.hybrid_java_parser import HybridJavaParser
from codeindex.utils.gwt_patterns import GwtRole


logger = logging.getLogger(__name__)


class GwtModelAnalyzer:
    """
    Analyzer for GWT Data Transfer Objects.

    Extracts field definitions, validation rules, and serialization metadata
    from shared DTO classes.
    """

    # Validation annotation patterns
    VALIDATION_ANNOTATIONS = {
        'NotNull': r'@NotNull\s*(?:\(message\s*=\s*"([^"]+)"\))?',
        'Size': r'@Size\s*\(\s*(?:min\s*=\s*(\d+)\s*,?\s*)?(?:max\s*=\s*(\d+)\s*,?\s*)?(?:message\s*=\s*"([^"]+)"\s*)?\)',
        'Email': r'@Email\s*(?:\(message\s*=\s*"([^"]+)"\))?',
        'Pattern': r'@Pattern\s*\(\s*regexp\s*=\s*"([^"]+)"(?:\s*,\s*message\s*=\s*"([^"]+)")?\s*\)',
        'Min': r'@Min\s*\(\s*value?\s*=?\s*(\d+)\s*(?:,\s*message\s*=\s*"([^"]+)")?\s*\)',
        'Max': r'@Max\s*\(\s*value?\s*=?\s*(\d+)\s*(?:,\s*message\s*=\s*"([^"]+)")?\s*\)',
    }

    def __init__(self):
        """Initialize GWT Model analyzer."""
        self.logger = logging.getLogger(__name__)
        self.parser = HybridJavaParser()

    def can_analyze(self, file_path: Path) -> bool:
        """
        Check if this analyzer can handle the file.

        Args:
            file_path: Path to Java file

        Returns:
            True if file is a GWT DTO
        """
        # Check file name pattern
        file_name = file_path.name
        if not file_name.endswith('DTO.java'):
            return False

        # Quick content check for DTO indicators
        try:
            content = file_path.read_text(encoding='utf-8')
            return any([
                'IsSerializable' in content,
                'implements Serializable' in content,
                'serialVersionUID' in content,
                # Check if in shared package
                'package' in content and 'shared' in content
            ])
        except Exception:
            return False

    def get_gwt_role(self) -> GwtRole:
        """
        Return the GWT role this analyzer produces.

        Returns:
            GwtRole.SHARED_DTO
        """
        return GwtRole.SHARED_DTO

    def analyze(
        self,
        file_path: Path,
        content: str,
        semantic_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analyze GWT DTO and extract metadata.

        Args:
            file_path: Path to DTO file
            content: Java source code
            semantic_data: Optional LLM-extracted semantic data

        Returns:
            Dictionary with GWT DTO metadata
        """
        self.logger.debug(f"Analyzing GWT DTO: {file_path.name}")

        try:
            # Extract class information
            class_info = self.parser.extract_class_info(content)

            # Extract DTO fields
            fields = self.extract_dto_fields(content)

            # Check GWT serialization
            serialization_info = self.check_gwt_serializable(content, class_info)

            # Detect nested DTOs
            nested_dtos = self._detect_nested_dtos(content, fields)

            # Detect inner classes
            inner_classes = self._detect_inner_classes(content)

            # Build metadata
            metadata = {
                'gwt_role': GwtRole.SHARED_DTO.value,
                'dto_name': class_info.get('class_name', file_path.stem),
                'package': class_info.get('package', ''),
                'fields': fields,
                'nested_dtos': nested_dtos,
                'inner_classes': inner_classes,
                **serialization_info,
                'warnings': []
            }

            # Add validation warnings
            if not serialization_info['has_default_constructor']:
                metadata['warnings'].append(
                    "Missing default constructor - required for GWT serialization"
                )

            if not serialization_info['gwt_serializable'] and not serialization_info['java_serializable']:
                metadata['warnings'].append(
                    "DTO does not implement Serializable or IsSerializable"
                )

            self.logger.info(
                f"Extracted DTO metadata from {file_path.name}: "
                f"fields={len(fields)}, "
                f"nested_dtos={len(nested_dtos)}"
            )

            return metadata

        except Exception as e:
            self.logger.error(f"Error analyzing GWT DTO {file_path}: {e}", exc_info=True)
            return {
                'gwt_role': GwtRole.SHARED_DTO.value,
                'dto_name': file_path.stem,
                'fields': [],
                'nested_dtos': [],
                'inner_classes': [],
                'gwt_serializable': False,
                'java_serializable': False,
                'has_default_constructor': False,
                'has_serial_version_uid': False,
                'warnings': [],
                'error': str(e)
            }

    def extract_dto_fields(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract DTO fields using hybrid parser.

        Args:
            content: Java source code

        Returns:
            List of field dictionaries with types, descriptions, and validation rules
        """
        fields = []

        # Pattern to match field declarations with optional Javadoc
        field_pattern = r'(?:/\*\*\s*(.*?)\s*\*/\s*)?(?:@\w+[^\n]*\s*)*private\s+(\w+(?:<[^>]+>)?)\s+(\w+)\s*;'

        for match in re.finditer(field_pattern, content, re.DOTALL):
            javadoc = match.group(1)
            field_type = match.group(2)
            field_name = match.group(3)

            # Extract validation rules for this field
            validation_rules = self.extract_validation_rules(content, field_name)

            # Clean up Javadoc
            description = None
            if javadoc:
                # Remove Javadoc stars and extra whitespace
                description = re.sub(r'\s*\*\s*', ' ', javadoc).strip()

            fields.append({
                'name': field_name,
                'type': field_type,
                'description': description,
                'validation_rules': validation_rules
            })

        self.logger.debug(f"Extracted {len(fields)} DTO fields")
        return fields

    def extract_validation_rules(
        self,
        content: str,
        field_name: str
    ) -> List[Dict[str, Any]]:
        """
        Extract validation rules for a specific field.

        Args:
            content: Java source code
            field_name: Name of field to extract rules for

        Returns:
            List of validation rule dictionaries
        """
        rules = []

        # Find field declaration with annotations
        field_section_pattern = rf'((?:@\w+[^\n]*\s*)*)\s*private\s+\w+(?:<[^>]+>)?\s+{re.escape(field_name)}\s*;'
        field_match = re.search(field_section_pattern, content, re.DOTALL)

        if not field_match:
            return rules

        annotations_text = field_match.group(1)

        # Extract each type of validation annotation
        for annotation_type, pattern in self.VALIDATION_ANNOTATIONS.items():
            for match in re.finditer(pattern, annotations_text):
                rule = {'type': annotation_type}

                # Extract specific attributes based on annotation type
                if annotation_type == 'NotNull':
                    if match.group(1):
                        rule['message'] = match.group(1)
                    else:
                        rule['message'] = f"{field_name} is required"

                elif annotation_type == 'Size':
                    if match.group(1):
                        rule['min'] = int(match.group(1))
                    if match.group(2):
                        rule['max'] = int(match.group(2))
                    if match.group(3):
                        rule['message'] = match.group(3)

                elif annotation_type == 'Email':
                    if match.group(1):
                        rule['message'] = match.group(1)
                    else:
                        rule['message'] = "Must be a valid email address"

                elif annotation_type == 'Pattern':
                    rule['regexp'] = match.group(1)
                    if match.group(2):
                        rule['message'] = match.group(2)

                elif annotation_type in ['Min', 'Max']:
                    rule['value'] = int(match.group(1))
                    if match.group(2):
                        rule['message'] = match.group(2)

                rules.append(rule)

        return rules

    def check_gwt_serializable(
        self,
        content: str,
        class_info: Dict[str, Any]
    ) -> Dict[str, bool]:
        """
        Check GWT serialization requirements.

        Args:
            content: Java source code
            class_info: Parsed class information

        Returns:
            Dictionary with serialization flags
        """
        # Check for IsSerializable interface
        implements = class_info.get('implements', [])
        gwt_serializable = 'IsSerializable' in implements or 'IsSerializable' in content

        # Check for Serializable interface
        java_serializable = 'Serializable' in implements or 'implements Serializable' in content

        # Check for serialVersionUID
        has_serial_version_uid = 'serialVersionUID' in content

        # Check for default constructor (no parameters)
        has_default_constructor = self._has_default_constructor(content, class_info)

        return {
            'gwt_serializable': gwt_serializable,
            'java_serializable': java_serializable,
            'has_serial_version_uid': has_serial_version_uid,
            'has_default_constructor': has_default_constructor
        }

    def _has_default_constructor(
        self,
        content: str,
        class_info: Dict[str, Any]
    ) -> bool:
        """
        Check if DTO has a default (no-arg) constructor.

        Args:
            content: Java source code
            class_info: Parsed class information

        Returns:
            True if default constructor exists
        """
        class_name = class_info.get('class_name', '')

        if not class_name:
            return False

        # Pattern for default constructor: public ClassName() { ... }
        default_constructor_pattern = rf'public\s+{re.escape(class_name)}\s*\(\s*\)\s*\{{'

        return bool(re.search(default_constructor_pattern, content))

    def _detect_nested_dtos(
        self,
        content: str,
        fields: List[Dict[str, Any]]
    ) -> List[Dict[str, str]]:
        """
        Detect nested DTO references in fields.

        Args:
            content: Java source code
            fields: Extracted field list

        Returns:
            List of nested DTO references
        """
        nested = []
        seen = set()

        for field in fields:
            field_type = field['type']

            # Extract DTO class names from field types
            # Handles: UserDTO, List<UserDTO>, Set<UserDTO>, Map<String, UserDTO>
            dto_pattern = r'(\w+DTO)'
            for match in re.finditer(dto_pattern, field_type):
                dto_name = match.group(1)

                if dto_name not in seen:
                    nested.append({
                        'name': dto_name,
                        'field': field['name']
                    })
                    seen.add(dto_name)

        return nested

    def _detect_inner_classes(self, content: str) -> List[Dict[str, str]]:
        """
        Detect inner class DTOs.

        Args:
            content: Java source code

        Returns:
            List of inner class information
        """
        inner_classes = []

        # Pattern for inner class: public static class NameDTO
        inner_class_pattern = r'public\s+static\s+class\s+(\w+DTO)'

        for match in re.finditer(inner_class_pattern, content):
            inner_class_name = match.group(1)

            inner_classes.append({
                'name': inner_class_name,
                'type': 'inner_dto'
            })

        return inner_classes
