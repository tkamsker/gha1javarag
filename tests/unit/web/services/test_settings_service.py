"""
Unit tests for settings persistence service (T098 - US2.4).

Tests settings storage in session state, validation, and default values.
"""

import pytest
from unittest.mock import Mock, patch
from typing import Dict, Any


class TestSettingsService:
    """Test suite for settings service."""

    @pytest.fixture
    def default_settings(self) -> Dict[str, Any]:
        """Create default settings."""
        return {
            "verbosity": "standard",
            "technical_level": "senior",
            "citation_style": "inline",
            "ui_theme": "light",
            "output_format": "markdown"
        }

    def test_get_default_settings(self, default_settings):
        """Test retrieving default settings."""
        from codeindex.web.services.settings_service import get_default_settings

        defaults = get_default_settings()

        assert defaults["verbosity"] == "standard"
        assert defaults["technical_level"] == "senior"
        assert defaults["citation_style"] == "inline"
        assert defaults["ui_theme"] == "light"
        assert defaults["output_format"] == "markdown"

    @patch('codeindex.web.services.settings_service.get')
    @patch('codeindex.web.services.settings_service.set_value')
    def test_load_settings_from_session_state(self, mock_set, mock_get):
        """Test loading settings from session state."""
        from codeindex.web.services.settings_service import load_settings

        # Mock existing settings in session state
        mock_get.return_value = {
            "verbosity": "verbose",
            "technical_level": "junior",
            "citation_style": "footnotes",
            "ui_theme": "dark",
            "output_format": "text"
        }

        settings = load_settings()

        assert settings["verbosity"] == "verbose"
        assert settings["technical_level"] == "junior"
        assert settings["citation_style"] == "footnotes"
        assert settings["ui_theme"] == "dark"
        assert settings["output_format"] == "text"

    @patch('codeindex.web.services.settings_service.get')
    @patch('codeindex.web.services.settings_service.set_value')
    def test_load_settings_with_missing_keys(self, mock_set, mock_get):
        """Test loading settings when some keys are missing."""
        from codeindex.web.services.settings_service import load_settings, get_default_settings

        # Mock partial settings (missing ui_theme and output_format)
        mock_get.return_value = {
            "verbosity": "concise",
            "technical_level": "mid",
            "citation_style": "none"
        }

        settings = load_settings()

        # Should have values from session state
        assert settings["verbosity"] == "concise"
        assert settings["technical_level"] == "mid"
        assert settings["citation_style"] == "none"

        # Should have default values for missing keys
        defaults = get_default_settings()
        assert settings["ui_theme"] == defaults["ui_theme"]
        assert settings["output_format"] == defaults["output_format"]

    @patch('codeindex.web.services.settings_service.set_value')
    def test_save_settings_to_session_state(self, mock_set):
        """Test saving settings to session state."""
        from codeindex.web.services.settings_service import save_settings

        new_settings = {
            "verbosity": "verbose",
            "technical_level": "senior",
            "citation_style": "inline",
            "ui_theme": "dark",
            "output_format": "markdown"
        }

        save_settings(new_settings)

        # Verify set_value was called with settings
        mock_set.assert_called_once_with("agent_settings", new_settings)

    def test_validate_settings_valid(self):
        """Test settings validation with valid settings."""
        from codeindex.web.services.settings_service import validate_settings

        valid_settings = {
            "verbosity": "standard",
            "technical_level": "senior",
            "citation_style": "inline",
            "ui_theme": "light",
            "output_format": "markdown"
        }

        is_valid, errors = validate_settings(valid_settings)

        assert is_valid == True
        assert len(errors) == 0

    def test_validate_settings_invalid_verbosity(self):
        """Test settings validation with invalid verbosity."""
        from codeindex.web.services.settings_service import validate_settings

        invalid_settings = {
            "verbosity": "invalid_value",
            "technical_level": "senior",
            "citation_style": "inline",
            "ui_theme": "light",
            "output_format": "markdown"
        }

        is_valid, errors = validate_settings(invalid_settings)

        assert is_valid == False
        assert "verbosity" in errors
        assert "concise" in errors["verbosity"].lower() or "standard" in errors["verbosity"].lower()

    def test_validate_settings_invalid_technical_level(self):
        """Test settings validation with invalid technical level."""
        from codeindex.web.services.settings_service import validate_settings

        invalid_settings = {
            "verbosity": "standard",
            "technical_level": "invalid_value",
            "citation_style": "inline",
            "ui_theme": "light",
            "output_format": "markdown"
        }

        is_valid, errors = validate_settings(invalid_settings)

        assert is_valid == False
        assert "technical_level" in errors

    def test_validate_settings_invalid_citation_style(self):
        """Test settings validation with invalid citation style."""
        from codeindex.web.services.settings_service import validate_settings

        invalid_settings = {
            "verbosity": "standard",
            "technical_level": "senior",
            "citation_style": "invalid_value",
            "ui_theme": "light",
            "output_format": "markdown"
        }

        is_valid, errors = validate_settings(invalid_settings)

        assert is_valid == False
        assert "citation_style" in errors

    def test_validate_settings_multiple_errors(self):
        """Test settings validation with multiple invalid fields."""
        from codeindex.web.services.settings_service import validate_settings

        invalid_settings = {
            "verbosity": "invalid1",
            "technical_level": "invalid2",
            "citation_style": "invalid3",
            "ui_theme": "invalid4",
            "output_format": "invalid5"
        }

        is_valid, errors = validate_settings(invalid_settings)

        assert is_valid == False
        assert len(errors) == 5
        assert "verbosity" in errors
        assert "technical_level" in errors
        assert "citation_style" in errors
        assert "ui_theme" in errors
        assert "output_format" in errors

    @patch('codeindex.web.services.settings_service.set_value')
    def test_reset_settings_to_defaults(self, mock_set):
        """Test resetting settings to default values."""
        from codeindex.web.services.settings_service import reset_settings, get_default_settings

        reset_settings()

        # Verify set_value was called with default settings
        defaults = get_default_settings()
        mock_set.assert_called_once_with("agent_settings", defaults)

    def test_get_setting_value(self):
        """Test retrieving individual setting value."""
        from codeindex.web.services.settings_service import get_setting

        settings = {
            "verbosity": "verbose",
            "technical_level": "junior"
        }

        with patch('codeindex.web.services.settings_service.load_settings', return_value=settings):
            verbosity = get_setting("verbosity")
            technical_level = get_setting("technical_level")

            assert verbosity == "verbose"
            assert technical_level == "junior"

    def test_get_setting_value_missing_key(self):
        """Test retrieving setting value with missing key returns default."""
        from codeindex.web.services.settings_service import get_setting, get_default_settings

        settings = {
            "verbosity": "standard"
        }

        defaults = get_default_settings()

        with patch('codeindex.web.services.settings_service.load_settings', return_value=settings):
            # Missing key should return default
            ui_theme = get_setting("ui_theme")
            assert ui_theme == defaults["ui_theme"]

    def test_update_setting_value(self):
        """Test updating individual setting value."""
        from codeindex.web.services.settings_service import update_setting

        current_settings = {
            "verbosity": "standard",
            "technical_level": "senior",
            "citation_style": "inline",
            "ui_theme": "light",
            "output_format": "markdown"
        }

        with patch('codeindex.web.services.settings_service.load_settings', return_value=current_settings):
            with patch('codeindex.web.services.settings_service.save_settings') as mock_save:
                update_setting("verbosity", "verbose")

                # Verify save was called with updated settings
                mock_save.assert_called_once()
                updated_settings = mock_save.call_args[0][0]
                assert updated_settings["verbosity"] == "verbose"
                assert updated_settings["technical_level"] == "senior"  # Unchanged

    def test_settings_service_singleton(self):
        """Test settings service maintains singleton instance."""
        from codeindex.web.services.settings_service import get_settings_service

        service1 = get_settings_service()
        service2 = get_settings_service()

        assert service1 is service2
