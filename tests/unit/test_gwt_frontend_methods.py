"""
Unit tests for GWT Frontend Analyzer methods.

Tests the new GWT artifact loading and conversion methods added to FrontendAnalyzer.
"""
import json
import pytest
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock

from codeindex.models.prd import (
    FormDefinition,
    FormField,
    FormType,
    UIComponent,
    ComponentType,
    Event,
    DataBinding,
)
from codeindex.services.frontend_analyzer import FrontendAnalyzer


# ==============================================================================
# Fixtures
# ==============================================================================

@pytest.fixture
def mock_ollama_client():
    """Mock Ollama client."""
    return Mock()


@pytest.fixture
def temp_output_dir(tmp_path):
    """Temporary output directory."""
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    return output_dir


@pytest.fixture
def temp_source_dir(tmp_path):
    """Temporary source directory."""
    source_dir = tmp_path / "source"
    source_dir.mkdir()
    return source_dir


@pytest.fixture
def sample_gwt_extraction_file(tmp_path):
    """Create a sample extraction-results.jsonl file with GWT artifacts."""
    extraction_file = tmp_path / "extraction-results.jsonl"

    artifacts = [
        # GWT Presenter
        {
            "artifact_id": "artifact_001",
            "file_path": "/test/AdminPresenter.java",
            "artifact_type": "GwtPresenter",
            "semantic_data": {
                "gwt_role": "presenter",
                "presenter_name": "AdminPresenter",
                "summary": "Manages admin interface logic",
                "view_binding": "AdminView",
                "event_handlers": [
                    {
                        "name": "onSaveClick",
                        "trigger": "click",
                        "handler": "handleSave",
                        "description": "Saves admin data"
                    },
                    {
                        "name": "onCancelClick",
                        "trigger": "click",
                        "handler": "handleCancel",
                        "description": "Cancels operation"
                    }
                ],
                "rpc_calls": [
                    {
                        "service": "AdminService",
                        "method": "saveData",
                        "description": "Saves admin configuration"
                    },
                    {
                        "service": "UserService",
                        "method": "getUsers",
                        "description": "Retrieves user list"
                    }
                ],
                "navigation_logic": [
                    {"target": "dashboard", "condition": "onSuccess"},
                    {"target": "error", "condition": "onFailure"}
                ],
                "frameworks": ["GWT", "MVP4G"],
                "package": "com.example.admin"
            }
        },
        # GWT View
        {
            "artifact_id": "artifact_002",
            "file_path": "/test/AdminView.java",
            "artifact_type": "GwtView",
            "semantic_data": {
                "gwt_role": "view",
                "view_name": "AdminView",
                "summary": "Admin interface view",
                "component_type": "Composite",
                "ui_fields": [
                    {
                        "field_name": "nameField",
                        "widget_type": "TextBox",
                        "description": "Name input"
                    },
                    {
                        "field_name": "emailField",
                        "widget_type": "TextBox",
                        "description": "Email input"
                    },
                    {
                        "field_name": "activeCheckbox",
                        "widget_type": "CheckBox",
                        "description": "Active status"
                    }
                ],
                "template_file": "AdminView.ui.xml",
                "frameworks": ["GWT"],
                "package": "com.example.admin"
            }
        },
        # GWT UiBinder with form fields
        {
            "artifact_id": "artifact_003",
            "file_path": "/test/UserForm.ui.xml",
            "artifact_type": "GwtUiBinder",
            "semantic_data": {
                "gwt_role": "ui_binder",
                "template_name": "UserForm",
                "summary": "User registration form",
                "form_fields": [
                    {
                        "field_name": "username",
                        "widget_type": "TextBox",
                        "label": "Username *",
                        "default_value": None
                    },
                    {
                        "field_name": "email",
                        "widget_type": "TextBox",
                        "label": "Email Address *",
                        "default_value": None
                    },
                    {
                        "field_name": "password",
                        "widget_type": "PasswordTextBox",
                        "label": "Password",
                        "default_value": None
                    },
                    {
                        "field_name": "active",
                        "widget_type": "CheckBox",
                        "label": "Active",
                        "default_value": "true"
                    },
                    {
                        "field_name": "role",
                        "widget_type": "ListBox",
                        "label": "Role",
                        "default_value": "user"
                    }
                ],
                "frameworks": ["GWT"]
            }
        },
        # GWT UiBinder without form fields (template only)
        {
            "artifact_id": "artifact_004",
            "file_path": "/test/Header.ui.xml",
            "artifact_type": "GwtUiBinder",
            "semantic_data": {
                "gwt_role": "ui_binder",
                "template_name": "Header",
                "summary": "Application header template",
                "form_fields": [],
                "frameworks": ["GWT"]
            }
        },
        # RPC Servlet
        {
            "artifact_id": "artifact_005",
            "file_path": "/test/AdminServlet.java",
            "artifact_type": "GwtRpcServlet",
            "semantic_data": {
                "gwt_role": "rpc_servlet",
                "servlet_name": "AdminServlet",
                "summary": "Admin RPC service"
            }
        },
        # Non-GWT artifact (should be filtered out)
        {
            "artifact_id": "artifact_006",
            "file_path": "/test/Service.java",
            "artifact_type": "JavaClass",
            "semantic_data": {
                "summary": "Regular Java service"
            }
        }
    ]

    # Write artifacts as JSONL (with summary line at top like real extraction files)
    with open(extraction_file, 'w') as f:
        # Add summary line (skipped by loader)
        f.write('{"summary": "Extraction results"}\n')
        for artifact in artifacts:
            f.write(json.dumps(artifact) + '\n')

    return extraction_file


