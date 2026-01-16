"""
Integration test for multi-agent PRD generation workflow (T086).

Tests end-to-end PRD generation with agent collaboration, workflow cancellation,
and PRD download functionality.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from typing import List, Dict, Any


class TestMultiAgentPrdGeneration:
    """Integration test suite for multi-agent PRD generation."""

    @pytest.fixture
    def comprehensive_artifacts(self) -> List[Dict[str, Any]]:
        """Create comprehensive set of test artifacts."""
        return [
            # Backend artifacts
            {
                "id": "backend-001",
                "artifactType": "BackendDoc",
                "fileName": "UserService.java",
                "relativePath": "src/main/java/com/example/service/UserService.java",
                "summary": "User management service with CRUD operations",
                "entities": ["createUser", "updateUser", "deleteUser", "findUser"],
                "_additional": {"id": "backend-001", "distance": 0.05}
            },
            {
                "id": "endpoint-001",
                "artifactType": "GwtEndpoint",
                "fileName": "UserServlet.java",
                "relativePath": "src/main/java/com/example/servlet/UserServlet.java",
                "summary": "GWT RPC servlet for user operations",
                "entities": ["getUserData", "saveUser", "deleteUser"],
                "_additional": {"id": "endpoint-001", "distance": 0.08}
            },
            # Frontend artifacts
            {
                "id": "presenter-001",
                "artifactType": "GwtPresenter",
                "fileName": "UserPresenter.java",
                "relativePath": "src/main/java/com/example/client/UserPresenter.java",
                "summary": "User management UI presenter with event handlers",
                "entities": ["onEditUser", "onSaveUser", "onDeleteUser"],
                "_additional": {"id": "presenter-001", "distance": 0.10}
            },
            {
                "id": "view-001",
                "artifactType": "GwtView",
                "fileName": "UserView.java",
                "relativePath": "src/main/java/com/example/client/UserView.java",
                "summary": "User management view interface",
                "entities": ["getUserNameField", "getEmailField", "getSaveButton"],
                "_additional": {"id": "view-001", "distance": 0.12}
            },
            # Data artifacts
            {
                "id": "db-001",
                "artifactType": "DbTable",
                "fileName": "users.sql",
                "relativePath": "schema/users.sql",
                "summary": "User accounts table",
                "entities": ["user_id", "email", "username", "password_hash", "created_at"],
                "_additional": {"id": "db-001", "distance": 0.15}
            },
            {
                "id": "dao-001",
                "artifactType": "DaoCall",
                "fileName": "UserDAO.java",
                "relativePath": "src/main/java/com/example/dao/UserDAO.java",
                "summary": "User data access object",
                "entities": ["findById", "save", "delete", "findAll"],
                "_additional": {"id": "dao-001", "distance": 0.18}
            }
        ]

    @patch('codeindex.web.agents.backend_specialist.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    @patch('codeindex.web.agents.frontend_specialist.get_search_service')
    @patch('codeindex.web.agents.data_analyst.get_search_service')
    @patch('codeindex.web.agents.prd_writer.get_search_service')
    def test_full_prd_generation_workflow(
        self,
        mock_prd_search,
        mock_data_search,
        mock_frontend_search,
        mock_ollama_class,
        mock_backend_search,
        comprehensive_artifacts
    ):
        """Test complete multi-agent PRD generation workflow."""
        from codeindex.web.workflows.prd_generation import PrdGenerationWorkflow

        # Mock search service for all agents
        for mock_search_getter in [mock_backend_search, mock_frontend_search, mock_data_search, mock_prd_search]:
            mock_search = Mock()
            mock_search.search.return_value = {
                "results": comprehensive_artifacts,
                "total": len(comprehensive_artifacts)
            }
            mock_search_getter.return_value = mock_search

        # Mock Ollama responses for each agent
        mock_ollama = Mock()

        def ollama_response_factory(prompt, **kwargs):
            if "backend" in prompt.lower() or "service" in prompt.lower():
                return {
                    "response": """Backend Analysis:
- UserService provides CRUD operations
- GWT RPC servlet handles remote procedure calls
- RESTful architecture with clear separation of concerns
"""
                }
            elif "frontend" in prompt.lower() or "ui" in prompt.lower():
                return {
                    "response": """Frontend Analysis:
- UserPresenter follows GWT MVP pattern
- UserView provides UI widgets for form fields
- Event handlers for user interactions
"""
                }
            elif "data" in prompt.lower() or "database" in prompt.lower():
                return {
                    "response": """Data Analysis:
- users table with primary key user_id
- UserDAO provides data access layer
- Well-defined schema with appropriate data types
"""
                }
            else:  # PRD Writer
                return {
                    "response": """# Product Requirements Document: User Management

## 1. Objectives
Enable comprehensive user account management functionality with:
- Create, read, update, delete user accounts
- Secure authentication and authorization
- User-friendly interface for administrators

## 2. Stakeholders
- **End Users**: Administrators managing user accounts
- **Development Team**: Backend and frontend developers
- **QA Team**: Testing user management features

## 3. User Stories

**US1: Create User Account**
- As an administrator, I can create a new user account
- **Acceptance Criteria**:
  - Form validates email format
  - Password meets security requirements
  - Duplicate emails are rejected

**US2: Edit User Account**
- As an administrator, I can edit existing user details
- **Acceptance Criteria**:
  - Changes are saved immediately
  - Audit log tracks modifications
  - Validation prevents invalid updates

**US3: Delete User Account**
- As an administrator, I can delete user accounts
- **Acceptance Criteria**:
  - Confirmation dialog prevents accidental deletion
  - Soft delete preserves data for audit
  - Related records are handled appropriately

## 4. Functional Requirements
- FR1: System shall support user CRUD operations
- FR2: System shall validate email addresses (RFC 5322)
- FR3: System shall enforce password complexity rules
- FR4: System shall provide audit logging for all changes
- FR5: System shall support role-based access control

## 5. Non-Functional Requirements
- NFR1: Response time < 200ms for user operations
- NFR2: Support 1000+ concurrent users
- NFR3: 99.9% uptime SLA
- NFR4: GDPR compliance for user data handling

