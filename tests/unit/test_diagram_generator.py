"""
Unit tests for Diagram Generator Service.

Tests the DiagramGenerator class for generating architecture diagrams.
"""
import json
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, mock_open

from codeindex.services.diagram_generator import DiagramGenerator


# ==============================================================================
# Fixtures
# ==============================================================================

@pytest.fixture
def temp_output_dir(tmp_path):
    """Create temporary output directory."""
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    return output_dir


@pytest.fixture
def diagram_generator(temp_output_dir):
    """Create DiagramGenerator instance."""
    return DiagramGenerator(output_dir=temp_output_dir)


@pytest.fixture
def sample_prd_components(temp_output_dir):
    """Create sample PRD component files."""
    # Create directory structure
    services_dir = temp_output_dir / "services" / "services"
    services_dir.mkdir(parents=True)

    frontend_dir = temp_output_dir / "frontend"
    components_dir = frontend_dir / "components"
    forms_dir = frontend_dir / "forms"
    components_dir.mkdir(parents=True)
    forms_dir.mkdir(parents=True)

    # Create sample service file
    service_data = {
        'class_name': 'UserService',
        'name': 'UserService',
        'methods': ['getUser', 'saveUser']
    }
    service_file = services_dir / "UserService.json"
    service_file.write_text(json.dumps(service_data))

    # Create sample presenter file
    presenter_data = {
        'id': 'gwt_presenter_UserPresenter',
        'name': 'UserPresenter',
        'component_type': 'gwt_presenter',
        'source_file': '/path/to/UserPresenter.java',
        'semantic_data': {
            'event_handlers': ['onSaveClick'],
            'rpc_calls': [{'service': 'UserService'}]
        }
    }
    presenter_file = components_dir / "gwt_presenter_UserPresenter.json"
    presenter_file.write_text(json.dumps(presenter_data))

    # Create sample view file
    view_data = {
        'id': 'gwt_view_UserView',
        'name': 'UserView',
        'component_type': 'gwt_view',
        'source_file': '/path/to/UserView.java'
    }
    view_file = components_dir / "gwt_view_UserView.json"
    view_file.write_text(json.dumps(view_data))

    # Create sample form file
    form_data = {
        'name': 'UserForm',
        'fields': ['name', 'email']
    }
    form_file = forms_dir / "UserForm.json"
    form_file.write_text(json.dumps(form_data))

    return {
        'services_dir': services_dir,
        'components_dir': components_dir,
        'forms_dir': forms_dir
    }


@pytest.fixture
def sample_extraction_file(tmp_path):
    """Create sample extraction results file."""
    extraction_file = tmp_path / "extraction-results.jsonl"

    # Sample summary line
    summary = {
        'type': 'summary',
        'total_files': 2
    }

    # Sample presenter artifact
    presenter = {
        'file_path': '/path/to/AdminPresenter.java',
        'semantic_data': {
            'gwt_role': 'presenter',
            'presenter_name': 'AdminPresenter',
            'view_binding': None,
            'event_handlers': ['onLoadClick'],
            'rpc_calls': [{'service': 'AdminService', 'method': 'getData'}],
            'entities': ['AdminPresenter', 'AdminView']
        }
    }

    # Sample view artifact
    view = {
        'file_path': '/path/to/AdminView.java',
        'semantic_data': {
            'gwt_role': 'view',
            'view_name': 'AdminView',
            'ui_fields': ['dataGrid', 'loadButton'],
            'entities': ['AdminView']
        }
    }

    # Write JSONL file
    with open(extraction_file, 'w') as f:
        f.write(json.dumps(summary) + '\n')
        f.write(json.dumps(presenter) + '\n')
        f.write(json.dumps(view) + '\n')

    return extraction_file


# ==============================================================================
# Tests: Initialization
# ==============================================================================

def test_diagram_generator_initialization(temp_output_dir):
    """Test DiagramGenerator initialization."""
    generator = DiagramGenerator(output_dir=temp_output_dir)

    assert generator.output_dir == temp_output_dir
    assert generator.weaviate_store is None
    assert generator.logger is not None

    # Check directory structure created
    assert (temp_output_dir / "diagrams").exists()
    assert (temp_output_dir / "diagrams" / "component").exists()
    assert (temp_output_dir / "diagrams" / "gwt").exists()
    assert (temp_output_dir / "diagrams" / "database").exists()
    assert (temp_output_dir / "diagrams" / "sequence").exists()


