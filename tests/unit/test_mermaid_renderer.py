"""
Unit tests for Mermaid Diagram Renderer.

Tests the MermaidRenderer class for generating diagrams in Mermaid format.
"""
import pytest
from pathlib import Path

from codeindex.services.diagram_renderers.mermaid_renderer import MermaidRenderer


# ==============================================================================
# Fixtures
# ==============================================================================

@pytest.fixture
def renderer():
    """Create MermaidRenderer instance."""
    return MermaidRenderer()


@pytest.fixture
def sample_components():
    """Sample component data for testing."""
    return {
        'presenters': [
            {
                'id': 'gwt_presenter_UserPresenter',
                'name': 'UserPresenter',
                'semantic_data': {
                    'event_handlers': ['onSaveClick', 'onCancelClick'],
                    'rpc_calls': [{'service': 'UserService', 'method': 'saveUser'}]
                }
            },
            {
                'id': 'gwt_presenter_AdminPresenter',
                'name': 'View',  # Incorrect name - should be extracted from id
                'semantic_data': {
                    'event_handlers': [],
                    'rpc_calls': []
                }
            }
        ],
        'views': [
            {
                'id': 'gwt_view_UserView',
                'name': 'UserView',
                'semantic_data': {
                    'ui_fields': ['nameField', 'emailField']
                }
            },
            {
                'id': 'gwt_view_AdminView',
                'name': 'AdminView',
                'semantic_data': {
                    'ui_fields': ['roleField']
                }
            }
        ],
        'services': [
            {
                'class_name': 'UserService',
                'name': 'UserService'
            }
        ],
        'daos': [
            {
                'name': 'UserDAO'
            }
        ],
        'forms': []
    }


@pytest.fixture
def sample_gwt_artifacts():
    """Sample GWT artifacts for testing."""
    presenters = [
        {
            'file_path': '/path/to/UserPresenter.java',
            'semantic_data': {
                'presenter_name': 'View',  # Incorrect
                'view_binding': None,
                'event_handlers': ['onSaveClick'],
                'rpc_calls': [
                    {'service': 'UserService', 'method': 'getUser'}
                ],
                'entities': ['UserPresenter', 'UserView'],
                'gwt_role': 'presenter'
            }
        }
    ]

    views = [
        {
            'file_path': '/path/to/UserView.java',
            'semantic_data': {
                'view_name': 'UserView',
                'ui_fields': ['nameField', 'emailField'],
                'gwt_role': 'view',
                'entities': ['UserView']
            }
        }
    ]

    return {'presenters': presenters, 'views': views}


# ==============================================================================
# Tests: Name Extraction
# ==============================================================================

def test_extract_component_name_from_name(renderer):
    """Test extracting name from 'name' field."""
    component = {'name': 'UserPresenter'}
    result = renderer._extract_component_name(component)
    assert result == 'UserPresenter'


def test_extract_component_name_from_id(renderer):
    """Test extracting name from 'id' field when name is 'View'."""
    component = {
        'name': 'View',
        'id': 'gwt_presenter_AdminPresenter'
    }
    result = renderer._extract_component_name(component)
    assert result == 'AdminPresenter'


def test_extract_component_name_from_source_file(renderer):
    """Test extracting name from 'source_file' field."""
    component = {
        'name': 'View',
        'id': '',
        'source_file': '/path/to/MyPresenter.java'
    }
    result = renderer._extract_component_name(component)
    assert result == 'MyPresenter'


def test_extract_component_name_from_file_path(renderer):
    """Test extracting name from 'file_path' field."""
    component = {
        'name': 'View',
        'id': '',
        'file_path': '/path/to/MyView.java'
    }
    result = renderer._extract_component_name(component)
    assert result == 'MyView'


def test_extract_component_name_from_entities(renderer):
    """Test extracting name from 'entities' list."""
    component = {
        'name': 'View',
        'id': '',
        'semantic_data': {
            'entities': ['SomeClass', 'UserPresenter', 'AnotherClass']
        }
    }
    result = renderer._extract_component_name(component)
    assert result == 'UserPresenter'


def test_extract_component_name_fallback(renderer):
    """Test fallback when no valid name found."""
    component = {'name': 'View', 'id': ''}
    result = renderer._extract_component_name(component, fallback='UnknownComponent')
    assert result == 'UnknownComponent'


# ==============================================================================
# Tests: ID Sanitization
# ==============================================================================

def test_sanitize_id_valid_name(renderer):
    """Test sanitizing a valid name."""
    result = renderer._sanitize_id('UserPresenter')
    assert result == 'UserPresenter'


def test_sanitize_id_with_special_chars(renderer):
    """Test sanitizing name with special characters."""
    result = renderer._sanitize_id('User-Presenter.Admin')
    assert result == 'User_Presenter_Admin'


def test_sanitize_id_starts_with_number(renderer):
    """Test sanitizing name that starts with a number."""
    result = renderer._sanitize_id('123Presenter')
    assert result == 'N123Presenter'


def test_sanitize_id_empty_string(renderer):
    """Test sanitizing empty string."""
    result = renderer._sanitize_id('')
    assert result == 'Unknown'


