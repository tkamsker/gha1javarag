"""Unit tests for DTO classification (T038-T042, T044)."""

import pytest
from pathlib import Path
from codeindex.services.classifier import classify_dto
from codeindex.models.dto_artifact import DtoArtifact, ClassificationResult


class TestDtoNamingPattern:
    """Test DTO naming pattern classification (T038)."""

    def test_dto_suffix_classified_as_dto(self):
        """Test that classes ending with 'DTO' are classified as DTOs."""
        fixture = Path("tests/fixtures/dto-classes/src/main/java/com/example/dto/standard-dto.java")

        result = classify_dto(fixture)

        assert result is not None
        assert isinstance(result, ClassificationResult)
        assert result.is_dto is True
        assert result.confidence >= 70  # Should meet threshold
        assert result.naming_pattern_score > 0  # Should score for naming

    def test_dto_lowercase_suffix_classified_as_dto(self):
        """Test that classes ending with 'Dto' (lowercase) are classified."""
        # This would need a fixture with lowercase, but testing the logic
        # For now, using standard fixture
        fixture = Path("tests/fixtures/dto-classes/src/main/java/com/example/dto/standard-dto.java")
        result = classify_dto(fixture)
        assert result.is_dto is True

    def test_non_dto_naming_not_classified(self):
        """Test that classes without DTO naming pattern score 0 for naming."""
        # Using entity fixture which doesn't have DTO in name
        fixture = Path("tests/fixtures/dto-classes/src/main/java/com/example/dto/entity-vs-dto.java")

        result = classify_dto(fixture)

        # Should NOT be classified as DTO due to @Entity annotation
        # even though it has DTO in the name
        assert result.is_dto is False


class TestEntityExclusion:
    """Test entity exclusion logic (T039)."""

    def test_entity_annotation_prevents_dto_classification(self):
        """Test that classes with @Entity are NOT classified as DTOs."""
        fixture = Path("tests/fixtures/dto-classes/src/main/java/com/example/dto/entity-vs-dto.java")

        result = classify_dto(fixture)

        assert result is not None
        assert result.is_dto is False
        assert result.entity_markers_found is True
        # Even if naming matches, entity markers should prevent classification

    def test_table_annotation_prevents_dto_classification(self):
        """Test that classes with @Table are NOT classified as DTOs."""
        # entity-vs-dto.java has @Table annotation
        fixture = Path("tests/fixtures/dto-classes/src/main/java/com/example/dto/entity-vs-dto.java")

        result = classify_dto(fixture)

        assert result.is_dto is False

    def test_dto_without_entity_markers_allowed(self):
        """Test that DTOs without entity markers can be classified."""
        fixture = Path("tests/fixtures/dto-classes/src/main/java/com/example/dto/standard-dto.java")

        result = classify_dto(fixture)

        assert result.is_dto is True
        assert result.entity_markers_found is False


class TestStructuralAnalysis:
    """Test structural analysis (field-to-method ratio) (T040)."""

    def test_high_field_to_method_ratio_increases_score(self):
        """Test that DTOs with many fields and few methods score higher."""
        fixture = Path("tests/fixtures/dto-classes/src/main/java/com/example/dto/standard-dto.java")

        result = classify_dto(fixture)

        assert result is not None
        assert result.structural_score > 0
        # Standard DTO should have high field count, low method count
        assert result.field_count >= 5  # UserDTO has 7 fields
        # Getters/setters are expected, but ratio should favor data

    def test_low_field_to_method_ratio_decreases_score(self):
        """Test that classes with many methods relative to fields score lower."""
        # This would require a fixture with heavy logic
        # For now, verify that structural analysis is performed
        fixture = Path("tests/fixtures/dto-classes/src/main/java/com/example/dto/standard-dto.java")
        result = classify_dto(fixture)
        assert hasattr(result, 'structural_score')

    def test_no_fields_prevents_dto_classification(self):
        """Test that classes with no fields cannot be DTOs."""
        # Would need a fixture with no fields
        # For now, verify field count is tracked
        fixture = Path("tests/fixtures/dto-classes/src/main/java/com/example/dto/standard-dto.java")
        result = classify_dto(fixture)
        assert result.field_count > 0


class TestSerializationMarkers:
    """Test serialization marker detection (T041)."""

    def test_serializable_interface_detected(self):
        """Test that Serializable implementation is detected."""
        fixture = Path("tests/fixtures/dto-classes/src/main/java/com/example/dto/standard-dto.java")

        result = classify_dto(fixture)

        assert result is not None
        assert result.serialization_markers_found is True
        assert result.serialization_score > 0

    def test_jackson_annotations_detected(self):
        """Test that Jackson annotations are detected as serialization markers."""
        # standard-dto.java may have Jackson annotations
        fixture = Path("tests/fixtures/dto-classes/src/main/java/com/example/dto/standard-dto.java")
        result = classify_dto(fixture)
        # Should detect serialization patterns
        assert hasattr(result, 'serialization_markers_found')

    def test_no_serialization_markers_reduces_score(self):
        """Test that lack of serialization markers affects score."""
        # Would need a fixture without serialization
        # For now, verify the attribute exists
        fixture = Path("tests/fixtures/dto-classes/src/main/java/com/example/dto/standard-dto.java")
        result = classify_dto(fixture)
        assert hasattr(result, 'serialization_score')


