"""
Unit tests for Data Analyst agent (T070).

Tests agent configuration, database analysis tools, and query execution.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from typing import List, Dict, Any
from datetime import datetime

from codeindex.web.agents.data_analyst import (
    DataAnalystAgent,
    get_data_analyst_agent
)
from codeindex.web.agents.base import (
    AgentRole,
    AgentConfig,
    AgentResponse,
    Citation
)


class TestDataAnalystAgent:
    """Test suite for DataAnalystAgent."""

    @pytest.fixture
    def agent_config(self) -> AgentConfig:
        """Create test agent configuration."""
        return AgentConfig(
            role=AgentRole.DATA_ANALYST,
            goal="Analyze database schemas and data flows",
            backstory="Test Data Analyst agent for unit testing",
            temperature=0.3,
            max_tokens=2000
        )

    @pytest.fixture
    def data_analyst(self, agent_config) -> DataAnalystAgent:
        """Create Data Analyst agent instance."""
        return DataAnalystAgent(config=agent_config)

    @pytest.fixture
    def mock_db_artifacts(self) -> List[Dict[str, Any]]:
        """Create mock database artifacts."""
        return [
            {
                "id": "table_001",
                "artifactType": "DbTable",
                "relativePath": "schema/users.sql",
                "fileName": "users.sql",
                "summary": "User account table",
                "entities": ["users", "user_id", "email"],
                "_additional": {"id": "uuid-table-001", "distance": 0.1}
            },
            {
                "id": "dao_001",
                "artifactType": "DaoCall",
                "relativePath": "dao/UserDao.java",
                "fileName": "UserDao.java",
                "summary": "User data access object",
                "entities": ["getUserById", "insertUser", "updateUser"],
                "_additional": {"id": "uuid-dao-001", "distance": 0.15}
            },
            {
                "id": "ibatis_001",
                "artifactType": "IbatisStatement",
                "relativePath": "sqlmap/User.xml",
                "fileName": "User.xml",
                "summary": "User SQL mappings",
                "entities": ["selectUser", "insertUser"],
                "_additional": {"id": "uuid-ibatis-001", "distance": 0.2}
            },
            {
                "id": "dto_001",
                "artifactType": "DtoArtifact",
                "relativePath": "dto/UserDTO.java",
                "fileName": "UserDTO.java",
                "summary": "User data transfer object",
                "entities": ["userId", "username", "email"],
                "_additional": {"id": "uuid-dto-001", "distance": 0.25}
            }
        ]

    def test_agent_initialization(self, data_analyst, agent_config):
        """Test that Data Analyst agent initializes correctly."""
        assert data_analyst is not None
        assert data_analyst.role == AgentRole.DATA_ANALYST
        assert data_analyst.config == agent_config

    def test_agent_initialization_with_default_config(self):
        """Test agent initialization with default configuration."""
        agent = DataAnalystAgent()
        assert agent is not None
        assert agent.role == AgentRole.DATA_ANALYST
        assert agent.config is not None

    @patch('codeindex.web.services.search_service.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_execute_query_success(
        self,
        mock_ollama,
        mock_get_search,
        data_analyst,
        mock_db_artifacts
    ):
        """Test successful query execution."""
        # Mock search service
        mock_search = Mock()
        mock_search.search.return_value = {
            "results": mock_db_artifacts,
            "total": 4
        }
        mock_get_search.return_value = mock_search

        # Mock Ollama response
        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.return_value = {
            "response": "The database schema includes a users table with user_id, email columns."
        }
        mock_ollama.return_value = mock_ollama_instance

        # Execute query
        response = data_analyst.execute_query("What tables are in the database?")

        # Verify response
        assert isinstance(response, AgentResponse)
        assert response.agent_role == AgentRole.DATA_ANALYST
        assert response.query == "What tables are in the database?"
        assert "users table" in response.response_text.lower()
        assert len(response.citations) > 0
        assert len(response.suggested_questions) > 0
        assert response.tools_used == ["WeaviateSearchTool", "DbSchemaAnalyzer", "DaoPatternAnalyzer"]
        assert response.error is None

    @patch('codeindex.web.services.search_service.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_execute_query_with_error(self, mock_ollama, mock_get_search, data_analyst):
        """Test query execution with error handling."""
        # Mock search service to return empty results
        mock_search = Mock()
        mock_search.search.return_value = {"results": [], "total": 0}
        mock_get_search.return_value = mock_search

        # Mock Ollama to raise exception (to trigger fallback)
        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.side_effect = Exception("Connection timeout")
        mock_ollama.return_value = mock_ollama_instance

        # Execute query
        response = data_analyst.execute_query("What tables exist?")

        # Verify fallback response (error caught in _generate_data_analysis)
        assert isinstance(response, AgentResponse)
        # Fallback generates response_text with error explanation
        assert len(response.response_text) > 0
        assert ("error" in response.response_text.lower() or
                "ensure" in response.response_text.lower())
        # Error field is None because exception was handled in fallback
        assert response.error is None

    @patch('codeindex.web.services.search_service.get_search_service')
    def test_search_database_artifacts(self, mock_get_search, data_analyst, mock_db_artifacts):
        """Test searching for database artifacts."""
        # Mock search service
        mock_search = Mock()
        mock_search.search.return_value = {
            "results": mock_db_artifacts,
            "total": 4
        }
        mock_get_search.return_value = mock_search

        # Search artifacts
        artifacts = data_analyst._search_database_artifacts("user table")

        # Verify search
        mock_search.search.assert_called_once()
        call_args = mock_search.search.call_args
        assert call_args[1]["query"] == "user table"
        assert "DbTable" in call_args[1]["filters"]["artifact_types"]
        assert "DaoCall" in call_args[1]["filters"]["artifact_types"]
        assert call_args[1]["limit"] == 15

        assert len(artifacts) == 4

    @patch('codeindex.web.services.search_service.get_search_service')
    def test_search_database_artifacts_error(self, mock_get_search, data_analyst):
        """Test error handling in artifact search."""
        # Mock search service to raise exception
        mock_get_search.side_effect = Exception("Search failed")

        # Search should return empty list on error
        artifacts = data_analyst._search_database_artifacts("test")
        assert artifacts == []

    def test_analyze_dao_patterns(self, data_analyst, mock_db_artifacts):
        """Test DAO pattern analysis."""
        analysis = data_analyst._analyze_dao_patterns(mock_db_artifacts)

        # Verify DAO analysis
        assert analysis["dao_count"] == 1
        assert analysis["ibatis_count"] == 1
        assert len(analysis["dao_methods"]) > 0
        assert "getUserById" in analysis["dao_methods"]
        assert "DAO Pattern" in analysis["patterns"]

    def test_analyze_dao_patterns_empty(self, data_analyst):
        """Test DAO pattern analysis with no artifacts."""
        analysis = data_analyst._analyze_dao_patterns([])

        assert analysis["dao_count"] == 0
        assert analysis["ibatis_count"] == 0
        assert len(analysis["dao_methods"]) == 0

    def test_extract_schema_info(self, data_analyst, mock_db_artifacts):
        """Test schema information extraction."""
        schema_info = data_analyst._extract_schema_info(mock_db_artifacts)

        # Verify schema extraction
        assert schema_info["table_count"] == 1
        assert "users" in schema_info["tables"]
        assert schema_info["dto_count"] == 1
        assert "userId" in schema_info["dtos"]

    def test_extract_schema_info_empty(self, data_analyst):
        """Test schema extraction with no artifacts."""
        schema_info = data_analyst._extract_schema_info([])

        assert schema_info["table_count"] == 0
        assert len(schema_info["tables"]) == 0
        assert schema_info["dto_count"] == 0

    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_generate_data_analysis_success(
        self,
        mock_ollama,
        data_analyst,
        mock_db_artifacts
    ):
        """Test data analysis generation with LLM."""
        # Mock Ollama response
        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.return_value = {
            "response": "The users table contains user account data with columns for user_id and email."
        }
        mock_ollama.return_value = mock_ollama_instance

        # Prepare inputs
        dao_analysis = {
            "dao_count": 1,
            "ibatis_count": 1,
            "dao_methods": ["getUserById"],
            "patterns": ["DAO Pattern"]
        }
        schema_info = {
            "table_count": 1,
            "tables": ["users"],
            "dto_count": 1,
            "dtos": ["UserDTO"]
        }

        # Generate analysis
        analysis = data_analyst._generate_data_analysis(
            "Explain the user table",
            mock_db_artifacts,
            dao_analysis,
            schema_info,
            None
        )

        # Verify analysis
        assert "users table" in analysis.lower()
        assert len(analysis) > 0
        mock_ollama_instance.call_ollama.assert_called_once()

    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_generate_data_analysis_with_error(
        self,
        mock_ollama,
        data_analyst,
        mock_db_artifacts
    ):
        """Test data analysis generation with LLM error (fallback)."""
        # Mock Ollama to raise exception
        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.side_effect = Exception("Ollama timeout")
        mock_ollama.return_value = mock_ollama_instance

        # Prepare inputs
        dao_analysis = {"dao_count": 1, "ibatis_count": 1, "dao_methods": ["getUserById"], "patterns": []}
        schema_info = {"table_count": 1, "tables": ["users"], "dto_count": 1, "dtos": ["UserDTO"]}

        # Generate analysis (should use fallback)
        analysis = data_analyst._generate_data_analysis(
            "Test query",
            mock_db_artifacts,
            dao_analysis,
            schema_info,
            None
        )

        # Verify fallback response
        assert "error" in analysis.lower() or "database tables" in analysis.lower()
        assert len(analysis) > 0

    def test_extract_citations(self, data_analyst, mock_db_artifacts):
        """Test citation extraction from artifacts."""
        citations = data_analyst._extract_citations(mock_db_artifacts)

        # Verify citations
        assert len(citations) == 4
        assert all(isinstance(c, Citation) for c in citations)

        # Check first citation
        assert citations[0].artifact_id == "uuid-table-001"
        assert "users.sql" in citations[0].file_path
        assert citations[0].artifact_type == "DbTable"
        assert 0.0 <= citations[0].confidence <= 1.0

    def test_extract_citations_limited(self, data_analyst):
        """Test citation extraction with limit."""
        # Create 15 artifacts
        many_artifacts = [
            {
                "id": f"artifact_{i}",
                "artifactType": "DbTable",
                "relativePath": f"table_{i}.sql",
                "fileName": f"table_{i}.sql",
                "_additional": {"id": f"uuid-{i}", "distance": 0.1}
            }
            for i in range(15)
        ]

        citations = data_analyst._extract_citations(many_artifacts)

        # Should limit to 10 citations
        assert len(citations) == 10

    def test_generate_follow_ups_with_tables(self, data_analyst, mock_db_artifacts):
        """Test follow-up question generation with table artifacts."""
        suggestions = data_analyst._generate_follow_ups("test query", mock_db_artifacts)

        # Verify suggestions
        assert len(suggestions) <= 4
        assert any("foreign key" in s.lower() for s in suggestions)

    def test_generate_follow_ups_with_daos(self, data_analyst):
        """Test follow-up generation with DAO artifacts."""
        dao_artifacts = [
            {"artifactType": "DaoCall", "id": "dao_001"}
        ]

        suggestions = data_analyst._generate_follow_ups("test query", dao_artifacts)

        assert len(suggestions) > 0
        assert any("dao" in s.lower() for s in suggestions)

    def test_generate_follow_ups_empty(self, data_analyst):
        """Test follow-up generation with no artifacts."""
        suggestions = data_analyst._generate_follow_ups("test query", [])

        # Should provide generic suggestions
        assert len(suggestions) > 0
        assert len(suggestions) <= 4

    def test_get_data_analyst_agent_singleton(self):
        """Test global singleton pattern."""
        # Reset global instance
        import codeindex.web.agents.data_analyst as module
        module._data_analyst_agent = None

        # Get instances
        agent1 = get_data_analyst_agent()
        agent2 = get_data_analyst_agent()

        # Should be same instance
        assert agent1 is agent2
        assert isinstance(agent1, DataAnalystAgent)

    def test_agent_response_structure(self, data_analyst):
        """Test that agent response has correct structure."""
        with patch('codeindex.web.services.search_service.get_search_service') as mock_search:
            with patch('codeindex.services.ollama_client.OllamaClient') as mock_ollama:
                # Mock minimal setup
                mock_search_instance = Mock()
                mock_search_instance.search.return_value = {"results": [], "total": 0}
                mock_search.return_value = mock_search_instance

                mock_ollama_instance = Mock()
                mock_ollama_instance.call_ollama.return_value = {"response": "Test response"}
                mock_ollama.return_value = mock_ollama_instance

                response = data_analyst.execute_query("test")

                # Verify all required fields
                assert hasattr(response, 'agent_role')
                assert hasattr(response, 'query')
                assert hasattr(response, 'timestamp')
                assert hasattr(response, 'duration_seconds')
                assert hasattr(response, 'response_text')
                assert hasattr(response, 'citations')
                assert hasattr(response, 'confidence')
                assert hasattr(response, 'suggested_questions')
                assert hasattr(response, 'tools_used')
                assert hasattr(response, 'error')

    @patch('codeindex.web.services.search_service.get_search_service')
    def test_context_passing(self, mock_get_search, data_analyst, mock_db_artifacts):
        """Test that context is passed correctly."""
        # Mock search
        mock_search = Mock()
        mock_search.search.return_value = {"results": mock_db_artifacts, "total": 4}
        mock_get_search.return_value = mock_search

        with patch('codeindex.services.ollama_client.OllamaClient') as mock_ollama:
            mock_ollama_instance = Mock()
            mock_ollama_instance.call_ollama.return_value = {"response": "Test"}
            mock_ollama.return_value = mock_ollama_instance

            context = {"previous_query": "What tables?", "project": "test-project"}
            response = data_analyst.execute_query("Follow-up question", context=context)

            assert response is not None
            assert response.error is None