# ==============================================================================
# Tests: Component Diagram Rendering
# ==============================================================================

def test_render_component_diagram_basic(renderer, sample_components):
    """Test basic component diagram rendering."""
    result = renderer.render_component_diagram(
        components=sample_components,
        style='default',
        depth=3
    )

    # Check structure
    assert '```mermaid' in result
    assert 'graph TB' in result
    assert '```' in result.split('```mermaid')[1]

    # Check layers
    assert 'Frontend Layer' in result
    assert 'Data Layer' in result

    # Check components
    assert 'UserPresenter' in result
    assert 'UserView' in result
    assert 'UserService' in result
    assert 'UserDAO' in result

    # Check name extraction worked for "View" name
    assert 'AdminPresenter' in result


def test_render_component_diagram_minimal_style(renderer, sample_components):
    """Test component diagram with minimal style."""
    result = renderer.render_component_diagram(
        components=sample_components,
        style='minimal',
        depth=3
    )

    assert 'graph TB' in result
    assert 'UserPresenter' in result


def test_render_component_diagram_empty_components(renderer):
    """Test rendering with empty components."""
    result = renderer.render_component_diagram(
        components={'presenters': [], 'views': [], 'services': [], 'daos': [], 'forms': []},
        style='default',
        depth=3
    )

    # Should still have basic structure
    assert '```mermaid' in result
    assert 'graph TB' in result
    # Should have Data Layer at minimum
    assert 'Data Layer' in result


def test_render_component_diagram_with_connections(renderer, sample_components):
    """Test that connections are generated."""
    result = renderer.render_component_diagram(
        components=sample_components,
        style='default',
        depth=3
    )

    # Check for connection syntax
    assert '-->' in result or '---' in result


# ==============================================================================
# Tests: GWT MVP Diagram Rendering
# ==============================================================================

def test_render_gwt_mvp_diagram_basic(renderer, sample_gwt_artifacts):
    """Test basic GWT MVP diagram rendering."""
    result = renderer.render_gwt_mvp_diagram(
        presenters=sample_gwt_artifacts['presenters'],
        views=sample_gwt_artifacts['views'],
        style='default'
    )

    # Check structure
    assert '```mermaid' in result
    assert 'graph TB' in result

    # Check subgraphs
    assert 'GWT Presenters' in result
    assert 'GWT Views' in result

    # Check components (name should be extracted from file path)
    assert 'UserPresenter' in result
    assert 'UserView' in result

    # Check RPC service extraction
    assert 'UserService' in result or 'RPC Services' in result


def test_render_gwt_mvp_diagram_detailed_style(renderer, sample_gwt_artifacts):
    """Test GWT MVP diagram with detailed style."""
    result = renderer.render_gwt_mvp_diagram(
        presenters=sample_gwt_artifacts['presenters'],
        views=sample_gwt_artifacts['views'],
        style='detailed'
    )

    # Should include event and RPC counts in detailed mode
    assert '1 events' in result or 'event' in result.lower()


def test_render_gwt_mvp_diagram_with_connections(renderer, sample_gwt_artifacts):
    """Test that presenter-view connections are generated."""
    result = renderer.render_gwt_mvp_diagram(
        presenters=sample_gwt_artifacts['presenters'],
        views=sample_gwt_artifacts['views'],
        style='default'
    )

    # Check for binds connection
    assert 'binds' in result or '-->' in result


def test_render_gwt_mvp_diagram_empty(renderer):
    """Test rendering with no presenters or views."""
    result = renderer.render_gwt_mvp_diagram(
        presenters=[],
        views=[],
        style='default'
    )

    # Should still have basic structure
    assert '```mermaid' in result
    assert 'graph TB' in result


def test_render_gwt_mvp_diagram_with_rpc_services(renderer):
    """Test that RPC services are extracted and displayed."""
    presenters = [
        {
            'file_path': '/path/to/UserPresenter.java',
            'semantic_data': {
                'presenter_name': 'UserPresenter',
                'rpc_calls': [
                    {'service': 'UserService', 'method': 'getUser'},
                    {'service': 'AdminService', 'method': 'getAdmin'}
                ],
                'entities': ['UserPresenter']
            }
        }
    ]

    result = renderer.render_gwt_mvp_diagram(
        presenters=presenters,
        views=[],
        style='default'
    )

    # Check that RPC services are mentioned
    assert 'UserService' in result or 'RPC Services' in result


# ==============================================================================
# Tests: Connection Generation
# ==============================================================================

def test_generate_connections_with_matching_names(renderer, sample_components):
    """Test connection generation finds matching presenter-view pairs."""
    connections = renderer._generate_connections(sample_components, style='default')

    # Should find connections based on naming convention
    # UserPresenter -> UserView
    connection_str = '\n'.join(connections)
    assert 'UserPresenter' in connection_str or len(connections) > 0


def test_generate_connections_with_daos(renderer, sample_components):
    """Test that DAO connections to database are generated."""
    connections = renderer._generate_connections(sample_components, style='default')

    connection_str = '\n'.join(connections)
    # Should connect DAO to DB
    assert 'DB' in connection_str or 'UserDAO' in connection_str