@pytest.fixture
def frontend_analyzer(mock_ollama_client, temp_output_dir, temp_source_dir):
    """Create a FrontendAnalyzer instance."""
    return FrontendAnalyzer(
        ollama_client=mock_ollama_client,
        output_dir=temp_output_dir,
        source_dir=temp_source_dir
    )


# ==============================================================================
# Test load_gwt_artifacts_from_extraction
# ==============================================================================

def test_load_gwt_artifacts_from_extraction(frontend_analyzer, sample_gwt_extraction_file):
    """Test loading GWT artifacts from extraction file."""
    artifacts = frontend_analyzer.load_gwt_artifacts_from_extraction(
        sample_gwt_extraction_file,
        project_id=None
    )

    # Verify categories
    assert 'presenters' in artifacts
    assert 'views' in artifacts
    assert 'ui_binders' in artifacts
    assert 'rpc_servlets' in artifacts
    assert 'shared_dtos' in artifacts

    # Verify counts
    assert len(artifacts['presenters']) == 1
    assert len(artifacts['views']) == 1
    assert len(artifacts['ui_binders']) == 2  # Both with and without form fields
    assert len(artifacts['rpc_servlets']) == 1
    assert len(artifacts['shared_dtos']) == 0

    # Verify presenter data
    presenter = artifacts['presenters'][0]
    assert presenter['semantic_data']['presenter_name'] == 'AdminPresenter'
    assert len(presenter['semantic_data']['event_handlers']) == 2
    assert len(presenter['semantic_data']['rpc_calls']) == 2

    # Verify view data
    view = artifacts['views'][0]
    assert view['semantic_data']['view_name'] == 'AdminView'
    assert len(view['semantic_data']['ui_fields']) == 3

    # Verify UiBinder data
    ui_binders = artifacts['ui_binders']
    form_binder = [u for u in ui_binders if u['semantic_data']['template_name'] == 'UserForm'][0]
    assert len(form_binder['semantic_data']['form_fields']) == 5


def test_load_gwt_artifacts_empty_file(frontend_analyzer, tmp_path):
    """Test loading from empty extraction file."""
    empty_file = tmp_path / "empty.jsonl"
    empty_file.write_text("")

    artifacts = frontend_analyzer.load_gwt_artifacts_from_extraction(empty_file)

    assert len(artifacts['presenters']) == 0
    assert len(artifacts['views']) == 0
    assert len(artifacts['ui_binders']) == 0


