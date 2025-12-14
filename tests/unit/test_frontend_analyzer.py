"""
Unit tests for Frontend Analyzer Service.
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
    NavigationFlow,
    FlowType,
    EntryPoint,
    NavigationStep,
    ExitPoint,
    VisitStatus,
    AnalysisLayer,
)
from codeindex.services.frontend_analyzer import FrontendAnalyzer


# ==============================================================================
# Fixtures
# ==============================================================================

@pytest.fixture
def mock_ollama_client():
    """Mock Ollama client."""
    client = Mock()
    return client


@pytest.fixture
def temp_output_dir(tmp_path):
    """Temporary output directory."""
    return tmp_path / "output"


@pytest.fixture
def temp_source_dir(tmp_path):
    """Temporary source directory with test files."""
    source_dir = tmp_path / "source"
    source_dir.mkdir()

    # Create a sample JSP form file
    jsp_file = source_dir / "userForm.jsp"
    jsp_file.write_text("""
<%@ page language="java" contentType="text/html; charset=UTF-8" %>
<html>
<body>
    <h2>User Registration</h2>
    <form action="/api/users" method="POST">
        <label for="email">Email:</label>
        <input type="email" id="email" name="email" required />

        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required />

        <label for="confirmPassword">Confirm Password:</label>
        <input type="password" id="confirmPassword" name="confirmPassword" required />

        <button type="submit">Register</button>
    </form>
</body>
</html>
""", encoding="utf-8")

    # Create a sample HTML file
    html_file = source_dir / "login.html"
    html_file.write_text("""
<!DOCTYPE html>
<html>
<head><title>Login</title></head>
<body>
    <form id="loginForm" action="/auth/login" method="POST">
        <input type="text" name="username" required />
        <input type="password" name="password" required />
        <button type="submit">Login</button>
    </form>
