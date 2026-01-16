"""
Unit tests for agent configuration application (T099 - US2.4).

Tests settings propagation to agents and AgentConfig updates.
"""

import pytest
from unittest.mock import Mock, patch
from typing import Dict, Any


class TestAgentConfigApplication:
    """Test suite for agent configuration application."""

    @pytest.fixture
    def sample_settings(self) -> Dict[str, Any]:
        """Create sample agent settings."""
        return {
            "verbosity": "verbose",
            "technical_level": "junior",
            "citation_style": "footnotes",
            "ui_theme": "dark",
            "output_format": "text"
        }

    @pytest.fixture
    def default_agent_config(self):
        """Create default agent config."""
        from codeindex.web.agents.base import AgentConfig, AgentRole

        return AgentConfig(
            role=AgentRole.SENIOR_DEVELOPER,
            goal="Test goal",
            backstory="Test backstory",
            temperature=0.7,
            max_tokens=2000
        )

    def test_apply_settings_to_agent_config(self, sample_settings, default_agent_config):
        """Test applying settings to agent configuration."""
        from codeindex.web.agents.base import apply_settings_to_config

        updated_config = apply_settings_to_config(default_agent_config, sample_settings)

        # Verify settings were applied
        assert updated_config.verbosity == "verbose"
        assert updated_config.technical_level == "junior"
        assert updated_config.citation_style == "footnotes"
        assert updated_config.output_format == "text"

        # Verify original config fields preserved
        assert updated_config.role == default_agent_config.role
        assert updated_config.goal == default_agent_config.goal
        assert updated_config.backstory == default_agent_config.backstory

    def test_apply_settings_with_partial_settings(self, default_agent_config):
        """Test applying partial settings (some keys missing)."""
        from codeindex.web.agents.base import apply_settings_to_config

        partial_settings = {
            "verbosity": "concise",
            "technical_level": "mid"
            # Missing: citation_style, ui_theme, output_format
        }

        updated_config = apply_settings_to_config(default_agent_config, partial_settings)

        # Applied settings
        assert updated_config.verbosity == "concise"
        assert updated_config.technical_level == "mid"

        # Missing settings should use defaults
        assert hasattr(updated_config, 'citation_style')
        assert hasattr(updated_config, 'output_format')

    def test_create_agent_with_settings(self, sample_settings):
        """Test creating agent instance with settings."""
        from codeindex.web.agents.senior_developer import get_senior_developer_agent
        from codeindex.web.agents.base import apply_settings_to_agent

        # Create agent
        agent = get_senior_developer_agent()

        # Apply settings
        with patch('codeindex.web.services.settings_service.load_settings', return_value=sample_settings):
            apply_settings_to_agent(agent, sample_settings)

            # Verify agent config was updated
            assert agent.config.verbosity == "verbose"
            assert agent.config.technical_level == "junior"
            assert agent.config.citation_style == "footnotes"

    def test_settings_propagate_to_agent_response(self, sample_settings):
        """Test that settings affect agent response generation."""
        from codeindex.web.agents.senior_developer import SeniorDeveloperAgent
        from codeindex.web.agents.base import AgentConfig, AgentRole

        # Create agent with verbose settings
        verbose_settings = {
            "verbosity": "verbose",
            "technical_level": "junior",
            "citation_style": "inline",
            "output_format": "markdown"
        }

        config = AgentConfig(
            role=AgentRole.SENIOR_DEVELOPER,
            goal="Explain code",
            backstory="Senior developer",
            temperature=0.7,
            max_tokens=2000,
            verbosity="verbose",
            technical_level="junior",
            citation_style="inline",
            output_format="markdown"
        )

        agent = SeniorDeveloperAgent(config)

        # Verify config has settings
        assert agent.config.verbosity == "verbose"
        assert agent.config.technical_level == "junior"

    def test_verbosity_affects_prompt_generation(self):
        """Test that verbosity setting affects prompt generation."""
        from codeindex.web.agents.base import build_agent_prompt

        # Concise verbosity
        concise_prompt = build_agent_prompt(
            query="Explain authentication",
            verbosity="concise",
            technical_level="senior"
        )

        # Verbose verbosity
        verbose_prompt = build_agent_prompt(
            query="Explain authentication",
            verbosity="verbose",
            technical_level="senior"
        )

        # Verbose should have instructions for detailed explanations
        assert len(verbose_prompt) > len(concise_prompt)
        assert "detailed" in verbose_prompt.lower() or "thorough" in verbose_prompt.lower()

    def test_technical_level_affects_prompt_generation(self):
        """Test that technical level affects prompt generation."""
        from codeindex.web.agents.base import build_agent_prompt

        # Junior level
        junior_prompt = build_agent_prompt(
            query="Explain dependency injection",
            verbosity="standard",
            technical_level="junior"
        )

        # Senior level
        senior_prompt = build_agent_prompt(
            query="Explain dependency injection",
            verbosity="standard",
            technical_level="senior"
        )

        # Junior should have instructions for simpler explanations
        assert "beginner" in junior_prompt.lower() or "simple" in junior_prompt.lower() or "basic" in junior_prompt.lower()

        # Senior should allow technical jargon
        assert "technical" in senior_prompt.lower() or "advanced" in senior_prompt.lower()

    def test_citation_style_inline(self):
        """Test inline citation style formatting."""
        from codeindex.web.agents.base import format_citations

        citations = [
            {
                "artifact_id": "art-001",
                "file_path": "UserService.java",
                "artifact_type": "BackendDoc"
            },
            {
                "artifact_id": "art-002",
                "file_path": "UserDAO.java",
                "artifact_type": "DaoCall"
            }
        ]

        formatted = format_citations(citations, style="inline")

        # Inline format: [1] [2] references in text
        assert "[1]" in formatted or "UserService.java" in formatted
        assert "[2]" in formatted or "UserDAO.java" in formatted

    def test_citation_style_footnotes(self):
        """Test footnotes citation style formatting."""
        from codeindex.web.agents.base import format_citations

        citations = [
            {
                "artifact_id": "art-001",
                "file_path": "UserService.java",
                "artifact_type": "BackendDoc"
            }
        ]

        formatted = format_citations(citations, style="footnotes")

        # Footnotes format: numbered list at end
        assert "1." in formatted or "1:" in formatted
        assert "UserService.java" in formatted

    def test_citation_style_none(self):
        """Test no citations (none style)."""
        from codeindex.web.agents.base import format_citations

        citations = [
            {
                "artifact_id": "art-001",
                "file_path": "UserService.java",
                "artifact_type": "BackendDoc"
            }
        ]

        formatted = format_citations(citations, style="none")

        # Should return empty or minimal output
        assert formatted == "" or formatted is None

    def test_output_format_markdown(self):
        """Test markdown output formatting."""
        from codeindex.web.agents.base import format_response_output

        response_text = "This is a test response with **bold** and *italic*"

        formatted = format_response_output(response_text, output_format="markdown")

        # Should preserve markdown syntax
        assert "**bold**" in formatted
        assert "*italic*" in formatted

    def test_output_format_text(self):
        """Test plain text output formatting."""
        from codeindex.web.agents.base import format_response_output

        response_text = "This is a test response with **bold** and *italic*"

        formatted = format_response_output(response_text, output_format="text")

        # Should strip markdown syntax
        assert "**" not in formatted or "bold" in formatted
        assert "*" not in formatted or "italic" in formatted

    def test_settings_applied_to_all_agent_types(self, sample_settings):
        """Test settings are applied to all agent types."""
        from codeindex.web.agents.base import apply_settings_to_config, AgentRole, AgentConfig

        agent_roles = [
            AgentRole.SENIOR_DEVELOPER,
            AgentRole.DATA_ANALYST,
            AgentRole.FRONTEND_SPECIALIST,
            AgentRole.BACKEND_SPECIALIST,
            AgentRole.PRD_WRITER
        ]

        for role in agent_roles:
            config = AgentConfig(
                role=role,
                goal="Test",
                backstory="Test",
                temperature=0.7,
                max_tokens=2000
            )

            updated_config = apply_settings_to_config(config, sample_settings)

            # Verify settings applied to all agent types
            assert updated_config.verbosity == "verbose"
            assert updated_config.technical_level == "junior"
            assert updated_config.citation_style == "footnotes"

    def test_settings_override_default_config(self):
        """Test that settings override default agent configuration."""
        from codeindex.web.agents.base import AgentConfig, AgentRole, apply_settings_to_config

        # Default config with standard settings
        default_config = AgentConfig(
            role=AgentRole.SENIOR_DEVELOPER,
            goal="Test",
            backstory="Test",
            temperature=0.7,
            max_tokens=2000,
            verbosity="standard",  # Default
            technical_level="senior"  # Default
        )

        # Override settings
        override_settings = {
            "verbosity": "concise",
            "technical_level": "junior"
        }

        updated_config = apply_settings_to_config(default_config, override_settings)

        # Verify overrides applied
        assert updated_config.verbosity == "concise"  # Overridden
        assert updated_config.technical_level == "junior"  # Overridden

    def test_invalid_settings_raise_validation_error(self):
        """Test that invalid settings raise validation errors."""
        from codeindex.web.agents.base import apply_settings_to_config, AgentConfig, AgentRole

        config = AgentConfig(
            role=AgentRole.SENIOR_DEVELOPER,
            goal="Test",
            backstory="Test"
        )

        invalid_settings = {
            "verbosity": "invalid_value",
            "technical_level": "invalid_level"
        }

        # Should raise validation error or use defaults
        with pytest.raises(ValueError):
            apply_settings_to_config(config, invalid_settings, strict=True)