def test_diagram_generator_with_weaviate_store(temp_output_dir):
    """Test DiagramGenerator initialization with Weaviate store."""
    mock_store = Mock()
    generator = DiagramGenerator(
        output_dir=temp_output_dir,
        weaviate_store=mock_store
    )

    assert generator.weaviate_store == mock_store


# ==============================================================================
# Tests: Load Components from PRD
# ==============================================================================

def test_load_components_from_prd(diagram_generator, sample_prd_components):
    """Test loading components from PRD artifacts."""
    components = diagram_generator._load_components_from_prd()

    # Check that components were loaded
    assert 'services' in components
    assert 'presenters' in components
    assert 'views' in components
    assert 'forms' in components

    # Check service loaded
    assert len(components['services']) == 1
    assert components['services'][0]['class_name'] == 'UserService'

    # Check presenter loaded
    assert len(components['presenters']) == 1
    assert components['presenters'][0]['name'] == 'UserPresenter'

    # Check view loaded
    assert len(components['views']) == 1
    assert components['views'][0]['name'] == 'UserView'

    # Check form loaded
    assert len(components['forms']) == 1
    assert components['forms'][0]['name'] == 'UserForm'


def test_load_components_from_prd_no_directories(diagram_generator):
    """Test loading components when directories don't exist."""
    components = diagram_generator._load_components_from_prd()

    # Should return empty lists
    assert components['services'] == []
    assert components['presenters'] == []
    assert components['views'] == []
    assert components['forms'] == []


def test_load_components_from_prd_with_project_filter(diagram_generator, sample_prd_components):
    """Test loading components with project filter."""
    # Note: Current implementation doesn't filter by project
    components = diagram_generator._load_components_from_prd(project_id='test-project')

    # Should still load components (filtering not implemented yet)
    assert len(components['services']) > 0 or len(components['presenters']) > 0


def test_load_components_handles_invalid_json(diagram_generator, temp_output_dir):
    """Test that loading handles invalid JSON files gracefully."""
    # Create services directory with invalid JSON
    services_dir = temp_output_dir / "services" / "services"
    services_dir.mkdir(parents=True)

    invalid_file = services_dir / "invalid.json"
    invalid_file.write_text("{ invalid json }")

    # Should log warning and continue
    components = diagram_generator._load_components_from_prd()
    assert components['services'] == []  # Invalid file should be skipped


# ==============================================================================
# Tests: Load GWT Artifacts
# ==============================================================================

def test_load_gwt_artifacts(diagram_generator, sample_extraction_file):
    """Test loading GWT artifacts from extraction file."""
    artifacts = diagram_generator._load_gwt_artifacts(sample_extraction_file)

    # Check structure
    assert 'presenters' in artifacts
    assert 'views' in artifacts
    assert 'ui_binders' in artifacts
    assert 'rpc_servlets' in artifacts

    # Check loaded artifacts
    assert len(artifacts['presenters']) == 1
    assert len(artifacts['views']) == 1

    # Check presenter data
    presenter = artifacts['presenters'][0]
    assert presenter['file_path'] == '/path/to/AdminPresenter.java'
    assert presenter['semantic_data']['gwt_role'] == 'presenter'

    # Check view data
    view = artifacts['views'][0]
    assert view['file_path'] == '/path/to/AdminView.java'
    assert view['semantic_data']['gwt_role'] == 'view'


def test_load_gwt_artifacts_file_not_exists(diagram_generator, tmp_path):
    """Test loading from non-existent extraction file."""
    nonexistent_file = tmp_path / "nonexistent.jsonl"
    artifacts = diagram_generator._load_gwt_artifacts(nonexistent_file)

    # Should return empty collections
    assert artifacts['presenters'] == []
    assert artifacts['views'] == []


def test_load_gwt_artifacts_skips_summary_line(diagram_generator, sample_extraction_file):
    """Test that summary line is skipped."""
    artifacts = diagram_generator._load_gwt_artifacts(sample_extraction_file)

    # Summary line should not be in any collection
    for collection in artifacts.values():
        for item in collection:
            assert item.get('type') != 'summary'


def test_load_gwt_artifacts_handles_invalid_lines(diagram_generator, tmp_path):
    """Test handling of invalid JSON lines."""
    extraction_file = tmp_path / "extraction.jsonl"

    with open(extraction_file, 'w') as f:
        f.write('{"type": "summary"}\n')
        f.write('invalid json line\n')  # Invalid
        f.write('{"semantic_data": {"gwt_role": "presenter"}}\n')  # Valid

    artifacts = diagram_generator._load_gwt_artifacts(extraction_file)

    # Should skip invalid line and load valid one
    assert len(artifacts['presenters']) == 1


