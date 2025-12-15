"""
Integration test for GWT PRD generation pipeline (T078).

Tests the complete end-to-end flow of GWT artifact analysis:
1. Classification - identifying GWT files
2. Analysis - extracting GWT metadata with specialized analyzers
3. Validation - ensuring GWT metadata is correctly extracted

This test uses the GWT fixtures in tests/fixtures/gwt/ and validates
that the analyzers correctly identify and extract GWT patterns.
"""

import pytest
import tempfile
from pathlib import Path
from typing import Dict, Any, List

from codeindex.services.classifier import FileClassifier
from codeindex.services.gwt_analyzer_registry import GwtAnalyzerRegistry
from codeindex.models import ArtifactType
from codeindex.utils.gwt_patterns import GwtRole


# Fixtures
@pytest.fixture
def gwt_fixtures_dir():
    """Get path to GWT test fixtures."""
    return Path(__file__).parent.parent / "fixtures" / "gwt"


@pytest.fixture
def temp_output_dir():
    """Temporary directory for test outputs."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def classifier():
    """Create file classifier."""
    return FileClassifier()


@pytest.fixture
def gwt_registry():
    """Create GWT analyzer registry."""
    return GwtAnalyzerRegistry()


# Test GWT File Discovery
class TestGwtFileDiscovery:
    """Test discovery of GWT fixture files."""

    def test_find_gwt_fixture_files(self, gwt_fixtures_dir):
        """Test that GWT fixture files exist."""
        # Check for presenter files
        presenter_files = list(gwt_fixtures_dir.glob("*Presenter.java"))
        assert len(presenter_files) >= 2  # FlashAdministrationPresenter, UserListPresenter

        # Check for view files
        view_files = list(gwt_fixtures_dir.glob("*View.java"))
        assert len(view_files) >= 1  # FlashAdministrationView

        # Check for DTO files
        dto_files = list(gwt_fixtures_dir.glob("*DTO.java"))
        assert len(dto_files) >= 2  # FlashInfoDTO, UserDTO

    def test_gwt_file_contents(self, gwt_fixtures_dir):
        """Test that GWT files contain expected patterns."""
        # Check presenter contains GWT patterns
        presenter_path = gwt_fixtures_dir / "FlashAdministrationPresenter.java"
        if presenter_path.exists():
            content = presenter_path.read_text()
            # Should have view reference
            assert 'Display' in content or 'View' in content
            # Should have event handling
            assert 'ClickHandler' in content or 'addClickHandler' in content

        # Check DTO contains serialization
        dto_path = gwt_fixtures_dir / "FlashInfoDTO.java"
        if dto_path.exists():
            content = dto_path.read_text()
            assert 'IsSerializable' in content or 'Serializable' in content
            assert 'serialVersionUID' in content


# Test GWT Classification
class TestGwtClassification:
    """Test classification of GWT files."""

    def test_classify_gwt_fixtures(self, classifier, gwt_fixtures_dir):
        """Test classification of GWT fixture files."""
        # Test presenter
        presenter_path = gwt_fixtures_dir / "FlashAdministrationPresenter.java"
        if presenter_path.exists():
            result = classifier.classify(presenter_path)
            assert result == ArtifactType.JAVA_SOURCE

        # Test view
        view_path = gwt_fixtures_dir / "FlashAdministrationView.java"
        if view_path.exists():
            result = classifier.classify(view_path)
            assert result == ArtifactType.JAVA_SOURCE

        # Test DTO
        dto_path = gwt_fixtures_dir / "FlashInfoDTO.java"
        if dto_path.exists():
            result = classifier.classify(dto_path)
            assert result == ArtifactType.JAVA_SOURCE

    def test_classify_uibinder_xml(self, classifier, gwt_fixtures_dir):
        """Test classification of UiBinder XML if present."""
        ui_xml_files = list(gwt_fixtures_dir.glob("*.ui.xml"))
        for ui_xml in ui_xml_files:
            result = classifier.classify(ui_xml)
            assert result == ArtifactType.GWT_UI_BINDER


# Test GWT Extraction
class TestGwtExtraction:
    """Test extraction of GWT metadata."""

    def test_extract_rpc_servlet(self, gwt_registry, gwt_fixtures_dir, classifier):
        """Test extraction of RPC servlet metadata."""
        servlet_path = gwt_fixtures_dir / "FlashInfoServletImpl.java"
        if not servlet_path.exists():
            pytest.skip("FlashInfoServletImpl.java fixture not found")

        content = servlet_path.read_text(encoding='utf-8')
        artifact_type = classifier.classify(servlet_path)
        analyzer = gwt_registry.get_analyzer(servlet_path, artifact_type)

        if analyzer:
            result = analyzer.analyze(servlet_path, content)
            assert result is not None
            assert result.get('gwt_role') == GwtRole.RPC_SERVLET.value
            assert 'rpc_methods' in result  # Field is 'rpc_methods' not 'service_methods'
            assert 'async_interface' in result

    def test_extract_presenter(self, gwt_registry, gwt_fixtures_dir, classifier):
        """Test extraction of presenter metadata."""
        presenter_path = gwt_fixtures_dir / "FlashAdministrationPresenter.java"
        content = presenter_path.read_text(encoding='utf-8')

        artifact_type = classifier.classify(presenter_path)
        analyzer = gwt_registry.get_analyzer(presenter_path, artifact_type)
        assert analyzer is not None

        result = analyzer.analyze(presenter_path, content)
        assert result is not None
        assert result.get('gwt_role') == GwtRole.PRESENTER.value

        # Check view binding
        assert 'view_binding' in result
        view_binding = result['view_binding']
        assert view_binding is not None
        assert 'view_interface' in view_binding  # Field is 'view_interface' not 'interface_name'
        assert 'confidence' in view_binding

        # Check event handlers
        assert 'event_handlers' in result
        handlers = result['event_handlers']
        assert len(handlers) >= 2  # Should have create and delete handlers

        # Check navigation
        assert 'navigation_logic' in result  # Field is 'navigation_logic' not 'navigation_targets'
        navigation = result['navigation_logic']
        assert len(navigation) >= 1  # Should navigate to edit view

    def test_extract_view(self, gwt_registry, gwt_fixtures_dir, classifier):
        """Test extraction of view metadata."""
        view_path = gwt_fixtures_dir / "FlashAdministrationView.java"
        content = view_path.read_text(encoding='utf-8')

        artifact_type = classifier.classify(view_path)
        analyzer = gwt_registry.get_analyzer(view_path, artifact_type)
        assert analyzer is not None

        result = analyzer.analyze(view_path, content)
        assert result is not None
        assert result.get('gwt_role') == GwtRole.VIEW.value  # Use VIEW not CLIENT_VIEW

        # Check component type
        assert 'component_type' in result
        assert result['component_type'] in ['Composite', 'Widget', 'Panel', 'PopupPanel']

        # Check UiBinder template
        if 'uibinder_template' in result:
            template = result['uibinder_template']
            assert 'template_file' in template

        # Check UI fields
        assert 'ui_fields' in result
        ui_fields = result['ui_fields']
        assert len(ui_fields) >= 2  # Should have dataTable and createButton

    def test_extract_dto(self, gwt_registry, gwt_fixtures_dir, classifier):
        """Test extraction of DTO metadata."""
        dto_path = gwt_fixtures_dir / "FlashInfoDTO.java"
        content = dto_path.read_text(encoding='utf-8')

        # Classify the file first
        artifact_type = classifier.classify(dto_path)

        analyzer = gwt_registry.get_analyzer(dto_path, artifact_type)
        assert analyzer is not None

        result = analyzer.analyze(dto_path, content)
        assert result is not None
        assert result.get('gwt_role') == GwtRole.SHARED_DTO.value

        # Check fields
        assert 'fields' in result
        fields = result['fields']
        assert len(fields) >= 10  # FlashInfoDTO has 11 fields

        # Check field structure
        title_field = next((f for f in fields if f['name'] == 'title'), None)
        assert title_field is not None
        assert title_field['type'] == 'String'
        assert 'validation_rules' in title_field

        # Check validation rules
        rules = title_field['validation_rules']
        assert len(rules) >= 2  # @NotNull and @Size

        # Check serialization
        assert 'gwt_serializable' in result
        assert 'java_serializable' in result
        assert 'has_default_constructor' in result
        assert result['gwt_serializable'] is True
        assert result['java_serializable'] is True
        assert result['has_default_constructor'] is True

    def test_extract_nested_dto(self, gwt_registry, gwt_fixtures_dir, classifier):
        """Test extraction of DTO with nested references."""
        dto_path = gwt_fixtures_dir / "UserDTO.java"
        content = dto_path.read_text(encoding='utf-8')

        artifact_type = classifier.classify(dto_path)
        analyzer = gwt_registry.get_analyzer(dto_path, artifact_type)
        assert analyzer is not None

        result = analyzer.analyze(dto_path, content)
        assert result is not None

        # Check nested DTOs
        assert 'nested_dtos' in result
        nested = result['nested_dtos']
        assert len(nested) >= 4  # UserProfileDTO, AddressDTO, PermissionDTO, ProjectDTO

        nested_names = [n['name'] for n in nested]
        assert 'UserProfileDTO' in nested_names
        assert 'AddressDTO' in nested_names
        assert 'PermissionDTO' in nested_names
        assert 'ProjectDTO' in nested_names

        # Check inner classes
        assert 'inner_classes' in result
        inner_classes = result['inner_classes']
        assert len(inner_classes) >= 4


# Test Full Pipeline Integration
class TestGwtPipelineIntegration:
    """Test complete GWT pipeline integration."""

    def test_analyze_all_gwt_fixtures(
        self,
        gwt_registry,
        gwt_fixtures_dir,
        classifier
    ):
        """Test analyzing all GWT fixture files."""
        # Find all Java files
        java_files = list(gwt_fixtures_dir.glob("*.java"))
        assert len(java_files) > 0

        # Analyze each file
        gwt_artifacts = []
        for java_file in java_files:
            try:
                content = java_file.read_text(encoding='utf-8')
                artifact_type = classifier.classify(java_file)
                analyzer = gwt_registry.get_analyzer(java_file, artifact_type)

                if analyzer:
                    result = analyzer.analyze(java_file, content)
                    if result and 'gwt_role' in result:
                        gwt_artifacts.append({
                            'file_path': str(java_file),
                            'gwt_role': result['gwt_role'],
                            'metadata': result
                        })
            except Exception as e:
                # Log but don't fail on individual file errors
                print(f"Error analyzing {java_file}: {e}")

        # Validate extraction results
        assert len(gwt_artifacts) >= 4  # At least 4 GWT artifacts

        # Check that we have different GWT roles
        roles = set(a['gwt_role'] for a in gwt_artifacts)
        assert len(roles) >= 2  # At least presenters and DTOs

        # Check that presenter has view binding
        presenters = [a for a in gwt_artifacts if a['gwt_role'] == GwtRole.PRESENTER.value]
        assert len(presenters) >= 1
        assert 'view_binding' in presenters[0]['metadata']

        # Check that DTO has fields
        dtos = [a for a in gwt_artifacts if a['gwt_role'] == GwtRole.SHARED_DTO.value]
        assert len(dtos) >= 1
        assert 'fields' in dtos[0]['metadata']
        assert len(dtos[0]['metadata']['fields']) >= 5

    def test_presenter_analysis_structure(
        self,
        gwt_registry,
        gwt_fixtures_dir,
        classifier
    ):
        """Test that presenter analysis follows expected structure."""
        # Analyze presenter
        presenter_path = gwt_fixtures_dir / "FlashAdministrationPresenter.java"
        content = presenter_path.read_text(encoding='utf-8')
        artifact_type = classifier.classify(presenter_path)
        analyzer = gwt_registry.get_analyzer(presenter_path, artifact_type)
        result = analyzer.analyze(presenter_path, content)

        # Validate result structure
        assert isinstance(result, dict)
        assert 'gwt_role' in result
        assert 'view_binding' in result
        assert 'event_handlers' in result
        assert 'navigation_logic' in result  # Field is 'navigation_logic' not 'navigation_targets'
        assert 'rpc_calls' in result

        # Validate view binding structure
        view_binding = result['view_binding']
        assert 'view_interface' in view_binding  # Field is 'view_interface' not 'interface_name'
        assert 'confidence' in view_binding
        assert isinstance(view_binding['confidence'], (int, float))
        assert 0 <= view_binding['confidence'] <= 100

        # Validate event handlers structure
        handlers = result['event_handlers']
        assert isinstance(handlers, list)
        if handlers:
            handler = handlers[0]
            # Check for actual field names in handler structure
            assert 'widget_getter' in handler or 'widget' in handler
            assert 'handler_type' in handler or 'event_type' in handler
            assert 'action_method' in handler or 'handler_method' in handler


# Test Error Handling
class TestGwtErrorHandling:
    """Test error handling in GWT extraction."""

    def test_analyze_invalid_java_file(self, gwt_registry, temp_output_dir):
        """Test handling of invalid Java file."""
        invalid_file = temp_output_dir / "Invalid.java"
        invalid_file.write_text("this is not valid java code { } ( )")

        analyzer = gwt_registry.get_analyzer(invalid_file, invalid_file.read_text())

        # Should either return None (no analyzer) or handle gracefully
        if analyzer:
            result = analyzer.analyze(invalid_file, invalid_file.read_text())
            # Result might be empty or contain error info
            assert result is not None

    def test_analyze_non_gwt_java_file(self, gwt_registry, temp_output_dir):
        """Test handling of regular Java file without GWT patterns."""
        regular_file = temp_output_dir / "RegularClass.java"
        regular_file.write_text("""
        package com.example;

        public class RegularClass {
            private String name;

            public String getName() {
                return name;
            }
        }
        """)

        analyzer = gwt_registry.get_analyzer(regular_file, regular_file.read_text())

        # Should return None - no GWT patterns detected
        assert analyzer is None
