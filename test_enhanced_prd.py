#!/usr/bin/env python
"""
Quick validation test for enhanced PRD generation functions.

This script creates sample data models and calls the PRD generation
functions to verify they produce valid markdown without errors.
"""
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from codeindex.models.prd import (
    DatabaseEntity, Column, ForeignKey, Index, SourceType,
    BusinessRule, RuleLayer, RuleScope, RuleType, RuleSeverity,
    ServiceDefinition, ServiceOperation, Parameter, ServiceType, ServiceDependency,
    APIEndpoint, HTTPMethod, RequestFormat, ResponseFormat, StatusCode, EndpointParameter,
    FormDefinition, FormField, FormType,
    UIComponent, ComponentType, Event, DataBinding,
)

# Import the PRD generation functions by reading from the prd.py module
from codeindex.cli.prd import _generate_database_prd, _generate_service_prd, _generate_frontend_prd


def test_database_prd():
    """Test database PRD generation with sample data."""
    print("Testing database PRD generation...")

    # Create sample database entities
    entities = [
        DatabaseEntity(
            id="users",
            name="users",
            qualified_name="public.users",
            source_type=SourceType.JPA_ANNOTATION,
            source_files=["src/model/User.java"],
            columns=[
                Column(name="id", data_type="BIGINT", nullable=False, description="Primary key"),
                Column(name="username", data_type="VARCHAR(50)", nullable=False, description="Login username"),
                Column(name="email", data_type="VARCHAR(100)", nullable=False, description="User email"),
                Column(name="created_at", data_type="TIMESTAMP", nullable=False, default_value="CURRENT_TIMESTAMP"),
            ],
            primary_key=["id"],
            foreign_keys=[],
            indexes=[
                Index(name="idx_username", columns=["username"], unique=True),
                Index(name="idx_email", columns=["email"], unique=True),
            ],
            description="User account information",
            estimated_row_count="medium",
            domain="Authentication",
            created_at=datetime.now(),
        ),
        DatabaseEntity(
            id="orders",
            name="orders",
            qualified_name="public.orders",
            source_type=SourceType.JPA_ANNOTATION,
            source_files=["src/model/Order.java"],
            columns=[
                Column(name="id", data_type="BIGINT", nullable=False, description="Primary key"),
                Column(name="user_id", data_type="BIGINT", nullable=False, description="User who placed order"),
                Column(name="total_amount", data_type="DECIMAL(10,2)", nullable=False, description="Order total"),
                Column(name="status", data_type="VARCHAR(20)", nullable=False, description="Order status"),
                Column(name="created_at", data_type="TIMESTAMP", nullable=False, default_value="CURRENT_TIMESTAMP"),
            ],
            primary_key=["id"],
            foreign_keys=[
                ForeignKey(
                    column_name="user_id",
                    referenced_table="users",
                    referenced_column="id",
                    on_delete="CASCADE",
                ),
            ],
            indexes=[
                Index(name="idx_user_id", columns=["user_id"], unique=False),
                Index(name="idx_status", columns=["status"], unique=False),
            ],
            description="Customer orders",
            estimated_row_count="large",
            domain="Commerce",
            created_at=datetime.now(),
        ),
    ]

    # Create sample business rules
    rules = [
        BusinessRule(
            id="BR001",
            name="Email Format Validation",
            layer=RuleLayer.DATABASE,
            scope=RuleScope.FIELD,
            rule_type=RuleType.VALIDATION,
            description="Email addresses must follow standard RFC 5322 format",
            source_files=["src/model/User.java"],
            severity=RuleSeverity.HIGH,
            security_relevant=False,
            domain="Authentication",
            created_at=datetime.now(),
        ),
        BusinessRule(
            id="BR002",
            name="Order Total Positive",
            layer=RuleLayer.SERVICE,
            scope=RuleScope.ENTITY,
            rule_type=RuleType.CONSTRAINT,
            description="Order total amount must be greater than zero",
            source_files=["src/service/OrderService.java"],
            severity=RuleSeverity.CRITICAL,
            security_relevant=False,
            domain="Commerce",
            created_at=datetime.now(),
        ),
    ]

    # Generate PRD
    prd_content = _generate_database_prd(entities, rules)

    # Basic validation
    assert len(prd_content) > 0, "Database PRD should not be empty"
    assert "# Database Schema Documentation" in prd_content
    assert "## Table of Contents" in prd_content
    assert "## Overview" in prd_content
    assert "## Entity Catalog" in prd_content
    assert "## Relationships" in prd_content
    assert "## Business Rules" in prd_content
    assert "users" in prd_content
    assert "orders" in prd_content
    assert "Authentication" in prd_content
    assert "Commerce" in prd_content

    print(f"✓ Database PRD generated successfully ({len(prd_content)} chars)")
    return True


