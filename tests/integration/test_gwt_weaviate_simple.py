"""
Simplified integration test for GWT metadata with Weaviate (T080).

Tests that GWT-specific metadata is correctly structured and
compatible with the Weaviate schema.

This test focuses on metadata structure validation rather than
full Weaviate operations, which are tested through CLI commands.
"""

import pytest
import json
from pathlib import Path

from codeindex.services.classifier import FileClassifier
from codeindex.services.gwt_analyzer_registry import GwtAnalyzerRegistry
from codeindex.utils.gwt_patterns import GwtRole


@pytest.fixture
def gwt_fixtures_dir():
    """Get path to GWT test fixtures."""
    return Path(__file__).parent.parent / "fixtures" / "gwt"


@pytest.fixture
def classifier():
    """File classifier instance."""
    return FileClassifier()


@pytest.fixture
def gwt_registry():
    """GWT analyzer registry."""
    return GwtAnalyzerRegistry()


class TestGwtMetadataStructure:
    """Test GWT metadata structure for Weaviate compatibility."""

    def test_presenter_metadata_structure(self, gwt_fixtures_dir, classifier, gwt_registry):
        """Test presenter metadata has correct structure."""
        presenter_path = gwt_fixtures_dir / "FlashAdministrationPresenter.java"
        if not presenter_path.exists():
            pytest.skip("Presenter fixture not found")

        content = presenter_path.read_text(encoding='utf-8')
        artifact_type = classifier.classify(presenter_path)
        analyzer = gwt_registry.get_analyzer(presenter_path, artifact_type)

        assert analyzer is not None, "No analyzer found for presenter"

        metadata = analyzer.analyze(presenter_path, content)
        assert metadata is not None
        assert 'gwt_role' in metadata
        assert metadata['gwt_role'] == GwtRole.PRESENTER.value

        # Verify presenter-specific fields
        assert 'view_binding' in metadata
        assert 'event_handlers' in metadata
        assert 'navigation_logic' in metadata
        assert 'rpc_calls' in metadata

        # Verify metadata is JSON-serializable (required for Weaviate)
        json_str = json.dumps(metadata)
        assert len(json_str) > 0

        # Verify can be deserialized
        reconstructed = json.loads(json_str)
        assert reconstructed['gwt_role'] == GwtRole.PRESENTER.value

    def test_dto_metadata_structure(self, gwt_fixtures_dir, classifier, gwt_registry):
        """Test DTO metadata has correct structure."""
        dto_path = gwt_fixtures_dir / "FlashInfoDTO.java"
        if not dto_path.exists():
            pytest.skip("DTO fixture not found")

        content = dto_path.read_text(encoding='utf-8')
        artifact_type = classifier.classify(dto_path)
        analyzer = gwt_registry.get_analyzer(dto_path, artifact_type)

        assert analyzer is not None, "No analyzer found for DTO"

        metadata = analyzer.analyze(dto_path, content)
        assert metadata is not None
        assert 'gwt_role' in metadata
        assert metadata['gwt_role'] == GwtRole.SHARED_DTO.value

        # Verify DTO-specific fields
        assert 'fields' in metadata
        assert len(metadata['fields']) >= 10
        assert 'gwt_serializable' in metadata
        assert 'java_serializable' in metadata
        assert 'has_default_constructor' in metadata

        # Verify metadata is JSON-serializable
        json_str = json.dumps(metadata)
        assert len(json_str) > 0

        # Verify can be deserialized
        reconstructed = json.loads(json_str)
        assert reconstructed['gwt_role'] == GwtRole.SHARED_DTO.value
        assert len(reconstructed['fields']) >= 10

    def test_view_metadata_structure(self, gwt_fixtures_dir, classifier, gwt_registry):
        """Test view metadata has correct structure."""
        view_path = gwt_fixtures_dir / "FlashAdministrationView.java"
        if not view_path.exists():
            pytest.skip("View fixture not found")

        content = view_path.read_text(encoding='utf-8')
        artifact_type = classifier.classify(view_path)
        analyzer = gwt_registry.get_analyzer(view_path, artifact_type)

        assert analyzer is not None, "No analyzer found for view"

        metadata = analyzer.analyze(view_path, content)
        assert metadata is not None
        assert 'gwt_role' in metadata
        assert metadata['gwt_role'] == GwtRole.VIEW.value

        # Verify view-specific fields
        assert 'component_type' in metadata
        assert 'ui_fields' in metadata

        # Verify metadata is JSON-serializable
        json_str = json.dumps(metadata)
        assert len(json_str) > 0

    def test_rpc_servlet_metadata_structure(self, gwt_fixtures_dir, classifier, gwt_registry):
        """Test RPC servlet metadata has correct structure."""
        servlet_path = gwt_fixtures_dir / "FlashInfoServletImpl.java"
        if not servlet_path.exists():
            pytest.skip("Servlet fixture not found")

        content = servlet_path.read_text(encoding='utf-8')
        artifact_type = classifier.classify(servlet_path)
        analyzer = gwt_registry.get_analyzer(servlet_path, artifact_type)

        assert analyzer is not None, "No analyzer found for servlet"

        metadata = analyzer.analyze(servlet_path, content)
        assert metadata is not None
        assert 'gwt_role' in metadata
        assert metadata['gwt_role'] == GwtRole.RPC_SERVLET.value

        # Verify servlet-specific fields
        assert 'rpc_methods' in metadata
        assert len(metadata['rpc_methods']) >= 5
        assert 'service_interface' in metadata

        # Verify metadata is JSON-serializable
        json_str = json.dumps(metadata)
        assert len(json_str) > 0


