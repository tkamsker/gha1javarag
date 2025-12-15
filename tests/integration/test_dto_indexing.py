"""Integration tests for DTO indexing in Weaviate (T045)."""

import pytest
from pathlib import Path
from src.codeindex.services.indexing import IndexingService
from src.codeindex.services.classifier import classify_dto
from src.codeindex.models.dto_artifact import DtoArtifact
from src.codeindex.utils.config import Config


class TestDtoIndexing:
    """Integration tests for DTO artifact indexing in Weaviate."""

    @pytest.fixture
    def indexing_service(self):
        """Create indexing service instance."""
        config = Config()
        return IndexingService(config=config)

    def test_dto_artifact_can_be_indexed(self, indexing_service):
        """Test that DtoArtifact can be successfully indexed to Weaviate (T045)."""
        # Arrange
        fixture_path = Path("tests/fixtures/dto-classes/standard-dto.java")

        # Classify the DTO
        classification_result = classify_dto(fixture_path)

        # Create DtoArtifact from classification result
        dto_artifact = DtoArtifact.from_classification(
            file_path=fixture_path,
            classification=classification_result
        )

        # Act
        artifact_id = indexing_service.index_dto(dto_artifact)

        # Assert
        assert artifact_id is not None
        assert isinstance(artifact_id, str)
        assert len(artifact_id) > 0

    def test_dto_artifact_retrieval_from_weaviate(self, indexing_service):
        """Test that indexed DTO can be retrieved from Weaviate."""
        # Arrange
        fixture_path = Path("tests/fixtures/dto-classes/standard-dto.java")
        classification_result = classify_dto(fixture_path)
        dto_artifact = DtoArtifact.from_classification(
            file_path=fixture_path,
            classification=classification_result
        )

        # Index the DTO
        artifact_id = indexing_service.index_dto(dto_artifact)

        # Act
        retrieved = indexing_service.get_dto_by_id(artifact_id)

        # Assert
        assert retrieved is not None
        assert retrieved['artifact_id'] == artifact_id
        assert retrieved['class_name'] == dto_artifact.class_name
        assert retrieved['is_dto'] is True

    def test_dto_search_by_class_name(self, indexing_service):
        """Test searching for DTOs by class name."""
        # Arrange
        fixture_path = Path("tests/fixtures/dto-classes/standard-dto.java")
        classification_result = classify_dto(fixture_path)
        dto_artifact = DtoArtifact.from_classification(
            file_path=fixture_path,
            classification=classification_result
        )

        # Index the DTO
        indexing_service.index_dto(dto_artifact)

        # Act
        results = indexing_service.search_dtos(
            query=dto_artifact.class_name,
            limit=10
        )

        # Assert
        assert len(results) > 0
        assert any(r['class_name'] == dto_artifact.class_name for r in results)

    def test_dto_field_metadata_preserved(self, indexing_service):
        """Test that DTO field metadata is preserved in Weaviate."""
        # Arrange
        fixture_path = Path("tests/fixtures/dto-classes/standard-dto.java")
        classification_result = classify_dto(fixture_path)
        dto_artifact = DtoArtifact.from_classification(
            file_path=fixture_path,
            classification=classification_result
        )

        # Index the DTO
        artifact_id = indexing_service.index_dto(dto_artifact)

        # Act
        retrieved = indexing_service.get_dto_by_id(artifact_id)

        # Assert
        assert 'fields' in retrieved
        assert len(retrieved['fields']) > 0

        # Check that field details are preserved
        for field in retrieved['fields']:
            assert 'name' in field
            assert 'field_type' in field
            # Validation annotations should be preserved if present
            if 'validation_annotations' in field:
                assert isinstance(field['validation_annotations'], list)

    def test_dto_validation_annotations_indexed(self, indexing_service):
        """Test that validation annotations are indexed with DTOs."""
        # Arrange
        fixture_path = Path("tests/fixtures/dto-classes/standard-dto.java")
        classification_result = classify_dto(fixture_path)
        dto_artifact = DtoArtifact.from_classification(
            file_path=fixture_path,
            classification=classification_result
        )

        # Index the DTO
        artifact_id = indexing_service.index_dto(dto_artifact)

        # Act
        retrieved = indexing_service.get_dto_by_id(artifact_id)

        # Assert
        if dto_artifact.has_validation_annotations:
            assert 'validation_rules' in retrieved
            validation_rules = retrieved['validation_rules']
            assert validation_rules is not None

    def test_nested_dto_relationships_indexed(self, indexing_service):
        """Test that nested DTO relationships are indexed."""
        # Arrange
        fixture_path = Path("tests/fixtures/dto-classes/nested-dto.java")
        classification_result = classify_dto(fixture_path)
        dto_artifact = DtoArtifact.from_classification(
            file_path=fixture_path,
            classification=classification_result
        )

        # Index the DTO
        artifact_id = indexing_service.index_dto(dto_artifact)

        # Act
        retrieved = indexing_service.get_dto_by_id(artifact_id)

        # Assert
        if dto_artifact.nested_dto_types:
            assert 'nested_dto_types' in retrieved
            nested_types = retrieved['nested_dto_types']
            assert len(nested_types) > 0

    def test_multiple_dtos_can_be_indexed(self, indexing_service):
        """Test that multiple DTOs can be indexed without conflicts."""
        # Arrange
        fixtures = [
            Path("tests/fixtures/dto-classes/standard-dto.java"),
            Path("tests/fixtures/dto-classes/nested-dto.java")
        ]

        artifact_ids = []

        # Act
        for fixture_path in fixtures:
            classification_result = classify_dto(fixture_path)
            dto_artifact = DtoArtifact.from_classification(
                file_path=fixture_path,
                classification=classification_result
            )
            artifact_id = indexing_service.index_dto(dto_artifact)
            artifact_ids.append(artifact_id)

        # Assert
        assert len(artifact_ids) == len(fixtures)
        # All IDs should be unique
        assert len(set(artifact_ids)) == len(artifact_ids)

        # All should be retrievable
        for artifact_id in artifact_ids:
            retrieved = indexing_service.get_dto_by_id(artifact_id)
            assert retrieved is not None

    def test_dto_update_replaces_existing(self, indexing_service):
        """Test that re-indexing a DTO updates the existing entry."""
        # Arrange
        fixture_path = Path("tests/fixtures/dto-classes/standard-dto.java")
        classification_result = classify_dto(fixture_path)
        dto_artifact = DtoArtifact.from_classification(
            file_path=fixture_path,
            classification=classification_result
        )

        # Index first time
        artifact_id_1 = indexing_service.index_dto(dto_artifact)

        # Act - Index again (simulating re-indexing)
        artifact_id_2 = indexing_service.index_dto(dto_artifact)

        # Assert
        # Should return same ID (idempotent) or new ID that replaces old
        # Check only one entry exists for this class
        results = indexing_service.search_dtos(
            query=dto_artifact.class_name,
            limit=10
        )

        matching_results = [r for r in results if r['class_name'] == dto_artifact.class_name]
        # Should have exactly 1 result (not duplicated)
        assert len(matching_results) == 1

    def test_dto_indexing_with_project_filtering(self, indexing_service):
        """Test that DTOs can be filtered by project when indexing."""
        # Arrange
        fixture_path = Path("tests/fixtures/dto-classes/standard-dto.java")
        classification_result = classify_dto(fixture_path)
        dto_artifact = DtoArtifact.from_classification(
            file_path=fixture_path,
            classification=classification_result,
            project_name="test-project"
        )

        # Act
        artifact_id = indexing_service.index_dto(dto_artifact, project="test-project")

        # Assert
        retrieved = indexing_service.get_dto_by_id(artifact_id)
        assert retrieved['project'] == "test-project"

        # Search with project filter
        results = indexing_service.search_dtos(
            query=dto_artifact.class_name,
            project="test-project",
            limit=10
        )

        assert len(results) > 0
        assert all(r['project'] == "test-project" for r in results)
