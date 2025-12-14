"""
Unit tests for Service Analyzer Service.
"""
import json
import pytest
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock

from codeindex.models.prd import (
    ServiceDefinition,
    ServiceOperation,
    Parameter,
    ServiceDependency,
    TransactionInfo,
    APIEndpoint,
    HTTPMethod,
    RequestFormat,
    ResponseFormat,
    ServiceType,
    VisitStatus,
    AnalysisLayer,
)
from codeindex.services.service_analyzer import ServiceAnalyzer


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

    # Create a sample service file
    service_file = source_dir / "UserService.java"
    service_file.write_text("""
package com.example.service;

import org.springframework.stereotype.Service;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.transaction.annotation.Transactional;

@Service
public class UserService {

    @Autowired
    private UserDAO userDAO;

    @Transactional
    public User createUser(UserDTO dto) throws ValidationException {
        // Create user logic
        return userDAO.save(user);
    }

    public User findById(Long id) {
        return userDAO.findById(id);
    }
}
""", encoding="utf-8")

    # Create a sample REST controller file
    controller_file = source_dir / "UserController.java"
    controller_file.write_text("""
package com.example.controller;

import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/users")
public class UserController {

    @Autowired
    private UserService userService;

    @GetMapping("/{id}")
    public User getUser(@PathVariable Long id) {
        return userService.findById(id);
    }

    @PostMapping
    public User createUser(@RequestBody UserDTO dto) {
        return userService.createUser(dto);
    }
}
""", encoding="utf-8")

    return source_dir


@pytest.fixture
def sample_service_llm_response():
    """Sample LLM response for service extraction."""
    return {
        "response": json.dumps({
            "class_name": "UserService",
            "qualified_name": "com.example.service.UserService",
            "service_type": "business_service",
            "description": "Manages user account lifecycle including registration, authentication, and profile updates. Coordinates with UserDAO for persistence.",
            "operations": [
                {
                    "name": "createUser",
                    "signature": "public User createUser(UserDTO dto) throws ValidationException",
                    "return_type": "User",
                    "parameters": [
                        {
                            "name": "dto",
                            "type": "UserDTO",
                            "description": "User registration data"
                        }
                    ],
                    "description": "Creates a new user account after validation",
                    "throws": ["ValidationException"],
                    "annotations": ["@Transactional"],
                    "line_number": 12
                },
                {
                    "name": "findById",
                    "signature": "public User findById(Long id)",
                    "return_type": "User",
                    "parameters": [
                        {
                            "name": "id",
                            "type": "Long",
                            "description": "User ID"
                        }
                    ],
                    "description": "Finds user by ID",
                    "throws": [],
                    "annotations": [],
                    "line_number": 18
                }
            ],
            "dependencies": [
                {
                    "target_service": "UserDAO",
                    "dependency_type": "injection",
                    "injection_method": "field"
                }
            ],
            "data_dependencies": ["user"],
            "business_rules": [
                {
                    "name": "User Validation",
                    "description": "Validate user data before creation",
                    "enforcement": "ValidationException thrown on invalid data"
                }
            ],
            "transaction_boundaries": [
                {
                    "method_name": "createUser",
                    "transaction_type": "REQUIRED",
                    "propagation": None,
                    "isolation_level": None,
                    "read_only": False
                }
            ],
            "frameworks": ["Spring"],
            "domain": "user_management"
        })
    }


# ==============================================================================
# Model Tests
# ==============================================================================

def test_parameter_creation():
    """Test Parameter model creation."""
    param = Parameter(
        name="id",
        type="Long",
        description="User ID"
    )

    assert param.name == "id"
    assert param.type == "Long"
    assert param.description == "User ID"

    # Test to_dict
    param_dict = param.to_dict()
    assert param_dict["name"] == "id"

    # Test from_dict
    param2 = Parameter.from_dict(param_dict)
    assert param2.name == param.name


def test_service_operation_creation():
    """Test ServiceOperation model creation."""
    operation = ServiceOperation(
        name="createUser",
        signature="public User createUser(UserDTO dto)",
        return_type="User",
        parameters=[Parameter(name="dto", type="UserDTO")],
        description="Creates a new user",
        throws=["ValidationException"],
        annotations=["@Transactional"],
        line_number=42
    )

    assert operation.name == "createUser"
    assert operation.return_type == "User"
    assert len(operation.parameters) == 1
    assert operation.line_number == 42

    # Test to_dict
    op_dict = operation.to_dict()
    assert op_dict["name"] == "createUser"
    assert len(op_dict["parameters"]) == 1

    # Test from_dict
    op2 = ServiceOperation.from_dict(op_dict)
    assert op2.name == operation.name
    assert len(op2.parameters) == len(operation.parameters)