def test_load_gwt_artifacts_with_project_filter(frontend_analyzer, tmp_path):
    """Test loading GWT artifacts with project ID filter."""
    extraction_file = tmp_path / "extraction.jsonl"

    artifacts = [
        {
            "artifact_id": "001",
            "file_path": "/test/Presenter1.java",
            "artifact_type": "GwtPresenter",
            "project_id": "project_a",
            "semantic_data": {"gwt_role": "presenter", "presenter_name": "Presenter1"}
        },
        {
            "artifact_id": "002",
            "file_path": "/test/Presenter2.java",
            "artifact_type": "GwtPresenter",
            "project_id": "project_b",
            "semantic_data": {"gwt_role": "presenter", "presenter_name": "Presenter2"}
        }
    ]

    with open(extraction_file, 'w') as f:
        # Add summary line (skipped by loader)
        f.write('{"summary": "Extraction results"}\n')
        for artifact in artifacts:
            f.write(json.dumps(artifact) + '\n')

    # Filter by project_a
    result = frontend_analyzer.load_gwt_artifacts_from_extraction(
        extraction_file,
        project_id="project_a"
    )

    assert len(result['presenters']) == 1
    assert result['presenters'][0]['project_id'] == 'project_a'


# ==============================================================================
# Test convert_gwt_presenter_to_component
# ==============================================================================

def test_convert_gwt_presenter_to_component(frontend_analyzer, sample_gwt_extraction_file):
    """Test converting GWT Presenter artifact to UIComponent."""
    artifacts = frontend_analyzer.load_gwt_artifacts_from_extraction(sample_gwt_extraction_file)
    presenter_artifact = artifacts['presenters'][0]

    component = frontend_analyzer.convert_gwt_presenter_to_component(presenter_artifact)

    # Verify basic attributes
    assert isinstance(component, UIComponent)
    assert component.name == "AdminPresenter"
    assert component.component_type == ComponentType.GWT_PRESENTER
    assert component.description == "Manages admin interface logic"
    assert component.source_file == "/test/AdminPresenter.java"
    assert component.created_at is not None

    # Verify event handlers
    assert len(component.events_handled) == 2
    event1 = component.events_handled[0]
    assert isinstance(event1, Event)
    assert event1.name == "onSaveClick"
    assert event1.type == "click"
    assert event1.handler == "handleSave"
    assert event1.description == "Saves admin data"

    # Verify data bindings (RPC calls)
    assert len(component.data_bindings) == 2
    binding1 = component.data_bindings[0]
    assert isinstance(binding1, DataBinding)
    assert binding1.field_name == "saveData"
    assert binding1.data_source == "AdminService"
    assert binding1.binding_type == "rpc_call"

    # Verify navigation targets
    assert len(component.navigation_targets) == 2
    assert "dashboard" in component.navigation_targets
    assert "error" in component.navigation_targets


def test_convert_gwt_presenter_minimal(frontend_analyzer):
    """Test converting presenter with minimal data."""
    minimal_artifact = {
        "file_path": "/test/MinimalPresenter.java",
        "semantic_data": {
            "presenter_name": "MinimalPresenter",
            "summary": "Minimal presenter"
        }
    }

    component = frontend_analyzer.convert_gwt_presenter_to_component(minimal_artifact)

    assert component.name == "MinimalPresenter"
    assert component.component_type == ComponentType.GWT_PRESENTER
    assert len(component.events_handled) == 0
    assert len(component.data_bindings) == 0
    assert len(component.navigation_targets) == 0


# ==============================================================================
# Test convert_gwt_view_to_component
# ==============================================================================

def test_convert_gwt_view_to_component(frontend_analyzer, sample_gwt_extraction_file):
    """Test converting GWT View artifact to UIComponent."""
    artifacts = frontend_analyzer.load_gwt_artifacts_from_extraction(sample_gwt_extraction_file)
    view_artifact = artifacts['views'][0]

    component = frontend_analyzer.convert_gwt_view_to_component(view_artifact)

    # Verify basic attributes
    assert isinstance(component, UIComponent)
    assert component.name == "AdminView"
    assert component.component_type == ComponentType.GWT_VIEW
    assert component.description == "Admin interface view"
    assert component.source_file == "/test/AdminView.java"
    assert component.created_at is not None

    # Verify data bindings (UI fields)
    assert len(component.data_bindings) == 3
    binding1 = component.data_bindings[0]
    assert isinstance(binding1, DataBinding)
    assert binding1.field_name == "nameField"
    assert binding1.data_source == "TextBox"
    assert binding1.binding_type == "ui_field"