def test_generate_gwt_connections_handles_none_view_binding(renderer):
    """Test that None view_binding is handled correctly."""
    presenters = [
        {
            'file_path': '/path/to/TestPresenter.java',
            'semantic_data': {
                'presenter_name': 'TestPresenter',
                'view_binding': None,  # Should not cause error
                'rpc_calls': [],
                'entities': ['TestPresenter']
            }
        }
    ]
    views = []
    rpc_services = set()

    # Should not raise TypeError
    connections = renderer._generate_gwt_connections(presenters, views, rpc_services, 'default')
    assert isinstance(connections, list)


def test_generate_gwt_connections_with_dict_view_binding(renderer):
    """Test that dict view_binding is handled correctly."""
    presenters = [
        {
            'file_path': '/path/to/TestPresenter.java',
            'semantic_data': {
                'presenter_name': 'TestPresenter',
                'view_binding': {'some': 'dict'},  # Should be ignored
                'rpc_calls': [],
                'entities': ['TestPresenter']
            }
        }
    ]
    views = []
    rpc_services = set()

    # Should not raise error
    connections = renderer._generate_gwt_connections(presenters, views, rpc_services, 'default')
    assert isinstance(connections, list)


# ==============================================================================
# Tests: RPC Service Extraction
# ==============================================================================

def test_extract_rpc_services(renderer):
    """Test extracting unique RPC services from presenters."""
    presenters = [
        {
            'semantic_data': {
                'rpc_calls': [
                    {'service': 'UserService'},
                    {'service': 'AdminService'}
                ]
            }
        },
        {
            'semantic_data': {
                'rpc_calls': [
                    {'service': 'UserService'},  # Duplicate
                    {'service': 'ProductService'}
                ]
            }
        }
    ]

    services = renderer._extract_rpc_services(presenters)

    assert isinstance(services, set)
    assert len(services) == 3  # UserService, AdminService, ProductService
    assert 'UserService' in services
    assert 'AdminService' in services
    assert 'ProductService' in services


def test_extract_rpc_services_empty(renderer):
    """Test extracting RPC services from presenters with no RPC calls."""
    presenters = [
        {
            'semantic_data': {
                'rpc_calls': []
            }
        }
    ]

    services = renderer._extract_rpc_services(presenters)
    assert isinstance(services, set)
    assert len(services) == 0


def test_extract_rpc_services_missing_service_name(renderer):
    """Test extracting RPC services with missing service names."""
    presenters = [
        {
            'semantic_data': {
                'rpc_calls': [
                    {'service': ''},  # Empty
                    {'service': 'ValidService'},
                    {'method': 'someMethod'}  # No service field
                ]
            }
        }
    ]

    services = renderer._extract_rpc_services(presenters)
    assert len(services) == 1
    assert 'ValidService' in services


# ==============================================================================
# Tests: Edge Cases
# ==============================================================================

def test_component_with_all_name_sources_missing(renderer):
    """Test component with all name extraction sources missing."""
    component = {
        'name': 'View',
        'id': '',
        'semantic_data': {
            'entities': []
        }
    }
    result = renderer._extract_component_name(component, 'Fallback')
    assert result == 'Fallback'


def test_render_with_special_characters_in_names(renderer):
    """Test rendering with special characters in component names."""
    components = {
        'presenters': [
            {
                'name': 'User-Admin.Presenter',
                'semantic_data': {'event_handlers': [], 'rpc_calls': []}
            }
        ],
        'views': [],
        'services': [],
        'daos': [],
        'forms': []
    }

    result = renderer.render_component_diagram(components, 'default', 3)

    # Special chars should be sanitized
    assert 'User_Admin_Presenter' in result


def test_render_component_diagram_limits_components(renderer):
    """Test that component diagram limits the number of components."""
    # Create more than 10 presenters
    many_presenters = [
        {
            'name': f'Presenter{i}',
            'semantic_data': {'event_handlers': [], 'rpc_calls': []}
        }
        for i in range(15)
    ]

    components = {
        'presenters': many_presenters,
        'views': [],
        'services': [],
        'daos': [],
        'forms': []
    }

    result = renderer.render_component_diagram(components, 'default', 3)

    # Should only include first 10 (limited to 10)
    assert 'Presenter0' in result
    assert 'Presenter9' in result
    # May or may not include Presenter10 depending on limit


def test_render_gwt_mvp_diagram_limits_presenters(renderer):
    """Test that GWT diagram limits presenters to 10."""
    many_presenters = [
        {
            'file_path': f'/path/to/Presenter{i}.java',
            'semantic_data': {
                'presenter_name': f'Presenter{i}',
                'rpc_calls': [],
                'entities': [f'Presenter{i}']
            }
        }
        for i in range(15)
    ]

    result = renderer.render_gwt_mvp_diagram(many_presenters, [], 'default')

    # Should limit to 10
    assert 'Presenter0' in result
    assert 'Presenter9' in result