def test_service_definition_creation():
    """Test ServiceDefinition model creation."""
    service = ServiceDefinition(
        id="com.example.UserService",
        class_name="UserService",
        qualified_name="com.example.UserService",
        package="com.example",
        source_file="/path/to/UserService.java",
        service_type=ServiceType.BUSINESS_SERVICE,
        operations=[
            ServiceOperation(
                name="createUser",
                signature="public User createUser(UserDTO dto)",
                return_type="User"
            )
        ],
        created_at=datetime.now()
    )

    assert service.id == "com.example.UserService"
    assert service.class_name == "UserService"
    assert service.service_type == ServiceType.BUSINESS_SERVICE
    assert len(service.operations) == 1

    # Test to_dict
    service_dict = service.to_dict()
    assert service_dict["id"] == "com.example.UserService"
    assert len(service_dict["operations"]) == 1

    # Test from_dict
    service2 = ServiceDefinition.from_dict(service_dict)
    assert service2.id == service.id
    assert len(service2.operations) == len(service.operations)


def test_service_definition_validation():
    """Test ServiceDefinition validation."""
    # Missing required fields
    with pytest.raises(ValueError, match="id is required"):
        ServiceDefinition(
            id="",
            class_name="UserService",
            qualified_name="com.example.UserService",
            package="com.example",
            source_file="/path/to/UserService.java",
            service_type=ServiceType.BUSINESS_SERVICE,
            operations=[ServiceOperation(name="test", signature="test", return_type="void")],
            created_at=datetime.now()
        )

    # No operations
    with pytest.raises(ValueError, match="operations is required"):
        ServiceDefinition(
            id="com.example.UserService",
            class_name="UserService",
            qualified_name="com.example.UserService",
            package="com.example",
            source_file="/path/to/UserService.java",
            service_type=ServiceType.BUSINESS_SERVICE,
            operations=[],
            created_at=datetime.now()
        )


def test_api_endpoint_creation():
    """Test APIEndpoint model creation."""
    endpoint = APIEndpoint(
        id="GET:/api/users/{id}",
        http_method=HTTPMethod.GET,
        path="/api/users/{id}",
        service_id="com.example.UserController",
        operation_name="getUser",
        source_file="/path/to/UserController.java",
        description="Get user by ID",
        authentication_required=True,
        created_at=datetime.now()
    )

    assert endpoint.id == "GET:/api/users/{id}"
    assert endpoint.http_method == HTTPMethod.GET
    assert endpoint.path == "/api/users/{id}"
    assert endpoint.authentication_required is True

    # Test to_dict
    endpoint_dict = endpoint.to_dict()
    assert endpoint_dict["http_method"] == "GET"
    assert endpoint_dict["path"] == "/api/users/{id}"

    # Test from_dict
    endpoint2 = APIEndpoint.from_dict(endpoint_dict)
    assert endpoint2.id == endpoint.id
    assert endpoint2.http_method == endpoint.http_method


# ==============================================================================
# Service Analyzer Tests
# ==============================================================================

def test_service_analyzer_init(mock_ollama_client, temp_output_dir, temp_source_dir):
    """Test ServiceAnalyzer initialization."""
    analyzer = ServiceAnalyzer(
        ollama_client=mock_ollama_client,
        output_dir=temp_output_dir,
        source_dir=temp_source_dir
    )

    assert analyzer.output_dir == temp_output_dir
    assert analyzer.source_dir == temp_source_dir
    assert analyzer.max_workers == 10
    assert analyzer.services_dir.exists()
    assert analyzer.endpoints_dir.exists()


def test_find_service_files(mock_ollama_client, temp_output_dir, temp_source_dir):
    """Test finding service files."""
    analyzer = ServiceAnalyzer(
        ollama_client=mock_ollama_client,
        output_dir=temp_output_dir,
        source_dir=temp_source_dir
    )

    files = analyzer.find_service_files()

    # Should find UserService.java and UserController.java
    assert len(files) >= 2
    assert any("UserService.java" in str(f) for f in files)
    assert any("UserController.java" in str(f) for f in files)


def test_detect_service_type(mock_ollama_client, temp_output_dir, temp_source_dir):
    """Test service type detection."""
    analyzer = ServiceAnalyzer(
        ollama_client=mock_ollama_client,
        output_dir=temp_output_dir,
        source_dir=temp_source_dir
    )

    # Business Service
    service_content = "@Service\\npublic class UserService {}"
    assert analyzer._detect_service_type(service_content, "UserService.java") == "Business Service"

    # REST Controller
    controller_content = "@RestController\\npublic class UserController {}"
    assert analyzer._detect_service_type(controller_content, "UserController.java") == "REST Controller"

    # DAO Service
    dao_content = "@Repository\\npublic class UserDAO {}"
    assert analyzer._detect_service_type(dao_content, "UserDAO.java") == "DAO Service"