def test_convert_gwt_view_minimal(frontend_analyzer):
    """Test converting view with minimal data."""
    minimal_artifact = {
        "file_path": "/test/MinimalView.java",
        "semantic_data": {
            "view_name": "MinimalView",
            "summary": "Minimal view"
        }
    }

    component = frontend_analyzer.convert_gwt_view_to_component(minimal_artifact)

    assert component.name == "MinimalView"
    assert component.component_type == ComponentType.GWT_VIEW
    assert len(component.data_bindings) == 0


# ==============================================================================
# Test convert_gwt_uibinder_to_form
# ==============================================================================

def test_convert_gwt_uibinder_to_form(frontend_analyzer, sample_gwt_extraction_file):
    """Test converting GWT UiBinder artifact to FormDefinition."""
    artifacts = frontend_analyzer.load_gwt_artifacts_from_extraction(sample_gwt_extraction_file)
    uibinder_artifacts = artifacts['ui_binders']
    form_artifact = [u for u in uibinder_artifacts if u['semantic_data']['template_name'] == 'UserForm'][0]

    form = frontend_analyzer.convert_gwt_uibinder_to_form(form_artifact)

    # Verify basic attributes
    assert isinstance(form, FormDefinition)
    assert form.name == "UserForm"
    assert form.form_type == FormType.GWT_FORM
    assert form.description == "User registration form"
    assert form.source_file == "/test/UserForm.ui.xml"
    assert form.created_at is not None

    # Verify fields
    assert len(form.fields) == 5

    # Check username field
    username_field = form.fields[0]
    assert isinstance(username_field, FormField)
    assert username_field.name == "username"
    assert username_field.type == "text"
    assert username_field.label == "Username *"
    assert username_field.required is True  # Has * in label

    # Check email field
    email_field = form.fields[1]
    assert email_field.name == "email"
    assert email_field.type == "text"
    assert email_field.required is True

    # Check password field
    password_field = form.fields[2]
    assert password_field.name == "password"
    assert password_field.type == "password"

    # Check checkbox field
    checkbox_field = form.fields[3]
    assert checkbox_field.name == "active"
    assert checkbox_field.type == "checkbox"
    assert checkbox_field.default_value == "true"

    # Check listbox field
    listbox_field = form.fields[4]
    assert listbox_field.name == "role"
    assert listbox_field.type == "select"


def test_convert_gwt_uibinder_without_fields_returns_none(frontend_analyzer, sample_gwt_extraction_file):
    """Test that UiBinder without form fields returns None."""
    artifacts = frontend_analyzer.load_gwt_artifacts_from_extraction(sample_gwt_extraction_file)
    uibinder_artifacts = artifacts['ui_binders']
    header_artifact = [u for u in uibinder_artifacts if u['semantic_data']['template_name'] == 'Header'][0]

    form = frontend_analyzer.convert_gwt_uibinder_to_form(header_artifact)

    # Should return None because no form fields
    assert form is None


def test_convert_gwt_uibinder_widget_type_mapping(frontend_analyzer):
    """Test widget type to form field type mapping."""
    artifact = {
        "file_path": "/test/TestForm.ui.xml",
        "semantic_data": {
            "template_name": "TestForm",
            "summary": "Test form",
            "form_fields": [
                {"field_name": "text", "widget_type": "TextBox"},
                {"field_name": "password", "widget_type": "PasswordTextBox"},
                {"field_name": "textarea", "widget_type": "TextArea"},
                {"field_name": "number", "widget_type": "IntegerBox"},
                {"field_name": "double", "widget_type": "DoubleBox"},
                {"field_name": "select", "widget_type": "ListBox"},
                {"field_name": "checkbox", "widget_type": "CheckBox"},
                {"field_name": "radio", "widget_type": "RadioButton"},
                {"field_name": "date", "widget_type": "DateBox"},
                {"field_name": "button", "widget_type": "Button"},
                {"field_name": "submit", "widget_type": "SubmitButton"},
                {"field_name": "unknown", "widget_type": "CustomWidget"}
            ]
        }
    }

    form = frontend_analyzer.convert_gwt_uibinder_to_form(artifact)

    assert form.fields[0].type == "text"
    assert form.fields[1].type == "password"
    assert form.fields[2].type == "textarea"
    assert form.fields[3].type == "number"
    assert form.fields[4].type == "number"
    assert form.fields[5].type == "select"
    assert form.fields[6].type == "checkbox"
    assert form.fields[7].type == "radio"
    assert form.fields[8].type == "date"
    assert form.fields[9].type == "button"
    assert form.fields[10].type == "submit"
    assert form.fields[11].type == "text"  # Unknown types default to text


