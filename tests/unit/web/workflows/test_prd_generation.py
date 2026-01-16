"""
Unit tests for PRD generation workflow orchestration (T084).

Tests sequential workflow execution, agent context passing, and
CrewAI process configuration.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock, call
from typing import List, Dict, Any


class TestPrdGenerationWorkflow:
    """Test suite for PRD generation workflow."""

    @pytest.fixture
    def workflow(self):
        """Create workflow instance."""
        from codeindex.web.workflows.prd_generation import PrdGenerationWorkflow

        return PrdGenerationWorkflow()

    @pytest.fixture
    def mock_artifacts(self) -> List[Dict[str, Any]]:
        """Create mock artifacts for workflow."""
        return [
            {
                "id": "backend-001",
                "artifactType": "BackendDoc",
                "fileName": "UserService.java",
                "summary": "User service"
            },
            {
                "id": "frontend-001",
                "artifactType": "GwtPresenter",
                "fileName": "UserPresenter.java",
                "summary": "User presenter"
            },
            {
                "id": "db-001",
                "artifactType": "DbTable",
                "fileName": "users.sql",
                "summary": "Users table"
            }
        ]

    @pytest.fixture
    def mock_agent_response(self):
        """Create mock agent response."""
        from codeindex.web.agents.base import AgentResponse, AgentRole, Citation

        def create_response(agent_role, content):
            return AgentResponse(
                agent_role=agent_role,
                query="Test query",
                timestamp="2024-01-01T00:00:00",
                duration_seconds=1.5,
                response_text=content,
                citations=[
                    Citation(
                        artifact_id="test-001",
                        file_path="test.java",
                        artifact_type="BackendDoc",
                        confidence=0.9
                    )
                ],
                confidence=0.85,
                suggested_questions=["Q1", "Q2"]
            )

        return create_response

    def test_workflow_initialization(self, workflow):
        """Test workflow initializes with correct steps."""
        from codeindex.web.agents.base import AgentRole

        assert len(workflow.steps) == 4
        assert workflow.steps[0].agent_role == AgentRole.BACKEND_SPECIALIST
        assert workflow.steps[1].agent_role == AgentRole.FRONTEND_SPECIALIST
        assert workflow.steps[2].agent_role == AgentRole.DATA_ANALYST
        assert workflow.steps[3].agent_role == AgentRole.PRD_WRITER

        # All steps should start as pending
        assert all(step.status == "pending" for step in workflow.steps)

    def test_workflow_initialization_context(self, workflow):
        """Test workflow initializes with empty context."""
        assert workflow.context == {}
        assert workflow.is_cancelled == False

    @patch('codeindex.web.workflows.prd_generation.get_backend_specialist_agent')
    @patch('codeindex.web.workflows.prd_generation.get_frontend_specialist_agent')
    @patch('codeindex.web.workflows.prd_generation.get_data_analyst_agent')
    @patch('codeindex.web.workflows.prd_generation.get_prd_writer_agent')
    def test_execute_sequential_workflow(
        self,
        mock_prd_writer,
        mock_data_analyst,
        mock_frontend,
        mock_backend,
        workflow,
        mock_artifacts,
        mock_agent_response
    ):
        """Test sequential execution of workflow steps."""
        from codeindex.web.agents.base import AgentRole

        # Mock each agent
        mock_backend_agent = Mock()
        mock_backend_agent.execute_query.return_value = mock_agent_response(
            AgentRole.BACKEND_SPECIALIST,
            "Backend analysis complete"
        )
        mock_backend.return_value = mock_backend_agent

        mock_frontend_agent = Mock()
        mock_frontend_agent.execute_query.return_value = mock_agent_response(
            AgentRole.FRONTEND_SPECIALIST,
            "Frontend analysis complete"
        )
        mock_frontend.return_value = mock_frontend_agent

        mock_data_agent = Mock()
        mock_data_agent.execute_query.return_value = mock_agent_response(
            AgentRole.DATA_ANALYST,
            "Data analysis complete"
        )
        mock_data_analyst.return_value = mock_data_agent

        mock_prd_agent = Mock()
        mock_prd_agent.execute_query.return_value = mock_agent_response(
            AgentRole.PRD_WRITER,
            "# PRD Document\n\nComprehensive PRD generated..."
        )
        mock_prd_writer.return_value = mock_prd_agent

        # Execute workflow
        result = workflow.execute(mock_artifacts, "TestProject")

        # Verify success
        assert result["success"] == True
        assert "PRD Document" in result["prd_content"]
        assert result["error"] is None

        # Verify all agents were called
        assert mock_backend_agent.execute_query.called
        assert mock_frontend_agent.execute_query.called
        assert mock_data_agent.execute_query.called
        assert mock_prd_agent.execute_query.called

        # Verify all steps completed
        assert all(step.status == "completed" for step in workflow.steps)

    @patch('codeindex.web.workflows.prd_generation.get_backend_specialist_agent')
    @patch('codeindex.web.workflows.prd_generation.get_frontend_specialist_agent')
    @patch('codeindex.web.workflows.prd_generation.get_data_analyst_agent')
    @patch('codeindex.web.workflows.prd_generation.get_prd_writer_agent')
    def test_context_passing_between_agents(
        self,
        mock_prd_writer,
        mock_data_analyst,
        mock_frontend,
        mock_backend,
        workflow,
        mock_artifacts,
        mock_agent_response
    ):
        """Test context is passed correctly between agents."""
        from codeindex.web.agents.base import AgentRole

        # Mock agents
        mock_backend_agent = Mock()
        mock_backend_agent.execute_query.return_value = mock_agent_response(
            AgentRole.BACKEND_SPECIALIST,
            "Backend: UserService with CRUD operations"
        )
        mock_backend.return_value = mock_backend_agent

        mock_frontend_agent = Mock()
        mock_frontend_agent.execute_query.return_value = mock_agent_response(
            AgentRole.FRONTEND_SPECIALIST,
            "Frontend: UserPresenter with event handlers"
        )
        mock_frontend.return_value = mock_frontend_agent

        mock_data_agent = Mock()
        mock_data_agent.execute_query.return_value = mock_agent_response(
            AgentRole.DATA_ANALYST,
            "Data: users table with email column"
        )
        mock_data_analyst.return_value = mock_data_agent

        mock_prd_agent = Mock()
        mock_prd_agent.execute_query.return_value = mock_agent_response(
            AgentRole.PRD_WRITER,
            "PRD generated from all analyses"
        )
        mock_prd_writer.return_value = mock_prd_agent

        # Execute workflow
        workflow.execute(mock_artifacts, "TestProject")

        # Verify context contains all agent analyses
        assert "Backend Specialist_analysis" in workflow.context
        assert "Frontend Specialist_analysis" in workflow.context
        assert "Data Analyst_analysis" in workflow.context

        # Verify PRD Writer received context from all previous agents
        prd_call_args = mock_prd_agent.execute_query.call_args
        query = prd_call_args[0][0]
        context = prd_call_args[1]["context"]

        # Context should include previous analyses
        assert "Backend Specialist_analysis" in context
        assert "Frontend Specialist_analysis" in context
        assert "Data Analyst_analysis" in context

    @patch('codeindex.web.workflows.prd_generation.get_backend_specialist_agent')
    @patch('codeindex.web.workflows.prd_generation.get_frontend_specialist_agent')
    @patch('codeindex.web.workflows.prd_generation.get_data_analyst_agent')
    @patch('codeindex.web.workflows.prd_generation.get_prd_writer_agent')
    def test_progress_callback_invoked(
        self,
        mock_prd_writer,
        mock_data_analyst,
        mock_frontend,
        mock_backend,
        workflow,
        mock_artifacts,
        mock_agent_response
    ):
        """Test progress callback is invoked correctly."""
        from codeindex.web.agents.base import AgentRole

        # Mock agents
        for mock_agent, agent_role in [
            (mock_backend, AgentRole.BACKEND_SPECIALIST),
            (mock_frontend, AgentRole.FRONTEND_SPECIALIST),
            (mock_data_analyst, AgentRole.DATA_ANALYST),
            (mock_prd_writer, AgentRole.PRD_WRITER)
        ]:
            agent_instance = Mock()
            agent_instance.execute_query.return_value = mock_agent_response(
                agent_role,
                f"{agent_role.value} complete"
            )
            mock_agent.return_value = agent_instance

        # Create progress callback mock
        progress_callback = Mock()

        # Execute workflow with callback
        workflow.execute(mock_artifacts, "TestProject", progress_callback=progress_callback)

        # Verify callback was called for each step + final
        assert progress_callback.call_count == 5  # 4 steps + 1 final

        # Verify callback arguments
        calls = progress_callback.call_args_list
        assert calls[0] == call(0, 4, AgentRole.BACKEND_SPECIALIST)
        assert calls[1] == call(1, 4, AgentRole.FRONTEND_SPECIALIST)
        assert calls[2] == call(2, 4, AgentRole.DATA_ANALYST)
        assert calls[3] == call(3, 4, AgentRole.PRD_WRITER)
        assert calls[4] == call(4, 4, None)  # Final progress

    @patch('codeindex.web.workflows.prd_generation.get_backend_specialist_agent')
    def test_workflow_stops_on_step_failure(
        self,
        mock_backend,
        workflow,
        mock_artifacts
    ):
        """Test workflow stops when a step fails."""
        from codeindex.web.agents.base import AgentResponse, AgentRole

        # Mock backend agent to fail
        mock_backend_agent = Mock()
        error_response = AgentResponse(
            agent_role=AgentRole.BACKEND_SPECIALIST,
            query="Test query",
            timestamp="2024-01-01T00:00:00",
            duration_seconds=1.0,
            response_text="",
            error="Connection timeout"
        )
        mock_backend_agent.execute_query.return_value = error_response
        mock_backend.return_value = mock_backend_agent

        # Execute workflow
        result = workflow.execute(mock_artifacts, "TestProject")

        # Verify workflow failed
        assert result["success"] == False
        assert "Backend Specialist" in result["error"]
        assert "Connection timeout" in result["error"]

        # Verify only first step was executed
        assert workflow.steps[0].status == "failed"
        assert workflow.steps[1].status == "pending"  # Never executed
        assert workflow.steps[2].status == "pending"
        assert workflow.steps[3].status == "pending"

    @patch('codeindex.web.workflows.prd_generation.get_backend_specialist_agent')
    def test_workflow_handles_exception_in_step(
        self,
        mock_backend,
        workflow,
        mock_artifacts
    ):
        """Test workflow handles exceptions during step execution."""
        # Mock backend agent to raise exception
        mock_backend_agent = Mock()
        mock_backend_agent.execute_query.side_effect = Exception("Agent crashed")
        mock_backend.return_value = mock_backend_agent

        # Execute workflow
        result = workflow.execute(mock_artifacts, "TestProject")

        # Verify workflow failed
        assert result["success"] == False
        assert "Agent crashed" in result["error"]

        # Verify step marked as failed
        assert workflow.steps[0].status == "failed"
        assert "Agent crashed" in workflow.steps[0].error

    def test_workflow_cancellation(self, workflow, mock_artifacts):
        """Test workflow can be cancelled."""
        # Cancel workflow immediately
        workflow.is_cancelled = True

        # Execute workflow
        result = workflow.execute(mock_artifacts, "TestProject")

        # Verify workflow was cancelled
        assert result["success"] == False
        assert "cancelled" in result["error"].lower()

        # Verify no steps were executed
        assert all(step.status == "pending" for step in workflow.steps)

    @patch('codeindex.web.workflows.prd_generation.get_backend_specialist_agent')
    @patch('codeindex.web.workflows.prd_generation.get_frontend_specialist_agent')
    def test_workflow_cancellation_during_execution(
        self,
        mock_frontend,
        mock_backend,
        workflow,
        mock_artifacts,
        mock_agent_response
    ):
        """Test workflow can be cancelled mid-execution."""
        from codeindex.web.agents.base import AgentRole

        # Mock backend agent to succeed
        mock_backend_agent = Mock()
        mock_backend_agent.execute_query.return_value = mock_agent_response(
            AgentRole.BACKEND_SPECIALIST,
            "Backend complete"
        )
        mock_backend.return_value = mock_backend_agent

        # Mock frontend agent but set cancelled flag before it runs
        def cancel_after_backend(*args, **kwargs):
            workflow.is_cancelled = True
            return mock_agent_response(AgentRole.FRONTEND_SPECIALIST, "Frontend complete")

        mock_frontend_agent = Mock()
        mock_frontend_agent.execute_query.side_effect = cancel_after_backend
        mock_frontend.return_value = mock_frontend_agent

        # Execute workflow
        result = workflow.execute(mock_artifacts, "TestProject")

        # Verify workflow was cancelled
        assert result["success"] == False
        assert "cancelled" in result["error"].lower()

    def test_build_query_for_backend(self, workflow):
        """Test query building for Backend Specialist."""
        from codeindex.web.agents.base import AgentRole

        workflow.context = {
            "project_name": "MyProject",
            "artifact_count": 10
        }

        query = workflow._build_query(AgentRole.BACKEND_SPECIALIST)

        assert "MyProject" in query
        assert "backend" in query.lower()
        assert "10 artifacts" in query

    def test_build_query_for_frontend(self, workflow):
        """Test query building for Frontend Specialist."""
        from codeindex.web.agents.base import AgentRole

        workflow.context = {
            "project_name": "MyProject",
            "artifact_count": 15
        }

        query = workflow._build_query(AgentRole.FRONTEND_SPECIALIST)

        assert "MyProject" in query
        assert "frontend" in query.lower()
        assert "15 artifacts" in query

    def test_build_query_for_data_analyst(self, workflow):
        """Test query building for Data Analyst."""
        from codeindex.web.agents.base import AgentRole

        workflow.context = {
            "project_name": "MyProject",
            "artifact_count": 5
        }

        query = workflow._build_query(AgentRole.DATA_ANALYST)

        assert "MyProject" in query
        assert "data" in query.lower()
        assert "5 artifacts" in query

    def test_build_query_for_prd_writer_includes_previous_analyses(self, workflow):
        """Test PRD Writer query includes previous agent analyses."""
        from codeindex.web.agents.base import AgentRole

        workflow.context = {
            "project_name": "MyProject",
            "Backend Specialist_analysis": "Backend: Services and APIs...",
            "Frontend Specialist_analysis": "Frontend: UI components...",
            "Data Analyst_analysis": "Data: Database schema..."
        }

        query = workflow._build_query(AgentRole.PRD_WRITER)

        assert "MyProject" in query
        assert "Backend" in query or "Services" in query
        assert "Frontend" in query or "UI" in query
        assert "Data" in query or "Database" in query

    def test_result_structure(self, workflow, mock_artifacts):
        """Test workflow result has correct structure."""
        # Create result without execution
        result = workflow._create_result(
            success=True,
            prd_content="# PRD\n\nTest content"
        )

        assert "success" in result
        assert "prd_content" in result
        assert "steps" in result
        assert "error" in result

        assert result["success"] == True
        assert "PRD" in result["prd_content"]
        assert isinstance(result["steps"], list)
        assert len(result["steps"]) == 4

    def test_result_includes_step_details(self, workflow):
        """Test workflow result includes step details."""
        from codeindex.web.agents.base import AgentResponse, AgentRole

        # Set up completed step
        workflow.steps[0].status = "completed"
        workflow.steps[0].start_time = "2024-01-01T00:00:00"
        workflow.steps[0].end_time = "2024-01-01T00:00:05"
        workflow.steps[0].response = AgentResponse(
            agent_role=AgentRole.BACKEND_SPECIALIST,
            query="Test",
            timestamp="2024-01-01T00:00:00",
            duration_seconds=5.0,
            response_text="Test"
        )

        result = workflow._create_result(success=True)

        step_info = result["steps"][0]
        assert step_info["agent_role"] == "Backend Specialist"
        assert step_info["status"] == "completed"
        assert step_info["start_time"] == "2024-01-01T00:00:00"
        assert step_info["end_time"] == "2024-01-01T00:00:05"
        assert step_info["duration_seconds"] == 5.0

    def test_cancel_method(self, workflow):
        """Test workflow cancel method."""
        assert workflow.is_cancelled == False

        workflow.cancel()

        assert workflow.is_cancelled == True