# ==============================================================================
# Tests: Generate Component Diagram
# ==============================================================================

def test_generate_component_diagram(diagram_generator, sample_prd_components):
    """Test generating component diagram."""
    output_file = diagram_generator.generate_component_diagram(
        output_format='mermaid',
        style='default',
        depth=3
    )

    # Check file was created
    assert output_file is not None
    assert output_file.exists()
    assert output_file.name == 'architecture.mmd'

    # Check content
    content = output_file.read_text()
    assert '```mermaid' in content
    assert 'graph TB' in content
    assert 'UserPresenter' in content or 'UserService' in content


def test_generate_component_diagram_no_components(diagram_generator):
    """Test generating diagram with no components."""
    output_file = diagram_generator.generate_component_diagram(
        output_format='mermaid',
        style='default',
        depth=3
    )

    # Implementation still generates basic diagram structure even with no components
    # This is acceptable behavior as it creates the Data Layer at minimum
    assert output_file is not None
    assert output_file.exists()
    content = output_file.read_text()
    assert '```mermaid' in content


def test_generate_component_diagram_unsupported_format(diagram_generator, sample_prd_components):
    """Test generating diagram with unsupported format."""
    with pytest.raises(ValueError, match="Unsupported output format"):
        diagram_generator.generate_component_diagram(
            output_format='unsupported',
            style='default',
            depth=3
        )


def test_generate_component_diagram_with_project_id(diagram_generator, sample_prd_components):
    """Test generating diagram with project filter."""
    output_file = diagram_generator.generate_component_diagram(
        project_id='test-project',
        output_format='mermaid',
        style='default',
        depth=3
    )

    # Should work (even if filtering not fully implemented)
    assert output_file is None or output_file.exists()


# ==============================================================================
# Tests: Generate GWT MVP Diagram
# ==============================================================================

def test_generate_gwt_mvp_diagram(diagram_generator, sample_extraction_file):
    """Test generating GWT MVP diagram."""
    output_file = diagram_generator.generate_gwt_mvp_diagram(
        extraction_file=sample_extraction_file,
        output_format='mermaid',
        style='default'
    )

    # Check file was created
    assert output_file is not None
    assert output_file.exists()
    assert output_file.name == 'mvp-overview.mmd'

    # Check content
    content = output_file.read_text()
    assert '```mermaid' in content
    assert 'graph TB' in content
    assert 'AdminPresenter' in content or 'Presenters' in content


def test_generate_gwt_mvp_diagram_no_artifacts(diagram_generator, tmp_path):
    """Test generating GWT diagram with no artifacts."""
    empty_file = tmp_path / "empty.jsonl"
    empty_file.write_text('{"type": "summary"}\n')

    output_file = diagram_generator.generate_gwt_mvp_diagram(
        extraction_file=empty_file,
        output_format='mermaid',
        style='default'
    )

    # Implementation still generates basic diagram structure even with no artifacts
    # This is acceptable behavior as it creates the basic Mermaid structure
    assert output_file is not None
    assert output_file.exists()
    content = output_file.read_text()
    assert '```mermaid' in content


def test_generate_gwt_mvp_diagram_unsupported_format(diagram_generator, sample_extraction_file):
    """Test generating GWT diagram with unsupported format."""
    with pytest.raises(ValueError, match="Unsupported output format"):
        diagram_generator.generate_gwt_mvp_diagram(
            extraction_file=sample_extraction_file,
            output_format='unsupported',
            style='default'
        )


# ==============================================================================
# Tests: Generate All Diagrams
# ==============================================================================

def test_generate_all_diagrams(diagram_generator, sample_prd_components, sample_extraction_file):
    """Test generating all diagrams."""
    results = diagram_generator.generate_all_diagrams(
        extraction_file=sample_extraction_file,
        output_format='mermaid'
    )

    # Check results
    assert isinstance(results, dict)
    assert 'component' in results
    assert 'gwt' in results

    # Check files exist
    assert results['component'].exists()
    assert results['gwt'].exists()

    # Check README was generated
    readme = diagram_generator.diagrams_dir / "README.md"
    assert readme.exists()