def test_compute_file_hash(mock_ollama_client, temp_output_dir, temp_source_dir):
    """Test file hash computation."""
    analyzer = ServiceAnalyzer(
        ollama_client=mock_ollama_client,
        output_dir=temp_output_dir,
        source_dir=temp_source_dir
    )

    # Find a test file
    files = analyzer.find_service_files()
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
    sample_service_llm_response
):
    """Test analyzing a single file with mocked LLM."""
    # Mock LLM response
    mock_ollama_client.call_ollama.return_value = sample_service_llm_response

    analyzer = ServiceAnalyzer(
        ollama_client=mock_ollama_client,
        output_dir=temp_output_dir,
        source_dir=temp_source_dir
    )

    # Find test file
    files = analyzer.find_service_files()
    service_files = [f for f in files if "UserService.java" in str(f)]
    assert len(service_files) > 0

    test_file = service_files[0]

    # Analyze file
    result = analyzer.analyze_file(test_file)

    # Verify result
    assert result is not None
    assert result["status"] == "success"
    assert "service" in result
    assert "rules" in result

    # Verify service
    service = result["service"]
    assert service.class_name == "UserService"
    assert len(service.operations) == 2
    assert len(service.dependencies) == 1
    assert service.service_type == ServiceType.BUSINESS_SERVICE

    # Verify business rules
    rules = result["rules"]
    assert len(rules) == 1
    assert rules[0].name == "User Validation"

    # Verify output files were created
    service_file = temp_output_dir / "services" / "definitions" / "UserService.json"
    assert service_file.exists()


def test_visit_log_tracking(mock_ollama_client, temp_output_dir, temp_source_dir):
    """Test visit log tracking."""
    analyzer = ServiceAnalyzer(
        ollama_client=mock_ollama_client,
        output_dir=temp_output_dir,
        source_dir=temp_source_dir
    )

    # Initially empty
    assert len(analyzer.visit_log) == 0

    # Find test file
    files = analyzer.find_service_files()
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
        layer=AnalysisLayer.SERVICE
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
    analyzer = ServiceAnalyzer(
        ollama_client=mock_ollama_client,
        output_dir=temp_output_dir,
        source_dir=temp_source_dir,
        force_refresh=True
    )

    # Add entry to visit log
    files = analyzer.find_service_files()
    test_file = files[0]

    from codeindex.models.prd import FileVisitEntry

    content_hash = analyzer._compute_file_hash(test_file)
    entry = FileVisitEntry(
        file_path=str(test_file),
        timestamp=datetime.now(),
        status=VisitStatus.SUCCESS,
        content_hash=content_hash,
        layer=AnalysisLayer.SERVICE
    )

    analyzer._append_visit_log(entry)

    # Even with entry in log, should still analyze due to force_refresh
    assert analyzer._should_analyze_file(test_file) is True


def test_http_method_extraction(mock_ollama_client, temp_output_dir, temp_source_dir):
    """Test HTTP method extraction from annotations."""
    analyzer = ServiceAnalyzer(
        ollama_client=mock_ollama_client,
        output_dir=temp_output_dir,
        source_dir=temp_source_dir
    )

    assert analyzer._extract_http_method("@GetMapping") == HTTPMethod.GET
    assert analyzer._extract_http_method("@PostMapping") == HTTPMethod.POST
    assert analyzer._extract_http_method("@PutMapping") == HTTPMethod.PUT
    assert analyzer._extract_http_method("@DeleteMapping") == HTTPMethod.DELETE
    assert analyzer._extract_http_method('@RequestMapping(method = RequestMethod.GET)') == HTTPMethod.GET


def test_path_extraction(mock_ollama_client, temp_output_dir, temp_source_dir):
    """Test path extraction from annotations."""
    analyzer = ServiceAnalyzer(
        ollama_client=mock_ollama_client,
        output_dir=temp_output_dir,
        source_dir=temp_source_dir
    )

    assert analyzer._extract_path('@GetMapping("/users")', "getUsers") == "/users"
    assert analyzer._extract_path('@RequestMapping(value = "/api/users")', "getUsers") == "/api/users"
    assert analyzer._extract_path('@PostMapping(path = "/users")', "createUser") == "/users"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