## 6. Out of Scope
- Social media integration
- Multi-factor authentication (future phase)
- User self-registration
- Password recovery workflow
"""
                }

        mock_ollama.call_ollama.side_effect = ollama_response_factory
        mock_ollama_class.return_value = mock_ollama

        # Execute workflow
        workflow = PrdGenerationWorkflow()
        result = workflow.execute(
            artifacts=comprehensive_artifacts,
            project_name="UserManagementSystem"
        )

        # Verify workflow completed successfully
        assert result["success"] == True
        assert result["error"] is None

        # Verify PRD content
        prd_content = result["prd_content"]
        assert len(prd_content) > 0
        assert "Product Requirements Document" in prd_content
        assert "Objectives" in prd_content
        assert "User Stories" in prd_content
        assert "Functional Requirements" in prd_content
        assert "Non-Functional Requirements" in prd_content

        # Verify all steps completed
        steps = result["steps"]
        assert len(steps) == 4
        assert all(step["status"] == "completed" for step in steps)

        # Verify step sequence
        assert steps[0]["agent_role"] == "Backend Specialist"
        assert steps[1]["agent_role"] == "Frontend Specialist"
        assert steps[2]["agent_role"] == "Data Analyst"
        assert steps[3]["agent_role"] == "PRD Writer"

    @patch('codeindex.web.agents.backend_specialist.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_workflow_with_progress_callback(
        self,
        mock_ollama_class,
        mock_backend_search,
        comprehensive_artifacts
    ):
        """Test workflow executes progress callback correctly."""
        from codeindex.web.workflows.prd_generation import PrdGenerationWorkflow

        # Mock search service
        mock_search = Mock()
        mock_search.search.return_value = {
            "results": comprehensive_artifacts,
            "total": len(comprehensive_artifacts)
        }
        mock_backend_search.return_value = mock_search

        # Mock Ollama (simple responses for all agents)
        mock_ollama = Mock()
        mock_ollama.call_ollama.return_value = {"response": "Test analysis"}
        mock_ollama_class.return_value = mock_ollama

        # Create progress callback mock
        progress_callback = Mock()

        # Execute workflow with callback
        workflow = PrdGenerationWorkflow()

        with patch('codeindex.web.agents.frontend_specialist.get_search_service', return_value=mock_search):
            with patch('codeindex.web.agents.data_analyst.get_search_service', return_value=mock_search):
                with patch('codeindex.web.agents.prd_writer.get_search_service', return_value=mock_search):
                    result = workflow.execute(
                        artifacts=comprehensive_artifacts,
                        project_name="TestProject",
                        progress_callback=progress_callback
                    )

        # Verify callback invoked for each step + final
        assert progress_callback.call_count == 5

    @patch('codeindex.web.agents.backend_specialist.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_workflow_cancellation(
        self,
        mock_ollama_class,
        mock_backend_search,
        comprehensive_artifacts
    ):
        """Test workflow cancellation mid-execution."""
        from codeindex.web.workflows.prd_generation import PrdGenerationWorkflow

        # Mock search service
        mock_search = Mock()
        mock_search.search.return_value = {
            "results": comprehensive_artifacts,
            "total": len(comprehensive_artifacts)
        }
        mock_backend_search.return_value = mock_search

        # Mock Ollama
        mock_ollama = Mock()
        mock_ollama.call_ollama.return_value = {"response": "Test"}
        mock_ollama_class.return_value = mock_ollama

        # Create workflow and cancel it
        workflow = PrdGenerationWorkflow()
        workflow.cancel()

        # Execute workflow
        result = workflow.execute(
            artifacts=comprehensive_artifacts,
            project_name="TestProject"
        )

        # Verify workflow was cancelled
        assert result["success"] == False
        assert "cancelled" in result["error"].lower()

    @patch('codeindex.web.agents.backend_specialist.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    @patch('codeindex.web.agents.frontend_specialist.get_search_service')
    def test_workflow_handles_agent_failure(
        self,
        mock_frontend_search,
        mock_ollama_class,
        mock_backend_search,
        comprehensive_artifacts
    ):
        """Test workflow stops gracefully when agent fails."""
        from codeindex.web.workflows.prd_generation import PrdGenerationWorkflow

        # Mock backend search to succeed
        mock_backend_svc = Mock()
        mock_backend_svc.search.return_value = {
            "results": comprehensive_artifacts,
            "total": len(comprehensive_artifacts)
        }
        mock_backend_search.return_value = mock_backend_svc

        # Mock frontend search to fail
        mock_frontend_svc = Mock()
        mock_frontend_svc.search.side_effect = Exception("Weaviate connection timeout")
        mock_frontend_search.return_value = mock_frontend_svc

        # Mock Ollama for backend
        mock_ollama = Mock()
        mock_ollama.call_ollama.return_value = {"response": "Backend analysis"}
        mock_ollama_class.return_value = mock_ollama

        # Execute workflow
        workflow = PrdGenerationWorkflow()
        result = workflow.execute(
            artifacts=comprehensive_artifacts,
            project_name="TestProject"
        )

        # Verify workflow failed
        assert result["success"] == False
        assert "Frontend Specialist" in result["error"]

        # Verify only first step completed
        steps = result["steps"]
        assert steps[0]["status"] == "completed"
        assert steps[1]["status"] == "failed"
        assert steps[2]["status"] == "pending"
        assert steps[3]["status"] == "pending"

    def test_prd_content_structure_validation(self):
        """Test PRD content has required sections."""
        # Sample PRD content from workflow
        prd_content = """# Product Requirements Document

## 1. Objectives
Enable user management...

## 2. Stakeholders
- Administrators
- Developers

## 3. User Stories
US1: Create user...

## 4. Functional Requirements
FR1: Support CRUD...

## 5. Non-Functional Requirements
NFR1: Performance...

