"""
Settings service for managing agent configuration (US2.4).

This service handles:
- Loading and saving agent settings from session state
- Settings validation
- Default settings management
- Settings persistence across user session
"""

from typing import Dict, Any, Tuple, List, Optional
from codeindex.web.utils.session_state import get, set_value


# Settings service singleton
_settings_service = None


class SettingsService:
    """Service for managing agent settings."""

    def __init__(self):
        """Initialize settings service."""
        self._defaults = self._get_default_settings()
        self._valid_values = self._get_valid_values()

    def _get_default_settings(self) -> Dict[str, Any]:
        """Get default settings."""
        return {
            "verbosity": "standard",
            "technical_level": "senior",
            "citation_style": "inline",
            "ui_theme": "light",
            "output_format": "markdown"
        }

    def _get_valid_values(self) -> Dict[str, List[str]]:
        """Get valid values for each setting."""
        return {
            "verbosity": ["concise", "standard", "verbose"],
            "technical_level": ["junior", "mid", "senior"],
            "citation_style": ["inline", "footnotes", "none"],
            "ui_theme": ["light", "dark"],
            "output_format": ["markdown", "text"]
        }

    def load_settings(self) -> Dict[str, Any]:
        """
        Load settings from session state.

        Returns:
            Dictionary of settings with defaults for missing keys
        """
        current_settings = get("agent_settings", {})

        # Merge with defaults for missing keys
        settings = self._defaults.copy()
        settings.update(current_settings)

        return settings

    def save_settings(self, settings: Dict[str, Any], validate: bool = False):
        """
        Save settings to session state.

        Args:
            settings: Settings dictionary
            validate: Whether to validate settings before saving

        Raises:
            ValueError: If validate=True and settings are invalid
        """
        if validate:
            is_valid, errors = self.validate_settings(settings)
            if not is_valid:
                error_messages = [f"{key}: {msg}" for key, msg in errors.items()]
                raise ValueError(f"Invalid settings: {', '.join(error_messages)}")

        set_value("agent_settings", settings)

    def validate_settings(self, settings: Dict[str, Any]) -> Tuple[bool, Dict[str, str]]:
        """
        Validate settings values.

        Args:
            settings: Settings dictionary to validate

        Returns:
            Tuple of (is_valid, error_dict)
        """
        errors = {}

        for key, value in settings.items():
            if key in self._valid_values:
                if value not in self._valid_values[key]:
                    valid_options = ", ".join(self._valid_values[key])
                    errors[key] = f"Must be one of: {valid_options}"

        is_valid = len(errors) == 0
        return is_valid, errors

    def reset_settings(self):
        """Reset settings to default values."""
        self.save_settings(self._defaults)

    def get_setting(self, key: str, default: Optional[Any] = None) -> Any:
        """
        Get individual setting value.

        Args:
            key: Setting key
            default: Default value if key not found

        Returns:
            Setting value
        """
        settings = self.load_settings()
        return settings.get(key, default if default is not None else self._defaults.get(key))

    def update_setting(self, key: str, value: Any):
        """
        Update individual setting value.

        Args:
            key: Setting key
            value: New value
        """
        settings = self.load_settings()
        settings[key] = value
        self.save_settings(settings)

    def get_default_settings(self) -> Dict[str, Any]:
        """Get default settings dictionary."""
        return self._defaults.copy()


def get_settings_service() -> SettingsService:
    """Get settings service singleton."""
    global _settings_service
    if _settings_service is None:
        _settings_service = SettingsService()
    return _settings_service


# Convenience functions for backward compatibility
def load_settings() -> Dict[str, Any]:
    """Load settings from session state."""
    return get_settings_service().load_settings()


def save_settings(settings: Dict[str, Any], validate: bool = False):
    """Save settings to session state."""
    get_settings_service().save_settings(settings, validate)


def validate_settings(settings: Dict[str, Any]) -> Tuple[bool, Dict[str, str]]:
    """Validate settings values."""
    return get_settings_service().validate_settings(settings)


def reset_settings():
    """Reset settings to defaults."""
    get_settings_service().reset_settings()


def get_setting(key: str, default: Optional[Any] = None) -> Any:
    """Get individual setting value."""
    return get_settings_service().get_setting(key, default)


def update_setting(key: str, value: Any):
    """Update individual setting value."""
    get_settings_service().update_setting(key, value)


def get_default_settings() -> Dict[str, Any]:
    """Get default settings dictionary."""
    return get_settings_service().get_default_settings()