# ==============================================================================
# Test process_gwt_artifacts
# ==============================================================================

def test_process_gwt_artifacts(frontend_analyzer, sample_gwt_extraction_file, temp_output_dir):
    """Test processing all GWT artifacts."""
    counts = frontend_analyzer.process_gwt_artifacts(
        sample_gwt_extraction_file,
        project_id=None
    )

    # Verify counts
    assert counts['presenters'] == 1
    assert counts['views'] == 1
    assert counts['ui_binders'] == 1  # Only the one with form fields
    assert counts['total_components'] == 2  # 1 presenter + 1 view
    assert counts['total_forms'] == 1

    # Verify files were saved
    forms_dir = temp_output_dir / "frontend" / "forms"
    components_dir = temp_output_dir / "frontend" / "components"

    assert forms_dir.exists()
    assert components_dir.exists()

    # Check that JSON files were created
    form_files = list(forms_dir.glob("*.json"))
    component_files = list(components_dir.glob("*.json"))

    assert len(form_files) == 1
    assert len(component_files) == 2


def test_process_gwt_artifacts_empty_file(frontend_analyzer, tmp_path):
    """Test processing empty extraction file."""
    empty_file = tmp_path / "empty.jsonl"
    empty_file.write_text("")

    counts = frontend_analyzer.process_gwt_artifacts(empty_file)

    assert counts['presenters'] == 0
    assert counts['views'] == 0
    assert counts['ui_binders'] == 0
    assert counts['total_components'] == 0
    assert counts['total_forms'] == 0


def test_process_gwt_artifacts_with_errors(frontend_analyzer, tmp_path, caplog):
    """Test processing artifacts with some errors."""
    extraction_file = tmp_path / "extraction.jsonl"

    artifacts = [
        # Valid presenter
        {
            "file_path": "/test/Valid.java",
            "artifact_type": "GwtPresenter",
            "semantic_data": {
                "gwt_role": "presenter",
                "presenter_name": "ValidPresenter"
            }
        },
        # Invalid presenter (missing semantic_data)
        {
            "file_path": "/test/Invalid.java",
            "artifact_type": "GwtPresenter"
        }
    ]

    with open(extraction_file, 'w') as f:
        # Add summary line (skipped by loader)
        f.write('{"summary": "Extraction results"}\n')
        for artifact in artifacts:
            f.write(json.dumps(artifact) + '\n')

    counts = frontend_analyzer.process_gwt_artifacts(extraction_file)

    # Should process the valid one, skip the invalid one
    assert counts['presenters'] == 1
    assert counts['total_components'] == 1


def test_process_gwt_artifacts_integration(frontend_analyzer, sample_gwt_extraction_file, temp_output_dir):
    """Integration test: process artifacts and verify saved data."""
    counts = frontend_analyzer.process_gwt_artifacts(sample_gwt_extraction_file)

    # Verify counts
    assert counts['total_components'] == 2
    assert counts['total_forms'] == 1

    # Load and verify saved form
    forms_dir = temp_output_dir / "frontend" / "forms"
    form_files = list(forms_dir.glob("*.json"))
    assert len(form_files) == 1

    with open(form_files[0]) as f:
        form_data = json.load(f)
        assert form_data['name'] == 'UserForm'
        assert form_data['form_type'] == 'gwt_form'
        assert len(form_data['fields']) == 5

    # Load and verify saved components
    components_dir = temp_output_dir / "frontend" / "components"
    component_files = list(components_dir.glob("*.json"))
    assert len(component_files) == 2

    # Find presenter component
    presenter_file = [f for f in component_files if 'AdminPresenter' in f.read_text()][0]
    with open(presenter_file) as f:
        presenter_data = json.load(f)
        assert presenter_data['name'] == 'AdminPresenter'
        assert presenter_data['component_type'] == 'gwt_presenter'
        assert len(presenter_data['events_handled']) == 2
        assert len(presenter_data['data_bindings']) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