def test_service_prd():
    """Test service PRD generation with sample data."""
    print("Testing service PRD generation...")

    # Create sample services
    services = [
        ServiceDefinition(
            id="com.example.service.UserService",
            class_name="UserService",
            qualified_name="com.example.service.UserService",
            package="com.example.service",
            source_file="src/service/UserService.java",
            service_type=ServiceType.BUSINESS_SERVICE,
            operations=[
                ServiceOperation(
                    name="createUser",
                    signature="createUser(UserDTO userDTO)",
                    return_type="User",
                    parameters=[
                        Parameter(name="userDTO", type="UserDTO", description="User data"),
                    ],
                    description="Creates a new user account",
                    annotations=["@Transactional"],
                ),
                ServiceOperation(
                    name="getUserById",
                    signature="getUserById(Long id)",
                    return_type="User",
                    parameters=[
                        Parameter(name="id", type="Long", description="User ID"),
                    ],
                    description="Retrieves user by ID",
                    annotations=["@Transactional(readOnly=true)"],
                ),
            ],
            description="User account management service",
            dependencies=[
                ServiceDependency(
                    target_service="UserRepository",
                    dependency_type="injection",
                    injection_method="constructor",
                ),
            ],
            data_dependencies=["users"],
            frameworks=["Spring"],
            domain="Authentication",
            created_at=datetime.now(),
        ),
    ]

    # Create sample endpoints
    endpoints = [
        APIEndpoint(
            id="POST:/api/users",
            http_method=HTTPMethod.POST,
            path="/api/users",
            service_id="com.example.service.UserService",
            operation_name="createUser",
            source_file="src/controller/UserController.java",
            description="Create a new user account",
            authentication_required=True,
            authorization_roles=["ADMIN"],
            produces=["application/json"],
            consumes=["application/json"],
            created_at=datetime.now(),
        ),
        APIEndpoint(
            id="GET:/api/users/{id}",
            http_method=HTTPMethod.GET,
            path="/api/users/{id}",
            service_id="com.example.service.UserService",
            operation_name="getUserById",
            source_file="src/controller/UserController.java",
            description="Get user by ID",
            authentication_required=True,
            authorization_roles=["USER", "ADMIN"],
            produces=["application/json"],
            created_at=datetime.now(),
        ),
    ]

    # Generate PRD
    prd_content = _generate_service_prd(services, endpoints)

    # Basic validation
    assert len(prd_content) > 0, "Service PRD should not be empty"
    assert "# Backend Services Documentation" in prd_content
    assert "## Table of Contents" in prd_content
    assert "## Overview" in prd_content
    assert "## Service Catalog" in prd_content
    assert "## API Endpoints" in prd_content
    assert "UserService" in prd_content
    assert "/api/users" in prd_content

    print(f"✓ Service PRD generated successfully ({len(prd_content)} chars)")
    return True


def test_frontend_prd():
    """Test frontend PRD generation with sample data."""
    print("Testing frontend PRD generation...")

    # Create sample forms
    forms = [
        FormDefinition(
            id="login_form",
            name="LoginForm",
            source_file="src/webapp/login.jsp",
            form_type=FormType.JSP_FORM,
            fields=[
                FormField(
                    name="username",
                    type="text",
                    required=True,
                    label="Username",
                    validation_pattern="^[a-zA-Z0-9_]{3,20}$",
                    validation_message="Username must be 3-20 alphanumeric characters",
                ),
                FormField(
                    name="password",
                    type="password",
                    required=True,
                    label="Password",
                    validation_pattern="^.{8,}$",
                    validation_message="Password must be at least 8 characters",
                ),
            ],
            description="User login form",
            submission_endpoint="/api/auth/login",
            submission_method="POST",
            submission_service="AuthService",
            bound_entities=["users"],
            navigation_on_success="/dashboard",
            navigation_on_cancel="/",
            security_patterns=["CSRF Protection", "SSL Required"],
            domain="Authentication",
            created_at=datetime.now(),
        ),
    ]

    # Create sample components
    components = [
        UIComponent(
            id="com.example.client.LoginPanel",
            name="LoginPanel",
            component_type=ComponentType.GWT_WIDGET,
            source_file="src/client/LoginPanel.java",
            description="Login panel widget",
            responsibilities=["Display login form", "Handle authentication", "Show error messages"],
            events_handled=[
                Event(name="onLoginClick", type="click", handler="handleLogin"),
            ],
            related_forms=["login_form"],
            domain="Authentication",
            created_at=datetime.now(),
        ),
    ]

    # Generate PRD
    prd_content = _generate_frontend_prd(forms, components)

    # Basic validation
    assert len(prd_content) > 0, "Frontend PRD should not be empty"
    assert "# Frontend Documentation" in prd_content
    assert "## Table of Contents" in prd_content
    assert "## Overview" in prd_content
    assert "## Form Catalog" in prd_content
    assert "## UI Components" in prd_content
    assert "LoginForm" in prd_content
    assert "LoginPanel" in prd_content

    print(f"✓ Frontend PRD generated successfully ({len(prd_content)} chars)")
    return True


def main():
    """Run all tests."""
    print("=" * 70)
    print("Testing Enhanced PRD Generation Functions")
    print("=" * 70)
    print()

    try:
        # Test database PRD
        test_database_prd()
        print()

        # Test service PRD
        test_service_prd()
        print()

        # Test frontend PRD
        test_frontend_prd()
        print()

        print("=" * 70)
        print("✓ All tests passed!")
        print("=" * 70)
        return 0

    except Exception as e:
        print()
        print("=" * 70)
        print(f"✗ Test failed: {e}")
        print("=" * 70)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