class TestGwtMetadataCompatibility:
    """Test GWT metadata compatibility with indexing pipeline."""

    def test_all_gwt_roles_have_metadata(self, gwt_fixtures_dir, classifier, gwt_registry):
        """Test that all GWT roles can generate metadata."""
        test_files = [
            ("FlashAdministrationPresenter.java", GwtRole.PRESENTER),
            ("FlashInfoDTO.java", GwtRole.SHARED_DTO),
            ("FlashAdministrationView.java", GwtRole.VIEW),
            ("FlashInfoServletImpl.java", GwtRole.RPC_SERVLET),
        ]

        for file_name, expected_role in test_files:
            file_path = gwt_fixtures_dir / file_name
            if not file_path.exists():
                continue

            content = file_path.read_text(encoding='utf-8')
            artifact_type = classifier.classify(file_path)
            analyzer = gwt_registry.get_analyzer(file_path, artifact_type)

            assert analyzer is not None, f"No analyzer for {file_name}"

            metadata = analyzer.analyze(file_path, content)
            assert metadata is not None, f"No metadata for {file_name}"
            assert metadata['gwt_role'] == expected_role.value, \
                f"Wrong role for {file_name}: {metadata['gwt_role']}"

            # Verify JSON serializability
            json_str = json.dumps(metadata)
            assert len(json_str) > 0, f"Empty JSON for {file_name}"

    def test_nested_dto_metadata_serializable(self, gwt_fixtures_dir, classifier, gwt_registry):
        """Test that complex nested DTO metadata can be serialized."""
        dto_path = gwt_fixtures_dir / "UserDTO.java"
        if not dto_path.exists():
            pytest.skip("UserDTO fixture not found")

        content = dto_path.read_text(encoding='utf-8')
        artifact_type = classifier.classify(dto_path)
        analyzer = gwt_registry.get_analyzer(dto_path, artifact_type)

        if analyzer:
            metadata = analyzer.analyze(dto_path, content)
            assert metadata is not None

            # UserDTO has nested DTOs and inner classes
            assert 'nested_dtos' in metadata
            assert 'inner_classes' in metadata

            # Verify the complex structure is JSON-serializable
            json_str = json.dumps(metadata)
            assert len(json_str) > 0

            # Verify can be reconstructed
            reconstructed = json.loads(json_str)
            assert 'nested_dtos' in reconstructed
            assert 'inner_classes' in reconstructed
            assert len(reconstructed['nested_dtos']) >= 4
            assert len(reconstructed['inner_classes']) >= 4