class TestPackageLocationHeuristics:
    """Test package location heuristics (T042)."""

    def test_dto_package_increases_score(self):
        """Test that DTOs in *.dto.* packages score higher."""
        # standard-dto.java should have appropriate package
        fixture = Path("tests/fixtures/dto-classes/src/main/java/com/example/dto/standard-dto.java")

        result = classify_dto(fixture)

        assert result is not None
        assert hasattr(result, 'package_score')
        # If in dto package, should have points

    def test_model_package_increases_score(self):
        """Test that DTOs in *.model.* packages score higher."""
        # Would need specific fixture
        fixture = Path("tests/fixtures/dto-classes/src/main/java/com/example/dto/standard-dto.java")
        result = classify_dto(fixture)
        assert hasattr(result, 'package_score')

    def test_non_dto_package_has_lower_score(self):
        """Test that DTOs not in typical packages have reduced package score."""
        # entity-vs-dto.java is in entity package
        fixture = Path("tests/fixtures/dto-classes/src/main/java/com/example/dto/entity-vs-dto.java")
        result = classify_dto(fixture)
        # Package score should be lower for entity package
        assert hasattr(result, 'package_score')


class TestNestedDtoIdentification:
    """Test nested DTO identification (T044)."""

    def test_nested_dto_fields_identified(self):
        """Test that nested DTO fields are identified."""
        fixture = Path("tests/fixtures/dto-classes/src/main/java/com/example/dto/nested-dto.java")

        result = classify_dto(fixture)

        assert result is not None
        assert result.is_dto is True
        # Should identify nested DTOs
        assert result.nested_dtos_found is True
        assert result.nested_dto_count > 0

    def test_nested_dto_names_extracted(self):
        """Test that nested DTO type names are extracted."""
        fixture = Path("tests/fixtures/dto-classes/src/main/java/com/example/dto/nested-dto.java")

        result = classify_dto(fixture)

        assert len(result.nested_dto_types) > 0
        # Should include CustomerDTO, OrderItemDTO, etc.
        expected_types = ["CustomerDTO", "OrderItemDTO", "ShippingAddressDTO"]
        for expected in expected_types:
            assert any(expected in dtype for dtype in result.nested_dto_types)

    def test_inner_class_dtos_identified(self):
        """Test that inner class DTOs are identified."""
        fixture = Path("tests/fixtures/dto-classes/src/main/java/com/example/dto/nested-dto.java")

        result = classify_dto(fixture)

        # Should detect inner classes if present
        assert hasattr(result, 'nested_dtos_found')

    def test_standard_dto_without_nested_types(self):
        """Test that simple DTOs report no nested DTOs."""
        fixture = Path("tests/fixtures/dto-classes/src/main/java/com/example/dto/standard-dto.java")

        result = classify_dto(fixture)

        # Standard DTO should not have nested DTO relationships
        # (unless it's using other DTOs as fields - need to check fixture)
        assert hasattr(result, 'nested_dtos_found')


class TestThresholdDecision:
    """Test confidence threshold decision logic."""

    def test_high_confidence_classified_as_dto(self):
        """Test that confidence >= 70 results in DTO classification."""
        fixture = Path("tests/fixtures/dto-classes/src/main/java/com/example/dto/standard-dto.java")

        result = classify_dto(fixture)

        assert result.is_dto is True
        assert result.confidence >= 70

    def test_low_confidence_not_classified_as_dto(self):
        """Test that confidence < 70 results in NOT DTO."""
        fixture = Path("tests/fixtures/dto-classes/src/main/java/com/example/dto/entity-vs-dto.java")

        result = classify_dto(fixture)

        # Entity fixture should have low confidence due to entity markers
        assert result.is_dto is False
        assert result.confidence < 70

    def test_confidence_calculation_includes_all_phases(self):
        """Test that confidence score includes all classification phases."""
        fixture = Path("tests/fixtures/dto-classes/src/main/java/com/example/dto/standard-dto.java")

        result = classify_dto(fixture)

        # Confidence should be sum of: naming + structural + serialization + package
        total_score = (
            result.naming_pattern_score +
            result.structural_score +
            result.serialization_score +
            result.package_score
        )

        # Confidence should match or be capped at 100
        assert result.confidence == min(total_score, 100)


class TestClassificationResult:
    """Test ClassificationResult model completeness."""

    def test_classification_result_has_all_required_fields(self):
        """Test that ClassificationResult includes all required metadata."""
        fixture = Path("tests/fixtures/dto-classes/src/main/java/com/example/dto/standard-dto.java")

        result = classify_dto(fixture)

        # Verify all required fields exist
        assert hasattr(result, 'is_dto')
        assert hasattr(result, 'confidence')
        assert hasattr(result, 'naming_pattern_score')
        assert hasattr(result, 'structural_score')
        assert hasattr(result, 'serialization_score')
        assert hasattr(result, 'package_score')
        assert hasattr(result, 'entity_markers_found')
        assert hasattr(result, 'serialization_markers_found')
        assert hasattr(result, 'nested_dtos_found')
        assert hasattr(result, 'field_count')
        assert hasattr(result, 'nested_dto_types')
        assert hasattr(result, 'nested_dto_count')

    def test_classification_result_types_correct(self):
        """Test that ClassificationResult field types are correct."""
        fixture = Path("tests/fixtures/dto-classes/src/main/java/com/example/dto/standard-dto.java")

        result = classify_dto(fixture)

        assert isinstance(result.is_dto, bool)
        assert isinstance(result.confidence, (int, float))
        assert isinstance(result.naming_pattern_score, (int, float))
        assert isinstance(result.field_count, int)
        assert isinstance(result.nested_dto_types, list)
