"""
GWT Analyzer Registry

Central registry for all GWT-specific analyzers. Routes files to appropriate
analyzers based on GWT patterns and roles.

This module acts as a dispatcher:
1. Receives a file path and artifact type
2. Checks if file matches GWT patterns
3. Returns appropriate analyzer or None
"""

import logging
from pathlib import Path
from typing import Optional, Dict, Any

from codeindex.models import ArtifactType
from codeindex.utils.gwt_patterns import (
    classify_gwt_file,
    GwtRole,
    is_gwt_rpc_servlet
)


logger = logging.getLogger(__name__)


class GwtAnalyzerRegistry:
    """
    Registry for GWT analyzers.

    Manages lifecycle and routing for all GWT-specific analyzers.
    Analyzers are lazy-loaded to avoid circular dependencies.
    """

    def __init__(self):
        """Initialize the GWT analyzer registry."""
        self.logger = logging.getLogger(__name__)
        self._analyzers: Dict[GwtRole, Any] = {}
        self._initialized = False

    def _lazy_init(self):
        """
        Lazy initialization of analyzers.

        Import analyzers only when needed to avoid circular dependencies.
        This is called on first use of the registry.
        """
        if self._initialized:
            return

        self.logger.debug("Initializing GWT analyzer registry")

        # Import analyzers here to avoid circular imports
        # These will be populated as analyzers are implemented
        # in subsequent phases (US1, US2, US3, US4)

        try:
            from codeindex.services.gwt_rpc_analyzer import GwtRpcAnalyzer
            self._analyzers[GwtRole.RPC_SERVLET] = GwtRpcAnalyzer()
            self.logger.debug("Registered GwtRpcAnalyzer")
        except ImportError:
            self.logger.debug("GwtRpcAnalyzer not yet implemented")

        try:
            from codeindex.parsers.uibinder_parser import GwtUiBinderParser
            self._analyzers[GwtRole.UI_BINDER] = GwtUiBinderParser()
            self.logger.debug("Registered GwtUiBinderParser")
        except ImportError:
            self.logger.debug("GwtUiBinderParser not yet implemented")

        try:
            from codeindex.services.gwt_presenter_analyzer import GwtPresenterAnalyzer
            self._analyzers[GwtRole.PRESENTER] = GwtPresenterAnalyzer()
            self.logger.debug("Registered GwtPresenterAnalyzer")
        except ImportError:
            self.logger.debug("GwtPresenterAnalyzer not yet implemented")

        try:
            from codeindex.services.gwt_view_analyzer import GwtViewAnalyzer
            self._analyzers[GwtRole.VIEW] = GwtViewAnalyzer()
            self.logger.debug("Registered GwtViewAnalyzer")
        except ImportError:
            self.logger.debug("GwtViewAnalyzer not yet implemented")

        try:
            from codeindex.services.gwt_model_analyzer import GwtModelAnalyzer
            self._analyzers[GwtRole.SHARED_DTO] = GwtModelAnalyzer()
            self.logger.debug("Registered GwtModelAnalyzer")
        except ImportError:
            self.logger.debug("GwtModelAnalyzer not yet implemented")

        self._initialized = True
        self.logger.info(f"GWT analyzer registry initialized with {len(self._analyzers)} analyzers")

    def get_analyzer(self, file_path: Path, artifact_type: ArtifactType) -> Optional[Any]:
        """
        Get appropriate GWT analyzer for file.

        Args:
            file_path: Path to file
            artifact_type: Classified artifact type

        Returns:
            GWT analyzer instance or None if not a GWT file
        """
        self._lazy_init()

        # Check if this is a GWT file
        gwt_role = classify_gwt_file(file_path)

        if not gwt_role:
            return None

        # Return registered analyzer for this role
        analyzer = self._analyzers.get(gwt_role)

        if analyzer:
            self.logger.debug(f"Found analyzer for {gwt_role.value}: {type(analyzer).__name__}")
        else:
            self.logger.debug(f"No analyzer registered for {gwt_role.value}")

        return analyzer

    def can_analyze(self, file_path: Path, artifact_type: ArtifactType) -> bool:
        """
        Check if a GWT analyzer can handle this file.

        Args:
            file_path: Path to file
            artifact_type: Classified artifact type

        Returns:
            True if a GWT analyzer can process this file
        """
        analyzer = self.get_analyzer(file_path, artifact_type)
        return analyzer is not None

    def analyze(
        self,
        file_path: Path,
        artifact_type: ArtifactType,
        content: str,
        semantic_data: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Analyze file using appropriate GWT analyzer.

        Args:
            file_path: Path to file
            artifact_type: Classified artifact type
            content: File content
            semantic_data: Optional LLM-extracted semantic data

        Returns:
            GWT metadata dictionary or None if no analyzer available
        """
        analyzer = self.get_analyzer(file_path, artifact_type)

        if not analyzer:
            return None

        try:
            self.logger.debug(f"Analyzing {file_path.name} with {type(analyzer).__name__}")
            result = analyzer.analyze(file_path, content, semantic_data)
            return result
        except Exception as e:
            self.logger.error(f"GWT analyzer failed for {file_path}: {e}", exc_info=True)
            return None

    def get_registered_roles(self) -> list[GwtRole]:
        """
        Get list of GWT roles with registered analyzers.

        Returns:
            List of GwtRole enum values with analyzers
        """
        self._lazy_init()
        return list(self._analyzers.keys())

    def register_analyzer(self, role: GwtRole, analyzer: Any):
        """
        Manually register an analyzer for a GWT role.

        Args:
            role: GWT role (rpc_servlet, presenter, etc.)
            analyzer: Analyzer instance

        This is useful for testing or custom analyzer registration.
        """
        self._lazy_init()
        self._analyzers[role] = analyzer
        self.logger.info(f"Manually registered analyzer for {role.value}: {type(analyzer).__name__}")


# Global registry instance (singleton pattern)
_registry = None


def get_gwt_analyzer_registry() -> GwtAnalyzerRegistry:
    """
    Get the global GWT analyzer registry instance.

    Returns:
        GwtAnalyzerRegistry singleton
    """
    global _registry
    if _registry is None:
        _registry = GwtAnalyzerRegistry()
    return _registry