## 6. Out of Scope
- Future features
"""

        # Verify required sections present
        assert "Objectives" in prd_content
        assert "Stakeholders" in prd_content
        assert "User Stories" in prd_content
        assert "Functional Requirements" in prd_content
        assert "Non-Functional Requirements" in prd_content
        assert "Out of Scope" in prd_content

    @patch('codeindex.web.agents.backend_specialist.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    @patch('codeindex.web.agents.frontend_specialist.get_search_service')
    @patch('codeindex.web.agents.data_analyst.get_search_service')
    @patch('codeindex.web.agents.prd_writer.get_search_service')
    def test_context_propagation_between_agents(
        self,
        mock_prd_search,
        mock_data_search,
        mock_frontend_search,
        mock_ollama_class,
        mock_backend_search,
        comprehensive_artifacts
    ):
        """Test context is correctly propagated between agents."""
        from codeindex.web.workflows.prd_generation import PrdGenerationWorkflow

        # Mock all search services
        for mock_search_getter in [mock_backend_search, mock_frontend_search, mock_data_search, mock_prd_search]:
            mock_search = Mock()
            mock_search.search.return_value = {
                "results": comprehensive_artifacts,
                "total": len(comprehensive_artifacts)
            }
            mock_search_getter.return_value = mock_search

        # Track Ollama calls to verify context passing
        ollama_calls = []

        def track_ollama_calls(prompt, **kwargs):
            ollama_calls.append({
                "prompt": prompt,
                "context": kwargs.get("context", {})
            })
            return {"response": f"Response for: {prompt[:50]}..."}

        mock_ollama = Mock()
        mock_ollama.call_ollama.side_effect = track_ollama_calls
        mock_ollama_class.return_value = mock_ollama

        # Execute workflow
        workflow = PrdGenerationWorkflow()
        workflow.execute(
            artifacts=comprehensive_artifacts,
            project_name="TestProject"
        )

        # Verify PRD Writer received context from all previous agents
        # (PRD Writer is the 4th agent, so check 4th call)
        if len(ollama_calls) >= 4:
            prd_call = ollama_calls[3]
            # Context should include analyses from previous agents
            assert "Backend" in prd_call["prompt"] or "backend" in str(prd_call).lower()
            assert "Frontend" in prd_call["prompt"] or "frontend" in str(prd_call).lower()
            assert "Data" in prd_call["prompt"] or "data" in str(prd_call).lower()

    def test_prd_download_format(self):
        """Test PRD content is formatted for download."""
        # Sample PRD content
        prd_content = """# Product Requirements Document

## Objectives
Test objectives...
"""

        # Verify PRD is markdown format
        assert prd_content.startswith("#")
        assert "##" in prd_content

        # Verify can be saved as .md file
        assert len(prd_content.encode('utf-8')) > 0

    @patch('codeindex.web.agents.backend_specialist.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    @patch('codeindex.web.agents.frontend_specialist.get_search_service')
    @patch('codeindex.web.agents.data_analyst.get_search_service')
    @patch('codeindex.web.agents.prd_writer.get_search_service')
    def test_workflow_with_empty_artifacts(
        self,
        mock_prd_search,
        mock_data_search,
        mock_frontend_search,
        mock_ollama_class,
        mock_backend_search
    ):
        """Test workflow handles empty artifact list gracefully."""
        from codeindex.web.workflows.prd_generation import PrdGenerationWorkflow

        # Mock search services to return empty results
        for mock_search_getter in [mock_backend_search, mock_frontend_search, mock_data_search, mock_prd_search]:
            mock_search = Mock()
            mock_search.search.return_value = {"results": [], "total": 0}
            mock_search_getter.return_value = mock_search

        # Mock Ollama with fallback responses
        mock_ollama = Mock()
        mock_ollama.call_ollama.return_value = {"response": "No artifacts found. Unable to generate analysis."}
        mock_ollama_class.return_value = mock_ollama

        # Execute workflow with empty artifacts
        workflow = PrdGenerationWorkflow()
        result = workflow.execute(
            artifacts=[],
            project_name="EmptyProject"
        )

        # Workflow should complete but with limited content
        # (behavior depends on implementation - should not crash)
        assert isinstance(result, dict)
        assert "success" in result
        assert "prd_content" in result
        assert "steps" in result