</body>
</html>
""", encoding="utf-8")

    return source_dir


@pytest.fixture
def sample_form_llm_response():
    """Sample LLM response for form extraction."""
    return {
        "response": json.dumps({
            "form_name": "userRegistrationForm",
            "form_type": "jsp_form",
            "description": "User registration form for creating new user accounts. Collects email and password.",
            "fields": [
                {
                    "name": "email",
                    "type": "email",
                    "label": "Email",
                    "required": True,
                    "validation_pattern": "^[^@]+@[^@]+\\.[^@]+$"
                },
                {
                    "name": "password",
                    "type": "password",
                    "label": "Password",
                    "required": True,
                    "validation_pattern": ".{8,}"
                },
                {
                    "name": "confirmPassword",
                    "type": "password",
                    "label": "Confirm Password",
                    "required": True,
                    "validation_pattern": None
                }
            ],
            "submission_endpoint": "/api/users",
            "submission_method": "POST",
            "bound_entities": ["user"]
        })
    }


# ==============================================================================
# Model Tests
# ==============================================================================

def test_form_field_creation():
    """Test FormField model creation."""
    field = FormField(
        name="email",
        type="email",
        label="Email Address",
        required=True,
        validation_pattern="^[^@]+@[^@]+\\.[^@]+$"
    )

    assert field.name == "email"
    assert field.type == "email"
    assert field.required is True
    assert field.validation_pattern is not None

    # Test to_dict
    field_dict = field.to_dict()
    assert field_dict["name"] == "email"
    assert field_dict["required"] is True

    # Test from_dict
    field2 = FormField.from_dict(field_dict)
    assert field2.name == field.name
    assert field2.required == field.required


def test_form_definition_creation():
    """Test FormDefinition model creation."""
    form = FormDefinition(
        id="userForm_registration",
        name="userRegistrationForm",
        source_file="/path/to/userForm.jsp",
        form_type=FormType.JSP_FORM,
        fields=[
            FormField(name="email", type="email", required=True),
            FormField(name="password", type="password", required=True)
        ],
        submission_endpoint="/api/users",
        submission_method="POST",
        created_at=datetime.now()
    )

    assert form.id == "userForm_registration"
    assert form.name == "userRegistrationForm"
    assert form.form_type == FormType.JSP_FORM
    assert len(form.fields) == 2
    assert form.submission_method == "POST"

    # Test to_dict
    form_dict = form.to_dict()
    assert form_dict["id"] == "userForm_registration"
    assert len(form_dict["fields"]) == 2
    assert form_dict["form_type"] == "jsp_form"

    # Test from_dict
    form2 = FormDefinition.from_dict(form_dict)
    assert form2.id == form.id
    assert len(form2.fields) == len(form.fields)


def test_form_definition_validation():
    """Test FormDefinition validation."""
    # Missing required fields
    with pytest.raises(ValueError, match="id is required"):
        FormDefinition(
            id="",
            name="testForm",
            source_file="/path/to/form.jsp",
            form_type=FormType.JSP_FORM,
            fields=[FormField(name="test", type="text")],
            created_at=datetime.now()
        )

    # No fields
    with pytest.raises(ValueError, match="fields is required"):
        FormDefinition(
            id="testForm",
            name="testForm",
            source_file="/path/to/form.jsp",
            form_type=FormType.JSP_FORM,
            fields=[],
            created_at=datetime.now()
        )


def test_ui_component_creation():
    """Test UIComponent model creation."""
    component = UIComponent(
        id="com.example.UserPanel",
        name="UserPanel",
        component_type=ComponentType.GWT_WIDGET,
        source_file="/path/to/UserPanel.java",
        description="User management panel widget",
        responsibilities=["Display user list", "Handle user actions"],
        created_at=datetime.now()
    )

    assert component.id == "com.example.UserPanel"
    assert component.name == "UserPanel"
    assert component.component_type == ComponentType.GWT_WIDGET
    assert len(component.responsibilities) == 2

    # Test to_dict
    component_dict = component.to_dict()
    assert component_dict["id"] == "com.example.UserPanel"
    assert component_dict["component_type"] == "gwt_widget"

    # Test from_dict
    component2 = UIComponent.from_dict(component_dict)
    assert component2.id == component.id
    assert component2.component_type == component.component_type


def test_navigation_flow_creation():
    """Test NavigationFlow model creation."""
    flow = NavigationFlow(
        id="user_registration_flow",
        name="User Registration Flow",
        flow_type=FlowType.WIZARD,
        entry_points=[
            EntryPoint(entry_type="direct_url", source="/register")
        ],
        steps=[
            NavigationStep(step_number=1, page_url="/register", action="Fill form"),
            NavigationStep(step_number=2, page_url="/confirm", action="Confirm registration")
        ],
        description="Multi-step user registration process",
        created_at=datetime.now()
    )

    assert flow.id == "user_registration_flow"
    assert flow.flow_type == FlowType.WIZARD
    assert len(flow.entry_points) == 1
    assert len(flow.steps) == 2

    # Test to_dict
    flow_dict = flow.to_dict()
    assert flow_dict["id"] == "user_registration_flow"
    assert flow_dict["flow_type"] == "wizard"
    assert len(flow_dict["steps"]) == 2

    # Test from_dict
    flow2 = NavigationFlow.from_dict(flow_dict)
    assert flow2.id == flow.id
    assert len(flow2.steps) == len(flow.steps)


# ==============================================================================
# Frontend Analyzer Tests
# ==============================================================================

def test_frontend_analyzer_init(mock_ollama_client, temp_output_dir, temp_source_dir):
    """Test FrontendAnalyzer initialization."""
    analyzer = FrontendAnalyzer(
        ollama_client=mock_ollama_client,
        output_dir=temp_output_dir,
        source_dir=temp_source_dir
    )

    assert analyzer.output_dir == temp_output_dir
    assert analyzer.source_dir == temp_source_dir
    assert analyzer.max_workers == 10
    assert analyzer.forms_dir.exists()
    assert analyzer.components_dir.exists()
    assert analyzer.navigation_dir.exists()


def test_find_frontend_files(mock_ollama_client, temp_output_dir, temp_source_dir):
    """Test finding frontend files."""
    analyzer = FrontendAnalyzer(
        ollama_client=mock_ollama_client,
        output_dir=temp_output_dir,
        source_dir=temp_source_dir
    )

    files = analyzer.find_frontend_files()

    # Should find userForm.jsp and login.html
    assert len(files) >= 2
    assert any("userForm.jsp" in str(f) for f in files)
    assert any("login.html" in str(f) for f in files)


def test_detect_file_type(mock_ollama_client, temp_output_dir, temp_source_dir):
    """Test file type detection."""
    analyzer = FrontendAnalyzer(
        ollama_client=mock_ollama_client,
        output_dir=temp_output_dir,
        source_dir=temp_source_dir
    )

    # Find test files
    files = analyzer.find_frontend_files()

    for file_path in files:
        file_type = analyzer._detect_file_type(file_path)
        if file_path.suffix == ".jsp":
            assert file_type == "JSP"
        elif file_path.suffix == ".html":
            assert file_type == "HTML"


def test_has_form(mock_ollama_client, temp_output_dir, temp_source_dir):
    """Test form detection in file content."""
    analyzer = FrontendAnalyzer(
        ollama_client=mock_ollama_client,
        output_dir=temp_output_dir,
        source_dir=temp_source_dir
    )

    # Content with form
    form_content = '<form action="/submit" method="POST"><input name="test" /></form>'
    assert analyzer._has_form(form_content) is True

    # Content without form
    no_form_content = '<div><p>Just some text</p></div>'
    assert analyzer._has_form(no_form_content) is False


def test_compute_file_hash(mock_ollama_client, temp_output_dir, temp_source_dir):
    """Test file hash computation."""
    analyzer = FrontendAnalyzer(
        ollama_client=mock_ollama_client,
        output_dir=temp_output_dir,
        source_dir=temp_source_dir
    )

    files = analyzer.find_frontend_files()
    if files:
        test_file = files[0]
        hash1 = analyzer._compute_file_hash(test_file)

        assert len(hash1) == 64  # SHA-256 hex string
        assert all(c in "0123456789abcdef" for c in hash1)

        # Same file should produce same hash
        hash2 = analyzer._compute_file_hash(test_file)
        assert hash1 == hash2


def test_analyze_file_with_mock_llm(
    mock_ollama_client,
    temp_output_dir,
    temp_source_dir,
    sample_form_llm_response
):
    """Test analyzing a single file with mocked LLM."""
    # Mock LLM response
    mock_ollama_client.call_ollama.return_value = sample_form_llm_response

    analyzer = FrontendAnalyzer(
        ollama_client=mock_ollama_client,
        output_dir=temp_output_dir,
        source_dir=temp_source_dir
    )

    # Find test file
    files = analyzer.find_frontend_files()
    jsp_files = [f for f in files if "userForm.jsp" in str(f)]
    assert len(jsp_files) > 0

    test_file = jsp_files[0]

    # Analyze file
    result = analyzer.analyze_file(test_file)

    # Verify result
    assert result is not None
    assert result["status"] == "success"
    assert "form" in result
    assert "rules" in result

    # Verify form
    form = result["form"]
    assert form.name == "userRegistrationForm"
    assert len(form.fields) == 3
    assert form.form_type == FormType.JSP_FORM
    assert form.submission_endpoint == "/api/users"

    # Verify business rules (validation rules from required fields)
    rules = result["rules"]
    assert len(rules) >= 2  # At least email and password validations

    # Verify output files were created
    form_file = temp_output_dir / "frontend" / "forms" / f"{form.name}.json"
    assert form_file.exists()


def test_visit_log_tracking(mock_ollama_client, temp_output_dir, temp_source_dir):
    """Test visit log tracking."""
    analyzer = FrontendAnalyzer(
        ollama_client=mock_ollama_client,
        output_dir=temp_output_dir,
        source_dir=temp_source_dir
    )

    # Initially empty
    assert len(analyzer.visit_log) == 0

    # Find test file
    files = analyzer.find_frontend_files()
    test_file = files[0]

    # Should analyze (not in log)
    assert analyzer._should_analyze_file(test_file) is True

    # Mock successful analysis
    from codeindex.models.prd import FileVisitEntry

    content_hash = analyzer._compute_file_hash(test_file)
    entry = FileVisitEntry(
        file_path=str(test_file),
        timestamp=datetime.now(),
        status=VisitStatus.SUCCESS,
        content_hash=content_hash,
        layer=AnalysisLayer.FRONTEND
    )

    analyzer._append_visit_log(entry)

    # Verify appended
    assert len(analyzer.visit_log) == 1
    assert str(test_file) in analyzer.visit_log

    # Should skip (unchanged file)
    assert analyzer._should_analyze_file(test_file) is False


def test_force_refresh_ignores_visit_log(
    mock_ollama_client,
    temp_output_dir,
    temp_source_dir
):
    """Test that force_refresh re-analyzes all files."""
    # Create analyzer with force_refresh
    analyzer = FrontendAnalyzer(
        ollama_client=mock_ollama_client,
        output_dir=temp_output_dir,
        source_dir=temp_source_dir,
        force_refresh=True
    )

    # Add entry to visit log
    files = analyzer.find_frontend_files()
    test_file = files[0]

    from codeindex.models.prd import FileVisitEntry

    content_hash = analyzer._compute_file_hash(test_file)
    entry = FileVisitEntry(
        file_path=str(test_file),
        timestamp=datetime.now(),
        status=VisitStatus.SUCCESS,
        content_hash=content_hash,
        layer=AnalysisLayer.FRONTEND
    )

    analyzer._append_visit_log(entry)

    # Even with entry in log, should still analyze due to force_refresh
    assert analyzer._should_analyze_file(test_file) is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