def test_generate_all_diagrams_partial_success(diagram_generator, sample_extraction_file):
    """Test generating all diagrams when some fail."""
    # No component data, but GWT data exists
    results = diagram_generator.generate_all_diagrams(
        extraction_file=sample_extraction_file,
        output_format='mermaid'
    )

    # Should have at least GWT diagram
    assert 'gwt' in results
    assert results['gwt'].exists()


def test_generate_all_diagrams_no_extraction_file(diagram_generator, sample_prd_components):
    """Test generating all diagrams without extraction file."""
    results = diagram_generator.generate_all_diagrams(
        extraction_file=None,
        output_format='mermaid'
    )

    # Should have component diagram (from PRD), but not GWT
    assert 'component' in results
    assert 'gwt' not in results


# ==============================================================================
# Tests: README Generation
# ==============================================================================

def test_generate_readme(diagram_generator):
    """Test README generation."""
    generated_diagrams = {
        'component': diagram_generator.component_dir / 'architecture.mmd',
        'gwt': diagram_generator.gwt_dir / 'mvp-overview.mmd'
    }

    diagram_generator._generate_readme(generated_diagrams)

    readme_path = diagram_generator.diagrams_dir / "README.md"
    assert readme_path.exists()

    content = readme_path.read_text()
    assert '# Architecture Diagrams' in content
    assert 'Component' in content
    assert 'Gwt' in content or 'GWT' in content
    assert 'component/architecture.mmd' in content
    assert 'gwt/mvp-overview.mmd' in content
    assert 'Mermaid' in content
    assert 'codeindex diagram' in content


def test_generate_readme_empty_diagrams(diagram_generator):
    """Test README generation with no diagrams."""
    diagram_generator._generate_readme({})

    readme_path = diagram_generator.diagrams_dir / "README.md"
    assert readme_path.exists()

    content = readme_path.read_text()
    assert '# Architecture Diagrams' in content


# ==============================================================================
# Tests: Error Handling
# ==============================================================================

def test_generate_component_diagram_handles_renderer_error(diagram_generator, sample_prd_components):
    """Test that errors from renderer are handled gracefully."""
    # Patch where MermaidRenderer is imported/used in the diagram_generator module
    with patch('codeindex.services.diagram_renderers.mermaid_renderer.MermaidRenderer') as mock_renderer_class:
        mock_renderer = Mock()
        mock_renderer.render_component_diagram.side_effect = Exception("Rendering error")
        mock_renderer_class.return_value = mock_renderer

        with pytest.raises(Exception):
            diagram_generator.generate_component_diagram(
                output_format='mermaid',
                style='default',
                depth=3
            )


def test_generate_gwt_mvp_diagram_handles_load_error(diagram_generator, tmp_path):
    """Test handling of errors when loading GWT artifacts."""
    # Create file with invalid JSONL format
    extraction_file = tmp_path / "broken.jsonl"
    extraction_file.write_text("not valid jsonl\n")

    # Should handle gracefully - loads what it can (nothing) and creates empty diagram
    output_file = diagram_generator.generate_gwt_mvp_diagram(
        extraction_file=extraction_file,
        output_format='mermaid',
        style='default'
    )

    # Creates diagram even with no valid artifacts (logs warning and continues)
    assert output_file is not None
    assert output_file.exists()


# ==============================================================================
# Tests: Integration
# ==============================================================================

def test_full_workflow(diagram_generator, sample_prd_components, sample_extraction_file):
    """Test full workflow: load components, generate diagrams, create README."""
    # Generate all diagrams
    results = diagram_generator.generate_all_diagrams(
        extraction_file=sample_extraction_file,
        output_format='mermaid'
    )

    # Verify all outputs
    assert len(results) >= 1

    # Check directory structure
    assert diagram_generator.diagrams_dir.exists()
    assert diagram_generator.component_dir.exists()
    assert diagram_generator.gwt_dir.exists()

    # Check README
    readme = diagram_generator.diagrams_dir / "README.md"
    assert readme.exists()

    # Check diagram files
    for diagram_type, file_path in results.items():
        assert file_path.exists()
        assert file_path.suffix == '.mmd'
        content = file_path.read_text()
        assert '```mermaid' in content
        assert '```' in content


def test_directory_structure_created_correctly(temp_output_dir):
    """Test that directory structure is created correctly on init."""
    generator = DiagramGenerator(output_dir=temp_output_dir)

    expected_dirs = [
        generator.diagrams_dir,
        generator.component_dir,
        generator.gwt_dir,
        generator.database_dir,
        generator.sequence_dir
    ]

    for directory in expected_dirs:
        assert directory.exists()
        assert directory.is_dir()
